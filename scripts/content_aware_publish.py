#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["boto3"]
# ///
"""
Content-aware S3 publish with targeted CloudFront invalidation.
Only uploads files that actually changed (by MD5/ETag comparison).
"""

import hashlib
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import boto3
from botocore.config import Config as BotoConfig


@dataclass
class Config:
    bucket: str
    distribution: str
    output_dir: Path
    profile: str
    dry_run: bool
    max_workers: int = 3


@dataclass
class ChangeSet:
    new: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)

    @property
    def to_upload(self) -> list[str]:
        return self.new + self.modified

    @property
    def all_changed(self) -> list[str]:
        return sorted(set(self.new + self.modified + self.deleted))


@dataclass
class UploadResult:
    key: str
    success: bool
    error: Optional[str] = None


CONTENT_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.wasm': 'application/wasm',
    '.txt': 'text/plain',
    '.st': 'application/octet-stream',
}

BOTO_CONFIG = BotoConfig(
    retries={'mode': 'standard', 'max_attempts': 3}
)


def load_config() -> Config:
    """Load configuration from environment variables."""
    bucket = os.environ.get('S3_BUCKET')
    distribution = os.environ.get('CLOUDFRONT_DISTRIBUTION')
    output_dir = os.environ.get('OUTPUT_DIR', 'output')
    profile = os.environ.get('AWS_PROFILE', 's3-publish')
    dry_run = os.environ.get('DRY_RUN', 'false').lower() == 'true'

    errors = []
    if not bucket:
        errors.append('S3_BUCKET must be set')
    if not distribution:
        errors.append('CLOUDFRONT_DISTRIBUTION must be set')

    if errors:
        for err in errors:
            print(f"Error: {err}", file=sys.stderr)
        sys.exit(2)

    return Config(
        bucket=bucket,
        distribution=distribution,
        output_dir=Path(output_dir),
        profile=profile,
        dry_run=dry_run,
    )


def fetch_s3_inventory(s3_client, bucket: str) -> dict[str, str]:
    """
    Fetch all S3 object ETags using pagination.
    Returns dict mapping key -> etag (without quotes).
    """
    inventory = {}
    paginator = s3_client.get_paginator('list_objects_v2')

    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get('Contents', []):
            # ETags from S3 come wrapped in quotes
            etag = obj['ETag'].strip('"')
            inventory[obj['Key']] = etag

    return inventory


def compute_local_checksums(output_dir: Path) -> dict[str, str]:
    """
    Compute MD5 checksums for all local files.
    Returns dict mapping relative path -> md5 hex digest.
    """
    checksums = {}

    for path in output_dir.rglob('*'):
        if path.is_file():
            rel_path = str(path.relative_to(output_dir))
            md5 = hashlib.md5()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5.update(chunk)
            checksums[rel_path] = md5.hexdigest()

    return checksums


def compute_changes(s3_inventory: dict[str, str], local_checksums: dict[str, str]) -> ChangeSet:
    """Compare S3 ETags vs local MD5s to determine what changed."""
    changes = ChangeSet()

    all_keys = set(s3_inventory.keys()) | set(local_checksums.keys())

    for key in all_keys:
        s3_etag = s3_inventory.get(key)
        local_md5 = local_checksums.get(key)

        if s3_etag is None:
            # Not in S3, but exists locally -> new
            changes.new.append(key)
        elif local_md5 is None:
            # In S3, but not locally -> deleted
            changes.deleted.append(key)
        elif s3_etag != local_md5:
            # Both exist but different -> modified
            changes.modified.append(key)
        else:
            # Both exist and match -> unchanged
            changes.unchanged.append(key)

    return changes


def get_content_type(key: str) -> str:
    """Determine content type based on file extension."""
    ext = Path(key).suffix.lower()
    return CONTENT_TYPES.get(ext, 'application/octet-stream')


def upload_file(
    s3_client,
    bucket: str,
    key: str,
    local_path: Path,
    content_type: str,
) -> UploadResult:
    """Upload a single file. Retries are handled by boto3's standard retry mode."""
    try:
        s3_client.upload_file(
            str(local_path),
            bucket,
            key,
            ExtraArgs={'ContentType': content_type},
        )
        return UploadResult(key=key, success=True)
    except Exception as e:
        return UploadResult(key=key, success=False, error=str(e))


def upload_files_parallel(
    s3_client,
    config: Config,
    keys: list[str],
) -> list[UploadResult]:
    """Upload files in parallel using ThreadPoolExecutor."""
    results = []

    with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
        futures = {}

        for key in keys:
            local_path = config.output_dir / key
            content_type = get_content_type(key)

            future = executor.submit(
                upload_file,
                s3_client,
                config.bucket,
                key,
                local_path,
                content_type,
            )
            futures[future] = key

        for future in as_completed(futures):
            result = future.result()
            status = "ok" if result.success else f"FAILED ({result.error})"
            print(f"  upload: {result.key} [{status}]")
            results.append(result)

    return results


