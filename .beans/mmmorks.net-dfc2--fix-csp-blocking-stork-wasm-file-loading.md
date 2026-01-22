---
# mmmorks.net-dfc2
title: Fix CSP blocking Stork WASM file loading
status: completed
type: bug
priority: normal
created_at: 2026-01-22T07:47:54Z
updated_at: 2026-01-22T07:49:32Z
---

Content-Security-Policy connect-src directive is blocking the Stork search WASM file from loading from files.stork-search.net. Need to update CSP to allow this external resource.