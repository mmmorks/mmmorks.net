---
# mmmorks.net-u98t
title: Add CloudFront invalidation to publish workflow
status: completed
type: task
priority: normal
created_at: 2026-01-21T02:50:16Z
updated_at: 2026-01-21T02:58:08Z
---

Discover CloudFront distribution ID and create a comprehensive publish target in Makefile that builds, uploads to S3, and invalidates CloudFront cache.

## Checklist
- [x] Find CloudFront distribution ID in infrastructure config
- [x] Add CloudFront invalidation target to Makefile
- [x] Create comprehensive publish target combining all steps
- [x] Test the new targets

## Found Distribution
- Distribution ID: E1E2AB2CCOLUJJ
- Domain: d3m0rtze23w79k.cloudfront.net