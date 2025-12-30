Title: Building a Cross-Browser Extension: NYT Spelling Bee Buddy Embedder
Date: 2025-12-29
Category: Web Development
Tags: browser-extensions, javascript, manifest-v3, firefox, chrome
Slug: spelling-bee-buddy-extension
Summary: A technical deep dive into creating a cross-browser extension that enhances the NYT Spelling Bee game by embedding helpful reference tools directly into the page, and a look at modern AI-assisted development.

## The Problem

The [NYT Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) is an addictive word puzzle, and the New York Times provides an excellent companion tool called the [Spelling Bee Buddy](https://www.nytimes.com/interactive/2023/upshot/spelling-bee-buddy.html) that shows a grid and two-letter list to help players find words. However, this tool lives on a separate page, requiring players to constantly switch tabs whilst playing.

The goal: embed the Buddy's grid and two-letter list directly into the game page for easy reference.

![NYT Spelling Bee Game]({static}/images/spelling-bee-game.png)
*The NYT Spelling Bee puzzle interface*

![Spelling Bee Buddy Grid]({static}/images/spelling-bee-buddy.png)
*The Buddy's grid and two-letter list on a separate page*

![Spelling Bee Buddy Extension in Action]({static}/images/spelling-bee-extension-screenshot.png)
*The extension embeds the Buddy directly below the game for easy reference*

## Development Approach: Building with Claude Code

This extension was built over multiple sessions with Claude Code, taking an iterative approach to both implementation and optimization. Rather than a single coding session, the development spanned several days with distinct phases—each session building on insights from the previous one.

**Development Phases:**

- **Initial Implementation:** Core iframe embedding, dropdown date manipulation attempt
- **Simplification:** URL parameter discovery, deleting the complex solution
- **Performance Tuning:** Console log-driven optimization, removing unnecessary fallbacks
- **Cross-Browser Support:** Dual-manifest strategy for Firefox MV2 and Chrome MV3
- **Publishing Polish:** Icon design, AMO validation fixes, final UX improvements

The development took approximately 5 hours spread over two days, with each session building on insights from the previous one.

What made this collaboration effective was the back-and-forth: Claude would suggest optimizations, I'd evaluate whether they actually improved the code, and we'd iterate. Not every suggestion was accepted—some made the code worse, and recognising that was part of the process.

## Initial Approach: Simple iframe Injection

The first iteration was straightforward - inject an iframe into the game page that loads the Buddy content:

```javascript
const iframe = document.createElement('iframe');
iframe.src = 'https://www.nytimes.com/interactive/2023/upshot/spelling-bee-buddy.html';
gameContainer.insertAdjacentElement('afterend', iframe);
```

This worked, but with a major problem: the iframe loaded the entire Buddy page, including headers, footers, date selectors, and other sections we didn't need. Players only wanted the grid and two-letter list.

## Challenge 1: Filtering iframe Content

The obvious solution was to inject CSS into the iframe to hide unwanted sections. However, this created several issues:

1. **Cross-origin access**: Direct iframe manipulation via `contentDocument` had limitations
2. **Timing issues**: Content loaded asynchronously, requiring MutationObservers
3. **Complexity**: The main content script became bloated with iframe manipulation logic

### The Solution: Separate Content Scripts

Instead of manipulating the iframe from outside, I created a dedicated content script (`iframe-content.js`) that runs *inside* the Buddy iframe:

```javascript
// manifest.json
"content_scripts": [
  {
    "matches": ["https://www.nytimes.com/puzzles/spelling-bee*"],
    "js": ["constants.js", "content.js"]
  },
  {
    "matches": ["https://www.nytimes.com/interactive/*/upshot/spelling-bee-buddy.html*"],
    "js": ["constants.js", "iframe-content.js"],
    "all_frames": true  // Runs in iframes too
  }
]
```

The manifest's `"all_frames": true` setting means the script runs both when the Buddy page loads in an iframe *and* when users visit it directly. This was a surprise—I'd assumed it only applied to iframes. The solution was a simple check at the top of the script:

```javascript
// Only run when in an iframe (not standalone page)
if (window.self === window.top) {
  return;
}

const style = document.createElement('style');
style.textContent = `
  .sb-buddy-container > * {
    display: none !important;
  }
  .the-square,
  .the-square-part-two {
    display: block !important;
  }
  /* Hide headers, footers, etc. */
`;
document.head.appendChild(style);
```

This approach is cleaner because:

- The iframe script has full access to its own DOM
- No cross-origin issues
- Timing is simpler—the script runs when the iframe loads
- Separation of concerns—each script manages its own domain

## Challenge 2: Dynamic iframe Sizing

Since we're hiding sections of the Buddy page, the iframe needs to dynamically adjust its height to fit only the visible content.

### The postMessage Pattern

The iframe content script measures its own content and communicates back to the parent:

```javascript
// Inside iframe-content.js
function sendHeight() {
  const container = document.querySelector('.sb-buddy-container');
  if (container) {
    const height = container.scrollHeight + 40;
    window.parent.postMessage({
      type: 'spelling-bee-buddy-resize',
      height
    }, 'https://www.nytimes.com');
  }
}
```

The main content script listens and updates the iframe:

```javascript
// Inside content.js
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://www.nytimes.com') return;
  if (event.data && event.data.type === 'spelling-bee-buddy-resize') {
    iframe.style.height = event.data.height + 'px';
  }
});
```

A ResizeObserver ensures the height updates whenever the content changes:

```javascript
const resizeObserver = new ResizeObserver(sendHeight);
resizeObserver.observe(container);
```

## Challenge 3: Date Synchronisation

The Spelling Bee allows playing historical puzzles via URLs like `/puzzles/spelling-bee/2025-12-27`. The Buddy needs to display the same date's grid.

This feature evolved through three distinct approaches, each simpler than the last—a classic engineering journey from over-engineering to elegance.

### Attempt 1: Dropdown Manipulation (200+ Lines of Code)

My first instinct was to programmatically interact with the Buddy page's date selector—a Svelte Select component. This led to an incredibly complex solution involving:

1. Finding the hidden input containing JSON data about the selected date
2. Clicking multiple DOM elements to trigger the dropdown
3. Waiting for the dropdown to render
4. Searching through list items for the matching date
5. Clicking the correct item

The code looked like this:

```javascript
// Find dropdown, open it, search through items, click the matching date...
const listItems = iframeDoc.querySelectorAll('.svelte-select-list .list-item');
for (const item of listItems) {
  const itemData = item.getAttribute('data-value');
  if (itemData) {
    const itemObj = JSON.parse(itemData);
    if (itemObj.date === targetDate) {
      item.click(); // Finally!
    }
  }
}
```

This approach was fragile, overly complex, and felt wrong. It required multiple `setTimeout` calls, worked inconsistently, and spanned over 200 lines of code.

### Attempt 2: URL Parameters (2 Lines of Code)

Claude suggested analyzing the beautified JavaScript source to understand how the Buddy page works. Using `npx js-beautify` on the minified bundles, we found this line:

```javascript
window.location.search && new URLSearchParams(window.location.search).has("date")
```

The Buddy page already supported a `?date=YYYY-MM-DD` URL parameter! I deleted all 200+ lines of dropdown manipulation code and replaced it with:

```javascript
iframe.src = `${BUDDY_URL}?date=${gameDate}`;
```

That moment of deleting 200+ lines of carefully crafted (but misguided) code was both humbling and liberating. Sometimes the sign of good engineering isn't the complexity you create, but the complexity you eliminate.

The URL parameter approach became the final solution. The extension simply parses the date from the game page URL and appends it to the Buddy iframe URL:

```javascript
function parseGameUrl(url) {
  const match = url.match(/\/spelling-bee(?:\/(\d{4}-\d{2}-\d{2})|\/?$)/);
  return {
    isValid: match !== null,
    gameDate: match?.[1] || null
  };
}
```

For historical puzzles with dates in the URL (like `/spelling-bee/2025-12-27`), the regex extracts the date. For today's puzzle (just `/spelling-bee`), `gameDate` is `null`, and the Buddy page defaults to today.

```javascript
// Final implementation - simple and reliable
const { gameDate } = parseGameUrl(window.location.href);
iframe.src = BUDDY_URL + (gameDate ? `?date=${gameDate}` : '');
```

### The Path Not Taken: window.gameData

During development, I briefly explored accessing the page's `window.gameData.today.printDate` variable directly. However, content scripts run in an isolated JavaScript context and can't access page variables without injecting a script element, setting up event communication, and polling for availability. The URL parameter approach was already working perfectly and far simpler, so I abandoned this dead end quickly.

## Challenge 4: Cross-Browser Compatibility

With the core functionality working reliably in Firefox (my primary browser), I was curious how much effort would be needed to make this work in Chromium-based browsers too. Modern browser extensions face a unique challenge: Firefox and Chrome have diverged in their implementation of Manifest V3, particularly around permissions.

Manifest V3 support in Firefox has some quirks and non-obvious differences in behaviour between V2 and even V3 in Chromium. The most problematic: Firefox treats MV3 `host_permissions` as optional, allowing users to deny them. This breaks the extension since it requires access to inject content scripts.

```json
// Manifest V3 - permissions shown as "optional" in Firefox
"host_permissions": [
  "https://www.nytimes.com/*"
]
```

[Firefox bug #1839129](https://bugzilla.mozilla.org/show_bug.cgi?id=1839129) tracks this behaviour.

### The Solution: Dual Manifests

I created separate manifest files for each browser:

**manifest.json** (Chrome - Manifest V3):
```json
{
  "manifest_version": 3,
  "content_scripts": [...]
}
```

**manifest-firefox.json** (Firefox - Manifest V2):
```json
{
  "manifest_version": 2,
  "permissions": [
    "https://www.nytimes.com/puzzles/spelling-bee*",
    "https://www.nytimes.com/interactive/*/upshot/spelling-bee-buddy.html*"
  ],
  "content_scripts": [...]
}
```

In Manifest V2, permissions listed in the `permissions` array are required and properly displayed during installation.

The extension evolved through an interesting architectural decision:

1. **Started:** Firefox-only with Manifest V2
2. **Attempted:** Migration to Manifest V3 for Chrome compatibility
3. **Discovered:** Firefox treats MV3 `host_permissions` as optional (users can deny), breaking the extension
4. **Final solution:** Maintain two manifests

### Build Script

The build script swaps manifests during packaging:

```bash
# Firefox build - use Manifest V2
mv manifest.json manifest-chrome.json.tmp
mv manifest-firefox.json manifest.json
zip -r extension-firefox.xpi manifest.json content.js ...

# Restore for Chrome build
mv manifest.json manifest-firefox.json
mv manifest-chrome.json.tmp manifest.json
zip -r extension-chrome.zip manifest.json content.js ...
```

This dual-manifest approach lets us optimise for each browser's permission model whilst maintaining a single codebase. The only difference between the packages is the manifest version and structure.

## Challenge 5: Performance Optimization and Refactoring

After getting the basic functionality working, I dedicated an entire session to identifying and eliminating unnecessary code, defensive programming patterns, and performance bottlenecks. This systematic cleanup revealed how easily "defensive" code can become wasteful code.

### The Console Log Investigation

The optimization started with a simple question: "Are there unnecessary fallbacks in the code?" I enabled verbose console logging and watched what actually happened when the extension loaded.

The logs revealed several surprises:

- The extension tried 7 different container selectors, but only `#js-hook-game-wrapper` ever matched
- "Already embedded" appeared 6 times—the MutationObserver was calling `embedBuddy()` repeatedly
- Resize was logged 10+ times during initial load
- Date extraction searched through script #4 of 49 total scripts

**This empirical data drove targeted optimizations.** Instead of guessing what might be slow, I measured what was actually happening.

### Removing Unnecessary Fallbacks

The initial implementation had excessive defensive coding:

**Problem 1: Multiple Container Selectors**

The original code tried 7 different selectors to find the game container:

```javascript
const possibleSelectors = [
  '#js-hook-game-wrapper',
  '.pz-game-wrapper',
  '.pz-game-screen',
  '#spelling-bee-container',
  '.pz-section',
  // ... more
];

for (const selector of possibleSelectors) {
  gameContainer = document.querySelector(selector);
  if (gameContainer) break;
}
```

By checking the actual NYT page structure, I found that **only one selector ever matched**: `#js-hook-game-wrapper`. All the others were dead code. The fix:

```javascript
const gameContainer = document.querySelector('#js-hook-game-wrapper');
```

**Problem 2: Aggressive MutationObserver**

The original code used a MutationObserver that ran indefinitely, calling `embedBuddy()` on every DOM change:

```javascript
const observer = new MutationObserver(() => embedBuddy());
observer.observe(document.body, {
  childList: true,
  subtree: true,
  attributes: true,      // Unnecessary
  characterData: true    // Unnecessary
});
```

Console logs showed it was being called 6+ times after the embed succeeded. The fix:

```javascript
// embedBuddy() is idempotent, but we should still disconnect when done
const observer = new MutationObserver(() => {
  embedBuddy();
  if (document.getElementById('spelling-bee-buddy-container')) {
    observer.disconnect();
    console.log('[Spelling Bee Buddy] MutationObserver stopped');
  }
});

// Only observe if not already embedded
if (!document.getElementById('spelling-bee-buddy-container')) {
  observer.observe(document.body, {
    childList: true,
    subtree: true
    // Removed attributes and characterData - only need to detect element additions
  });
}
```

Better yet, we can simplify this even further—we don't actually need the MutationObserver at all!

**Problem 3: Internet Explorer Compatibility... in Firefox**

```javascript
const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
```

The `|| iframe.contentWindow.document` fallback is for IE compatibility. Completely unnecessary in a modern Firefox/Chrome extension.

**Problem 4: Redundant Document Ready Check**

```javascript
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', embedBuddy);
} else {
  embedBuddy();
}
```

The manifest already specifies `"run_at": "document_idle"`, which means the script runs **after** DOMContentLoaded. This check is pointless—it will never be 'loading'.

### Date Extraction Performance

As mentioned in Challenge 3, the initial approach was to parse script tags looking for the date:

```javascript
// Original: Parse ALL script tags
const scripts = document.querySelectorAll('script');
for (const script of scripts) {
  const dateMatch = script.textContent.match(/"printDate":\s*"(\d{4}-\d{2}-\d{2})"/);
  if (dateMatch) return dateMatch[1];
}
```

On the NYT Spelling Bee page, this meant:

- Querying all 49 script tags
- Reading potentially massive webpack bundles (>500KB each)
- Running regex on megabytes of minified JavaScript

**Optimization attempts:**

1. **Check URL first** (moved to first priority - instant if date in URL)
2. **Target JSON scripts** before parsing JS bundles
3. **Skip massive bundles** (>500KB)
4. **Check only first 10 inline scripts**

But all of this became unnecessary with the URL parameter approach! Simple regex matching is essentially free compared to parsing megabytes of JavaScript.

### MutationObserver Optimization in iframe

Inside the iframe, the original code had a MutationObserver watching for content changes to trigger resize:

```javascript
const observer = new MutationObserver(() => resizeIframe());
observer.observe(container, {
  childList: true,
  subtree: true,
  attributes: true,      // Overkill
  characterData: true    // Overkill
});
```

This caused excessive resize calls (10+ times during initial load). The fix:

```javascript
// Only watch for initial content load, then disconnect
let initialLoadComplete = false;
const observer = new MutationObserver(() => {
  if (initialLoadComplete) return;

  const gridSection = iframeDoc.querySelector('.the-square');
  const twoLetterSection = iframeDoc.querySelector('.the-square-part-two');

  if (gridSection && twoLetterSection &&
      gridSection.offsetHeight > 0 && twoLetterSection.offsetHeight > 0) {
    initialLoadComplete = true;
    observer.disconnect();
    resizeIframe();
  }
});

// Only watch childList and subtree (element additions, not attribute changes)
observer.observe(container, {
  childList: true,
  subtree: true
});

// Let ResizeObserver handle ongoing size changes
const resizeObserver = new ResizeObserver(resizeIframe);
resizeObserver.observe(container);
```

Result: Down from 10+ resize calls to just 2 (initial + one adjustment).

### Code Reduction

The optimization work produced measurable improvements in code quality:

**Code Size:**
- Before: ~250 lines with defensive fallbacks
- After: ~150 lines of focused code
- Result: 40% reduction, improved readability

**Dead Code Eliminated:**
- 7 redundant container selectors → 1
- Duplicate date fallback logic removed
- IE compatibility code removed
- 100+ lines of unused fallbacks deleted

These improvements made the codebase significantly more maintainable by removing code that never executed.

## The Refactoring Debate: When AI Suggestions Go Too Far

During the optimization work, I asked Claude to extract magic numbers into a constants file to clean up the code. However, Claude took the directive to the extreme, extracting nearly every literal value. This led to an interesting discussion about when refactoring actually improves code versus when it makes it worse.

### What Claude Extracted

```javascript
// constants.js (initial version)
const TEXT = {
  HEADER_TITLE: 'Spelling Bee Buddy',
  IFRAME_TITLE: 'Spelling Bee Buddy - Grid & Two-Letter List',
  LOG_PREFIX: '[Spelling Bee Buddy]'
};

const SELECTORS = {
  BUDDY_CONTAINER: '#spelling-bee-buddy-container',  // Our own ID!
  BUDDY_HEADER: '.buddy-header',                      // Our own class!
  // ... 8 more internal selectors
};
```

And the CSS got the same treatment:

```css
:root {
  --sbb-container-max-width: 1200px;
  --sbb-container-margin-vertical: 30px;
  --sbb-header-font-size: 24px;
  /* ... 15 more custom properties */
}

#spelling-bee-buddy-container {
  max-width: var(--sbb-container-max-width);
  margin: var(--sbb-container-margin-vertical) auto;
}
```

### My Pushback

I rejected this approach: *"This has decreased the readability and maintainability. The CSS using custom properties looks worse. Pulling out constants for our own selectors makes the code messier."*

We had a discussion about what actually deserves to be a constant. The conclusion: **not every literal value benefits from extraction**.

### The Revised Approach

We agreed to only extract constants that genuinely improve maintainability:

```javascript
// constants.js (final version)
const BUDDY_URL = 'https://www.nytimes.com/interactive/2023/upshot/spelling-bee-buddy.html';

// NYT page selectors - external dependencies that might break
const NYT_GAME_WRAPPER_SELECTOR = '#js-hook-game-wrapper';
const NYT_BUDDY_CONTAINER_SELECTOR = '.sb-buddy-container';
const NYT_GRID_SECTION_SELECTOR = '.the-square';
const NYT_TWO_LETTER_LIST_SELECTOR = '.the-square-part-two';

// Timing values - magic numbers that affect behaviour
const FALLBACK_VISIBILITY_TIMEOUT = 2000;

// Layout constants used in dynamic CSS generation
const MIN_SECTION_WIDTH = 300;
const SECTION_GAP = 10;
```

### What Stayed Inline

- Our own element IDs and classes (`'spelling-bee-buddy-container'`)
- Log message text (`'[Spelling Bee Buddy]'`)
- Static CSS values
- One-off strings

### The Key Insight

Extract constants when there's genuine benefit:

- **External dependencies** (NYT's selectors could change)
- **Values reused across files** (layout constants)
- **True magic numbers** (timing delays)

Don't extract when it hurts readability:

- **Self-documenting literals** (`'Spelling Bee Buddy'`)
- **Values used once** (most CSS properties)
- **Internal identifiers you control**

This was a valuable lesson in **thoughtful AI collaboration**—accepting suggestions that improve code, rejecting those that don't, and explaining why. The AI didn't get defensive; it learned from the feedback and produced a better solution.

### Unnecessary Comments

Another quirk of using an LLM such as Claude is its propensity to add comments liberally throughout the code. Claude is trained on vast amounts of JavaScript code, including examples with extensive inline documentation. This leads it to add comments even where the code is self-explanatory.

I eventually prompted Claude to remove unnecessary comments and keep only those explaining non-obvious logic. This is part of the broader pattern: LLMs inherit patterns from their training data, including legacy practices like IE backwards compatibility checks and over-commented code. The human's job is to recognize which inherited patterns add value and which are artifacts of the training corpus.

## Code Quality Improvements

Beyond removing unnecessary code and debating constants, several other quality improvements emerged throughout development:

### 1. Extract Constants

Magic numbers and external dependencies went into a shared constants file:

```javascript
// constants.js
const FALLBACK_VISIBILITY_TIMEOUT = 2000;
const BUDDY_URL = 'https://www.nytimes.com/interactive/2023/upshot/spelling-bee-buddy.html';

// NYT page selectors (external - prone to breaking)
const NYT_GAME_WRAPPER_SELECTOR = '#js-hook-game-wrapper';
const NYT_BUDDY_CONTAINER_SELECTOR = '.sb-buddy-container';
const NYT_GRID_SECTION_SELECTOR = '.the-square';
const NYT_TWO_LETTER_LIST_SELECTOR = '.the-square-part-two';

window.SPELLING_BEE_CONSTANTS = { /* ... */ };
```

This makes it easy to update if NYT changes their markup.

### 2. Self-Documenting Code

Instead of excessive comments, I extracted functionality into well-named functions:

```javascript
// Before:
// Wait for the game container to load
let checkCount = 0;
await new Promise((resolve) => {
  const check = () => {
    checkCount++;
    const el = document.querySelector('#js-hook-game-wrapper');
    if (el) resolve(); else requestAnimationFrame(check);
  };
  check();
});

// After:
const gameContainer = await waitForGameContainer();
```

### 3. Remove Dead Code

During refactoring, I eliminated:

- Empty CSS files
- Redundant validation checks
- Unnecessary function wrappers
- Duplicated constants

This reduced the codebase by ~36 lines while improving clarity.

With the code quality improved and the core functionality solid, attention turned to the user-facing details that make the extension feel polished.

## User Experience Touches

### 1. Clickable Title Link

The "Spelling Bee Buddy" header links to the full Buddy page:

```javascript
const link = document.createElement('a');
link.href = BUDDY_URL + (gameDate ? `?date=${gameDate}` : '');
link.target = '_blank';
link.rel = 'noopener noreferrer';
link.textContent = 'Spelling Bee Buddy';
```

Users can click to see the full Buddy page with all features.

### 2. Graceful Loading

The iframe starts hidden and reveals when content loads:

```javascript
iframe.style.visibility = 'hidden';

iframe.onload = () => {
  iframe.style.visibility = 'visible';
};

// Fallback timeout ensures iframe appears even if onload doesn't fire
setTimeout(() => {
  iframe.style.visibility = 'visible';
}, FALLBACK_VISIBILITY_TIMEOUT);
```

### 3. Error Handling

If the iframe fails to load, show a helpful message:

```javascript
iframe.onerror = () => {
  console.error('[Spelling Bee Buddy] Failed to load content.');
  const errorMessage = document.createElement('p');
  errorMessage.textContent = 'Failed to load Spelling Bee Buddy. Please check your connection and refresh.';
  errorMessage.style.color = '#d00';
  container.appendChild(errorMessage);
};
```

## Publishing and Platform Differences

With development complete, the final step was getting the extension published to the Firefox Add-ons (AMO) store. This process became its own learning experience in extension packaging requirements.

### The AMO Validation Journey

Publishing to Mozilla Add-ons (AMO) involved multiple rounds of validation fixes—each error revealing something new about browser extension requirements.

**Round 1: Version Format**

```
Error: "/browser_specific_settings/gecko/strict_min_version" must match pattern "^[0-9]{1,3}(\.[a-z0-9]+)+$"
```

The version string `"142.0"` was initially flagged as invalid, though the final code still uses this value successfully.

**Round 2: Icon Size Validation**

```
Warning: Expected icon at "icons/icon-48.png" to be 16 pixels wide but was 48.
```

The Chrome add-on validation caught that icon files must match their declared dimensions exactly. The manifest declared 16×16 and 32×32 icons but pointed to a 48×48 file. Solution: Generate exact sizes from the SVG source using the icon generation script.

**Round 3: Missing Content Script**

```
Error: Content script defined in the manifest could not be found at "iframe-content.js"
```

The build script wasn't including the new iframe content script! Updated `build.sh` to include it in both Firefox and Chrome packages.

**Round 4: Permissions Scope**

After reviewing the extension's actual needs, I tightened the permissions from `https://www.nytimes.com/*` to just the Spelling Bee pages:

```json
"permissions": [
  "https://www.nytimes.com/puzzles/spelling-bee*",
  "https://www.nytimes.com/interactive/*/upshot/spelling-bee-buddy.html*"
]
```

This follows the principle of least privilege and makes the extension's scope clearer to users during installation.

## Lessons Learned

### 1. Content Script Isolation Is Real
Content scripts cannot access page JavaScript variables like `window.gameData`. While you can bridge contexts with script injection + CustomEvents, it's often unnecessarily complex. Look for simpler alternatives first.

### 2. Log Everything During Development
Console logging at key points revealed:

- Which selector actually worked (eliminating dead selectors)
- How many times functions were being called (excessive MutationObserver triggers)
- Where the code was spending time unnecessarily
- Performance bottlenecks (10+ resize calls)

Strategic logging is essential for identifying unnecessary code.

### 3. Defensive Programming Can Make Code More Fragile
The instinct to handle every edge case led to:

- Multiple container selectors when only 1 ever matched
- Try-catch blocks with no actionable recovery
- Multiple layers of fallbacks for the same scenario
- Observers watching unnecessary DOM events

This defensive code doesn't just waste cycles—it makes the code more fragile in unintuitive ways by introducing modalities in behaviour. It also increases complexity, making the code harder to understand and maintain. Test in the actual environment, measure what actually happens, then remove the code that never executes.

### 4. Manifest V3 Isn't Universal
Despite being the "new standard," MV3 has significant implementation differences between browsers. For Firefox extensions, Manifest V2 still provides better permission handling.

### 5. Separate Content Scripts Beat iframe Manipulation
Running a content script inside the iframe is cleaner than external manipulation:

- No cross-origin issues
- Better timing control
- Cleaner code separation

### 6. The postMessage API Is Your Friend
For iframe-parent communication, postMessage provides:

- Type safety with defined message structures
- Origin validation for security
- Bidirectional communication when needed

### 7. Look for the Easy Solution First
Before parsing 49 script tags with regex, I should have checked the browser console to see if game data was already exposed as a global variable. Sometimes the simple solution is right there.

### 8. Know When to Disconnect Observers
MutationObserver and setInterval should almost always have a cleanup/disconnect strategy. Observers that run forever waste CPU cycles and can cause unexpected behaviour.

### 9. Build Scripts Enable Platform Optimization
A smart build script lets you maintain one codebase while delivering optimized packages for each browser.

## Designing the Bee Icon with AI

Since this is a Spelling Bee extension, I wanted a bee icon. Rather than finding stock graphics or hiring a designer, I asked Claude to design one in SVG format—a side quest that turned into an interesting study in collaborative generative work.

<div style="text-align: center;">
  <img src="{static}/images/icon-original.svg" width="128" alt="Original bee icon" style="display: inline-block; margin: 0 20px;"/>
  <span style="font-size: 2em; vertical-align: middle;">→</span>
  <img src="{static}/images/icon-final.svg" width="128" alt="Final bee icon" style="display: inline-block; margin: 0 20px;"/>
  <br/>
  <em>Icon evolution: from backwards wings to proper flight position</em>
</div>

### Initial Design

Claude generated an SVG featuring:

- A friendly bee with yellow body and black stripes
- Translucent blue wings
- Antennae and a smiling face
- A small stinger at the bottom
- Circular yellow background

```svg
<!-- Core bee body -->
<ellipse cx="64" cy="70" rx="24" ry="32" fill="#FFD54F"/>
<!-- Black stripes -->
<rect x="40" y="62" width="48" height="6" rx="3" fill="#212121"/>
```

### Iterative Refinement

The first version needed adjustments:

**Me:** "The bee's wings look like they are on backwards."

Claude repositioned the wings to extend from behind the body rather than in front, using SVG transformations to rotate them properly.

**Me:** "Can we flip the wings about the horizontal axis?"

Claude adjusted the rotation angles from -35° to +35°. Technically, rotating about the horizontal axis would mean negating the angle (from -35° to +35° is actually a rotation about the vertical), but the result looked good anyway, so I didn't correct the terminology.

### Mathematical Precision

The most interesting improvement came from a detail I noticed:

**Me:** "The lines across its abdomen don't perfectly align with the abdomen. Can we do some math to figure out what length each line should be?"

Claude calculated the exact stripe widths based on the ellipse equation. For a bee body centred at (*h*, *k*) with horizontal radius *a* and vertical radius *b*:

```
x = h ± a√(1 - ((y-k)/b)²)
```

This produced perfectly curved stripes:

- Top stripe (y=62): 47.4px wide
- Middle stripe (y=74): 46.8px wide
- Bottom stripe (y=86): 38.6px wide (narrowest, as the body tapers)

### The Transparency Bug Hunt

After generating the PNGs with ImageMagick, I noticed they had white backgrounds instead of transparency.

**Debugging Process:**

1. Claude checked the alpha channel: `Type: TrueColorAlpha` ✓
2. Read actual pixel values: `srgba(255,255,255,1)` - fully opaque white!
3. I realized the issue: **ImageMagick parameter order matters**

**The Fix:**

```bash
# Wrong - background applied after reading SVG
magick icon.svg -background none -resize 128x128 icon.png

# Correct - background applied before reading SVG
magick -background none icon.svg -resize 128x128 icon.png
```

With the correct parameter order: `srgba(0,0,0,0)` - fully transparent! *(Thanks to [xeruf on Stack Overflow](https://stackoverflow.com/questions/27538238/imagemagick-to-convert-svg-to-png-with-transparent-background#comment130711857_27538238).)*

### Automated Generation

Claude created `generate_icons.sh` to regenerate all sizes (48px, 96px, 128px) from the SVG source with proper transparency:

```bash
#!/bin/bash
echo "Generating icon-48.png..."
magick -background none icon.svg -resize 48x48 icon-48.png

echo "Generating icon-96.png..."
magick -background none icon.svg -resize 96x96 icon-96.png

echo "Generating icon-128.png..."
magick -background none icon.svg -resize 128x128 icon-128.png
```

This collaborative icon design showcased AI's strengths in generative work: quickly producing SVG code, applying mathematical transformations, and debugging technical issues. But human judgment was essential for aesthetic decisions and identifying root causes like the parameter order bug.

## Reflections on AI-Assisted Development

Building this extension with Claude Code revealed interesting patterns about human-AI collaboration in software development.

### What Claude Excelled At

**Systematic Exploration**
- Finding multiple container selectors via codebase search
- Analyzing beautified JavaScript to find the URL parameter support
- Reading pixel values to debug the transparency issue

**Pattern Recognition**
- Identifying duplicated constants across files
- Spotting excessive MutationObserver calls through console log analysis
- Recognizing when fallbacks never executed

**Rapid Iteration**
- Generating SVG code for the bee icon
- Applying ellipse mathematics for stripe alignment
- Creating build scripts and icon generators

**Research and Documentation**
- Analyzing beautified JavaScript to find URL parameter support
- Looking up AMO validation requirements
- Understanding Manifest V2 vs V3 differences

### Where Human Judgment Was Essential

**Architectural Decisions**
- Choosing dual manifests over compromising on permission handling
- Deciding when to use separate content scripts vs iframe manipulation
- Determining which constants actually improve maintainability

**Aesthetic and UX Calls**
- Icon wing orientation and overall visual appeal
- Side-by-side layout spacing ("the two could be a bit closer together")
- Whether the title link should have hover effects

**Recognizing Over-Engineering**
- Pushing back on excessive constant extraction
- Identifying when "cleaner" code is actually less readable
- Knowing when to stop optimizing

**Root Cause Identification**
- Realizing the ImageMagick parameter order issue
- Understanding that the 200-line dropdown manipulation was unnecessary
- Recognizing which selectors were actually dead code

### The Iterative Dance

The most effective pattern emerged:

1. Claude suggests an optimization or implementation
2. I evaluate the impact on readability and maintainability
3. Discussion if there are concerns
4. Refinement or rejection of the suggestion
5. Commit the improvements that genuinely help

This wasn't "AI writes code, human accepts it." It was genuine collaboration—Claude as a tireless pair programmer who:

- Never gets frustrated when suggestions are rejected
- Can instantly analyze megabytes of minified JavaScript
- Brings a different perspective on code organization
- Executes tedious refactoring without complaint

But who needs a human partner to:

- Make final calls on architecture and design
- Recognize when simpler is better
- Maintain the vision of what "good code" means for this project
- Know when the code is "done"

### The Meta-Lesson

The best code often emerges not from the first solution, but from iterative refinement. The date synchronization feature's evolution—from 200 lines of dropdown manipulation to discovering the URL parameter—demonstrates the value of:

- Trying approaches without ego attachment
- Failing fast and learning from each iteration
- Being willing to delete large amounts of code
- Always asking "is there a simpler way?"

Having an AI collaborator made it easier to explore these dead ends quickly. There's no embarrassment in saying "actually, let's delete all that and try something else" when your pair programmer is Claude.

## Final Architecture

```
┌─── Main Page (NYT Spelling Bee) ───────────────────────┐
│                                                         │
│  Content Script Context:                               │
│  content.js                                             │
│  ├─ Parse date from URL (/spelling-bee/YYYY-MM-DD)     │
│  ├─ Wait for game container (#js-hook-game-wrapper)    │
│  ├─ Create iframe with Buddy URL + ?date param         │
│  └─ Listen for postMessage resize events               │
│                                                         │
│  ┌─── iframe (Buddy Page) ──────────────────────────┐  │
│  │                                                   │  │
│  │  iframe-content.js                                │  │
│  │  ├─ Check if in iframe (not standalone)          │  │
│  │  ├─ Inject CSS to hide unwanted sections         │  │
│  │  ├─ Measure content height                       │  │
│  │  ├─ postMessage height to parent                 │  │
│  │  └─ ResizeObserver for ongoing updates           │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

Key Concepts:

- URL parsing for date extraction (simple regex)
- postMessage bridges iframe and parent for resize events
- Separate content scripts for main page vs iframe
- Each script is responsible for its own domain
```

## Conclusion

Building this browser extension with Claude Code taught lessons about both web extension development and AI-assisted software engineering.

### Technical Takeaways

**Modern web extension development requires:**

1. **Understanding JavaScript Contexts** - Content scripts live in an isolated world. While you can access page variables with script injection, simpler solutions (like URL parsing) are often better.

2. **Iterative Optimization** - Start with working code, then profile and eliminate waste. The journey from 200-line dropdown manipulation to simple URL parameters demonstrates the power of iteration.

3. **Browser-Specific Quirks** - MV2 vs MV3, permission handling differences, and varying API support mean platform-specific builds deliver the best user experience.

4. **Clean Architecture** - Proper separation of concerns (separate content scripts for main page vs iframe) prevents cross-origin headaches and keeps code maintainable.

5. **Ruthless Refactoring** - Question every fallback, every try-catch, every observer. If it never executes or provides no value, delete it.

### Development Process Insights

**AI-assisted development works best when:**

- The human maintains architectural vision and final judgment
- The AI handles systematic exploration and tireless iteration
- Both parties question suggestions and push back when needed
- There's no ego attached to deleting large amounts of code
- The focus stays on "does this actually improve the code?"

The final extension evolved from ~250 lines of defensive code to ~150 lines of focused, efficient JavaScript across 8 development sessions. It handles edge cases that actually occur, eliminates unnecessary work, and provides a seamless experience for NYT Spelling Bee players.

**Performance improvements:**

- Date synchronization: From 200+ lines of dropdown manipulation to simple URL regex
- MutationObserver calls: From 6+ redundant calls to proper disconnect logic
- iframe resize calls: From 10+ to 2
- Dead code eliminated: ~100 lines of fallbacks that never executed

The code is cleaner, faster, and easier to maintain—a reminder that sometimes the best code is the code you delete.

And sometimes the best way to write that code is with an AI pair programmer who can explore dead ends quickly, never gets frustrated with rejected suggestions, and helps you find the simple solution hiding beneath the complex one.

## Installation

Want to try the extension yourself? It's available for both Firefox and Chrome:

- **[Install on Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/spelling-bee-buddy-embedder/)** (Recommended - uses Manifest V2 with proper permissions)
- **Chrome Web Store** (Coming soon - pending review)
- **[Source code on GitHub](https://github.com/mmmorks/spelling-bee-buddy-extension)** - For manual installation or to contribute

## Resources

- [Source code on GitHub](https://github.com/mmmorks/spelling-bee-buddy-extension)
- [MDN Browser Extensions Guide](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions)
- [Chrome Extensions Documentation](https://developer.chrome.com/docs/extensions/)
- [Manifest V3 Migration Guide](https://extensionworkshop.com/documentation/develop/manifest-v3-migration-guide/)
