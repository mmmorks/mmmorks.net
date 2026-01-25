---
# mmmorks.net-uo2w
title: Fix CSP frame-src to allow commentbox.io iframes
status: in-progress
type: bug
created_at: 2026-01-22T08:32:39Z
updated_at: 2026-01-22T08:32:39Z
---

The Content-Security-Policy frame-src directive is set to 'self' which blocks commentbox.io from loading its iframe at https://app.commentbox.io. Need to update the CloudFront distribution's CSP headers to allow frame-src 'self' https://app.commentbox.io.

## Checklist
- [x] Get current CloudFront distribution configuration
- [x] Identify the CSP response headers policy
- [x] Update frame-src directive to include https://app.commentbox.io
- [x] Apply the changes to CloudFront
- [ ] Test that commentbox.io loads without CSP errors

## Changes Made
- Updated CloudFront Response Headers Policy ID: 96e32b70-61af-4fd8-84a3-74910ae98cbe
- Cleaned up CSP by removing unused CDN sources:
  - Removed jQuery CDN from script-src
  - Removed Bootstrap CDN from script-src
  - Removed Stork CDN from style-src
- Added `https://app.commentbox.io` to frame-src directive
- New frame-src: `frame-src 'self' https://app.commentbox.io`