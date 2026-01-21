---
# mmmorks.net-ew21
title: Clean up untracked files
status: todo
type: task
priority: low
created_at: 2026-01-20T03:13:28Z
updated_at: 2026-01-20T03:13:28Z
---

Review and handle untracked files in the repo:

- .DS_Store - Should be in .gitignore
- convos/ - Directory with 60 conversation files, may want to archive or gitignore
- plugins/ - Has extract_toc.py plugin, decide if should be committed
- todo - Plain text todo file, can be removed once beans are created