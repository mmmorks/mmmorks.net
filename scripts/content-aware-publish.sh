#!/usr/bin/env bash
# Content-aware S3 publish with targeted CloudFront invalidation
# Only uploads files that actually changed (by MD5/ETag comparison)

set -e

BUCKET="${S3_BUCKET:?S3_BUCKET must be set}"
DISTRIBUTION="${CLOUDFRONT_DISTRIBUTION:?CLOUDFRONT_DISTRIBUTION must be set}"
OUTPUT_DIR="${OUTPUT_DIR:-output}"
PROFILE="${AWS_PROFILE:-s3-publish}"
DRY_RUN="${DRY_RUN:-false}"

count_lines() {
    if [ -z "$1" ]; then echo 0; else echo "$1" | wc -l | tr -d ' '; fi
}

echo "=== Content-aware publish ==="
echo "Bucket: $BUCKET"
echo "Distribution: $DISTRIBUTION"
echo "Output dir: $OUTPUT_DIR"
[ "$DRY_RUN" = "true" ] && echo "DRY RUN - no changes will be made"
echo ""

# Fetch S3 ETags
echo "Fetching S3 inventory..."
aws --profile "$PROFILE" s3api list-objects-v2 \
    --bucket "$BUCKET" \
    --output json 2>/dev/null \
    | jq -r '.Contents[]? | "\(.Key)\t\(.ETag | gsub("\""; ""))"' \
    | sort \
    > /tmp/s3-etags.txt

S3_COUNT=$(wc -l < /tmp/s3-etags.txt | tr -d ' ')
echo "Found $S3_COUNT files in S3"

# Compute local MD5s
echo "Computing local checksums..."
(cd "$OUTPUT_DIR" && find . -type f -print0 | xargs -0 md5 -r) \
    | awk '{gsub(/^\.\//, "", $2); print $2 "\t" $1}' \
    | sort \
    > /tmp/local-md5s.txt

LOCAL_COUNT=$(wc -l < /tmp/local-md5s.txt | tr -d ' ')
echo "Found $LOCAL_COUNT local files"
echo ""

# Compare
join -t $'\t' -a1 -a2 -o 0,1.2,2.2 \
    /tmp/s3-etags.txt \
    /tmp/local-md5s.txt \
    > /tmp/comparison.txt

# Categorize changes
NEW=$(awk -F'\t' '$2 == "" { print $1 }' /tmp/comparison.txt)
MODIFIED=$(awk -F'\t' '$2 != "" && $3 != "" && $2 != $3 { print $1 }' /tmp/comparison.txt)
DELETED=$(awk -F'\t' '$3 == "" { print $1 }' /tmp/comparison.txt)
UNCHANGED=$(awk -F'\t' '$2 != "" && $3 != "" && $2 == $3 { print $1 }' /tmp/comparison.txt)

NEW_COUNT=$(count_lines "$NEW")
MODIFIED_COUNT=$(count_lines "$MODIFIED")
DELETED_COUNT=$(count_lines "$DELETED")
UNCHANGED_COUNT=$(count_lines "$UNCHANGED")

echo "=== Changes detected ==="
echo "New:       $NEW_COUNT"
echo "Modified:  $MODIFIED_COUNT"
echo "Deleted:   $DELETED_COUNT"
echo "Unchanged: $UNCHANGED_COUNT"
echo ""

TO_UPLOAD=$(echo -e "${NEW}\n${MODIFIED}" | grep -v '^$' || true)
UPLOAD_COUNT=$(count_lines "$TO_UPLOAD")

if [ "$UPLOAD_COUNT" -eq 0 ] && [ "$DELETED_COUNT" -eq 0 ]; then
    echo "Nothing to do - all files are up to date"
    exit 0
fi

# Upload new and modified files
if [ "$UPLOAD_COUNT" -gt 0 ]; then
    MAX_JOBS=3
    echo "=== Uploading $UPLOAD_COUNT files (max $MAX_JOBS parallel) ==="
    job_count=0

    while read -r key; do
        local_path="$OUTPUT_DIR/$key"
        s3_path="s3://$BUCKET/$key"

        # Determine content type
        case "$key" in
            *.html) content_type="text/html" ;;
            *.css)  content_type="text/css" ;;
            *.js)   content_type="application/javascript" ;;
            *.json) content_type="application/json" ;;
            *.xml)  content_type="application/xml" ;;
            *.svg)  content_type="image/svg+xml" ;;
            *.png)  content_type="image/png" ;;
            *.jpg|*.jpeg) content_type="image/jpeg" ;;
            *.gif)  content_type="image/gif" ;;
            *.woff) content_type="font/woff" ;;
            *.woff2) content_type="font/woff2" ;;
            *.wasm) content_type="application/wasm" ;;
            *.txt)  content_type="text/plain" ;;
            *.st)   content_type="application/octet-stream" ;;
            *)      content_type="application/octet-stream" ;;
        esac

        if [ "$DRY_RUN" = "true" ]; then
            echo "[dry-run] upload: $key ($content_type)"
        else
            echo "upload: $key"
            (
                aws --profile "$PROFILE" s3 cp "$local_path" "$s3_path" \
                    --content-type "$content_type" \
                    --quiet
            ) &

            ((++job_count))
            if [ "$job_count" -ge "$MAX_JOBS" ]; then
                wait -n
                ((--job_count))
            fi
        fi
    done <<< "$TO_UPLOAD"
    wait
    echo ""
fi

# Delete removed files
if [ "$DELETED_COUNT" -gt 0 ]; then
    echo "=== Deleting $DELETED_COUNT files ==="
    echo "$DELETED" | while read -r key; do
        s3_path="s3://$BUCKET/$key"

        if [ "$DRY_RUN" = "true" ]; then
            echo "[dry-run] delete: $key"
        else
            echo "delete: $key"
            aws --profile "$PROFILE" s3 rm "$s3_path" --quiet
        fi
    done
    echo ""
fi

# Invalidate CloudFront cache for changed paths
ALL_CHANGED=$(echo -e "${NEW}\n${MODIFIED}\n${DELETED}" | grep -v '^$' | sort -u || true)
INVALIDATE_COUNT=$(count_lines "$ALL_CHANGED")

if [ "$INVALIDATE_COUNT" -gt 0 ]; then
    echo "=== Invalidating $INVALIDATE_COUNT CloudFront paths ==="

    # Build paths array (prepend /)
    PATHS=$(echo "$ALL_CHANGED" | sed 's|^|/|' | tr '\n' ' ')

    if [ "$DRY_RUN" = "true" ]; then
        echo "[dry-run] Would invalidate:"
        echo "$ALL_CHANGED" | sed 's|^|  /|'
    else
        # CloudFront allows up to 3000 paths per invalidation
        if [ "$INVALIDATE_COUNT" -le 3000 ]; then
            aws --profile "$PROFILE" cloudfront create-invalidation \
                --distribution-id "$DISTRIBUTION" \
                --paths $PATHS \
                --output text \
                | head -1
        else
            echo "Warning: $INVALIDATE_COUNT paths exceeds CloudFront limit, using wildcard"
            aws --profile "$PROFILE" cloudfront create-invalidation \
                --distribution-id "$DISTRIBUTION" \
                --paths "/*" \
                --output text \
                | head -1
        fi
    fi
    echo ""
fi

echo "=== Done ==="
echo "Uploaded:    $UPLOAD_COUNT"
echo "Deleted:     $DELETED_COUNT"
echo "Invalidated: $INVALIDATE_COUNT"
