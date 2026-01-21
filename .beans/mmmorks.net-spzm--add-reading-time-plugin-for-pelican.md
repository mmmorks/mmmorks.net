---
# mmmorks.net-spzm
title: Add reading time plugin for Pelican
status: completed
type: feature
priority: normal
created_at: 2026-01-21T08:23:30Z
updated_at: 2026-01-21T08:29:12Z
---

Add a reading time estimation feature to blog posts, mimicking Medium's style (e.g., '5 min read'). Use the readtime library to calculate reading time and display it prominently on articles.

## Checklist
- [x] Explore current Pelican setup and theme structure
- [x] Research readtime library and Pelican plugin options
- [x] Modify post_stats plugin to use Medium's 265 WPM
- [x] Enable post_stats plugin in pelicanconf.py
- [x] Update post_stats.html template to match Medium's style (remove tilde, remove minimum)
- [x] Test reading time calculation on existing articles
- [x] Rebuild site and verify display