def delete_files(s3_client, bucket: str, keys: list[str], dry_run: bool) -> bool:
    """
    Delete files from S3 using batch delete.
    Returns True if all deletes succeeded.
    """
    if not keys:
        return True

    if dry_run:
        for key in keys:
            print(f"  [dry-run] delete: {key}")
        return True

    # delete_objects accepts up to 1000 keys per call
    success = True
    for i in range(0, len(keys), 1000):
        batch = keys[i:i + 1000]
        delete_request = {
            'Objects': [{'Key': key} for key in batch],
            'Quiet': True,
        }

        try:
            response = s3_client.delete_objects(Bucket=bucket, Delete=delete_request)
            errors = response.get('Errors', [])
            if errors:
                success = False
                for err in errors:
                    print(f"  delete FAILED: {err['Key']} - {err['Message']}")
            else:
                for key in batch:
                    print(f"  delete: {key}")
        except Exception as e:
            success = False
            print(f"  delete batch FAILED: {e}")

    return success


def invalidate_cloudfront(
    cf_client,
    distribution_id: str,
    paths: list[str],
    dry_run: bool,
) -> bool:
    """Create CloudFront invalidation for changed paths."""
    if not paths:
        return True

    # Prepend / to each path
    invalidation_paths = [f"/{p}" for p in paths]

    if dry_run:
        print("  [dry-run] Would invalidate:")
        for p in invalidation_paths:
            print(f"    {p}")
        return True

    try:
        # CloudFront allows up to 3000 paths per invalidation
        if len(invalidation_paths) > 3000:
            print(f"  Warning: {len(invalidation_paths)} paths exceeds CloudFront limit, using wildcard")
            invalidation_paths = ['/*']

        response = cf_client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(invalidation_paths),
                    'Items': invalidation_paths,
                },
                'CallerReference': str(int(time.time() * 1000)),
            },
        )
        invalidation_id = response['Invalidation']['Id']
        print(f"  Invalidation created: {invalidation_id}")
        return True

    except Exception as e:
        print(f"  Invalidation FAILED: {e}")
        return False


def report_results(
    changes: ChangeSet,
    upload_results: list[UploadResult],
    delete_success: bool,
    invalidate_success: bool,
) -> int:
    """Print summary and return exit code."""
    print("\n=== Summary ===")
    print(f"Uploaded:    {len(upload_results)}")
    print(f"Deleted:     {len(changes.deleted)}")
    print(f"Invalidated: {len(changes.all_changed)}")

    failed_uploads = [r for r in upload_results if not r.success]
    if failed_uploads:
        print(f"\n=== Failed uploads ({len(failed_uploads)}) ===")
        for r in failed_uploads:
            print(f"  {r.key}: {r.error}")

    if failed_uploads or not delete_success or not invalidate_success:
        return 1
    return 0


def main() -> int:
    config = load_config()

    print("=== Content-aware publish ===")
    print(f"Bucket: {config.bucket}")
    print(f"Distribution: {config.distribution}")
    print(f"Output dir: {config.output_dir}")
    if config.dry_run:
        print("DRY RUN - no changes will be made")
    print()

    # Create AWS clients
    session = boto3.Session(profile_name=config.profile)
    s3_client = session.client('s3', config=BOTO_CONFIG)
    cf_client = session.client('cloudfront', config=BOTO_CONFIG)

    # Fetch S3 inventory
    print("Fetching S3 inventory...")
    s3_inventory = fetch_s3_inventory(s3_client, config.bucket)
    print(f"Found {len(s3_inventory)} files in S3")

    # Compute local checksums
    print("Computing local checksums...")
    local_checksums = compute_local_checksums(config.output_dir)
    print(f"Found {len(local_checksums)} local files")
    print()

    # Compute changes
    changes = compute_changes(s3_inventory, local_checksums)

    print("=== Changes detected ===")
    print(f"New:       {len(changes.new)}")
    print(f"Modified:  {len(changes.modified)}")
    print(f"Deleted:   {len(changes.deleted)}")
    print(f"Unchanged: {len(changes.unchanged)}")
    print()

    if not changes.to_upload and not changes.deleted:
        print("Nothing to do - all files are up to date")
        return 0

    # Upload new and modified files
    upload_results = []
    if changes.to_upload:
        print(f"=== Uploading {len(changes.to_upload)} files (max {config.max_workers} parallel) ===")
        if config.dry_run:
            for key in changes.to_upload:
                content_type = get_content_type(key)
                print(f"  [dry-run] upload: {key} ({content_type})")
        else:
            upload_results = upload_files_parallel(s3_client, config, changes.to_upload)
        print()

    # Delete removed files
    delete_success = True
    if changes.deleted:
        print(f"=== Deleting {len(changes.deleted)} files ===")
        delete_success = delete_files(s3_client, config.bucket, changes.deleted, config.dry_run)
        print()

    # Invalidate CloudFront cache
    invalidate_success = True
    if changes.all_changed:
        print(f"=== Invalidating {len(changes.all_changed)} CloudFront paths ===")
        invalidate_success = invalidate_cloudfront(
            cf_client, config.distribution, changes.all_changed, config.dry_run
        )
        print()

    return report_results(changes, upload_results, delete_success, invalidate_success)


if __name__ == '__main__':
    sys.exit(main())
