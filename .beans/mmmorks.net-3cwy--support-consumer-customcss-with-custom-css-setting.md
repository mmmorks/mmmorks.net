---
# mmmorks.net-3cwy
title: Support consumer custom.css with CUSTOM_CSS setting
status: completed
type: feature
priority: normal
created_at: 2026-01-26T06:30:34Z
updated_at: 2026-01-26T06:40:41Z
---

The theme currently has a hardcoded reference to custom.css that doesn't work.

## History

- **2013** (44b3d28): Added `{% if CUSTOM_CSS %}` conditional and empty `static/css/custom.css` file in theme
  - `CUSTOM_CSS` was a boolean setting users would set to enable loading the theme's custom.css file
  - Users would edit the theme's custom.css directly (problematic for upgrades)
- **2014** (c4084f1): Removed `CUSTOM_CSS` setting "as it is no longer required"
  - But left the conditional in template and the file in place
- **2026** (adb827d): esbuild migration removed the conditional, making the link hardcoded
  - This broke the feature since no check for the setting anymore
- **2026** (8bfa5f9): CSS modernization deleted `static/css/custom.css` file
  - Theme's CSS variables moved to `base/variables.css` and `themes/dark-mode.css`
  - But template link remained, now pointing to non-existent file

## Current Issues

1. Template has hardcoded link to `{{ THEME_STATIC_DIR }}/css/custom.css` which doesn't exist
2. No build step creates this file
3. Documentation says to create custom template extending base.html (too complex for simple CSS addition)
4. No conditional check for whether custom CSS is actually configured
5. Browser gets 404 error for missing custom.css

## Note on Existing Settings

- `CSS_FILE` is an official Pelican setting, but it's for the built-in `notmyidea` theme only
- `CUSTOM_CSS` was an Elegant-specific boolean setting, now removed
- No standard Pelican setting exists for site-specific custom CSS paths

## Proposed Solution

Add a `CUSTOM_CSS` setting that consumers can use to specify a custom CSS file path:

```python
# In pelicanconf.py
STATIC_PATHS = ['static']
CUSTOM_CSS = 'static/css/custom.css'
```

Note: `EXTRA_PATH_METADATA` is not needed since `STATIC_PATHS` already copies files to the correct location preserving directory structure.

## Checklist

- [x] Remove hardcoded custom.css link from templates/base.html
- [x] Add conditional link that checks for CUSTOM_CSS setting
- [x] Update documentation/content/Advanced Features/custom-style.md to explain the new approach
- [x] Test with and without CUSTOM_CSS setting configured
- [x] Verify the path resolution works correctly

## Test Results

Tested on mmmorks.net blog:
- Without `CUSTOM_CSS`: No custom.css link in output ✅
- With `CUSTOM_CSS = 'static/css/custom.css'`: Link appears and file copied correctly ✅
- Simplified config (removed unnecessary `EXTRA_PATH_METADATA`) works perfectly ✅