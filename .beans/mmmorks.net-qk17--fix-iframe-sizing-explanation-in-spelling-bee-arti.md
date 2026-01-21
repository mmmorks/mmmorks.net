---
# mmmorks.net-qk17
title: Fix iframe sizing explanation in Spelling Bee article
status: completed
type: task
priority: normal
created_at: 2026-01-20T03:12:43Z
updated_at: 2026-01-20T03:18:01Z
---

The dynamic iframe sizing section doesn't correctly explain the problem. The iframe after hiding the unwanted divs had a ton of whitespace. We needed a way to resize it and the iframe couldn't resize itself; we needed the parent to resize it, which introduces the need for postmessage.

File: content/articles/spelling-bee-buddy-extension.md
Section: Challenge 2: Dynamic iframe Sizing