---
# mmmorks.net-h21x
title: Identify clichés and AI text tropes
status: completed
type: task
priority: normal
created_at: 2026-01-21T02:11:21Z
updated_at: 2026-01-21T02:34:42Z
parent: mmmorks.net-uuh4
---

Hunt for tired phrases, clichés, and patterns commonly seen in AI-generated text.

## Common AI text tropes to watch for
- "That's not X. That's Y." constructions
- "Here's the thing:" or "Here's where it gets interesting"
- "Let me be clear" / "To be clear"
- "In other words"
- Overuse of "crucially," "importantly," "fundamentally"
- "X isn't just Y—it's Z"
- Unnecessary hedging ("I think," "it seems," "might be")
- Listicles that feel formulaic
- Overly balanced "on the one hand / on the other hand" structures
- Starting sentences with "And" or "But" excessively
- "The real question is..."
- "What does this mean for..."

## General clichés to flag
- "Game-changer"
- "At the end of the day"
- "Moving forward"
- "Best of both worlds"
- Any phrase that feels like it could be in a LinkedIn post

## Checklist
- [x] Scan for AI text trope patterns
- [x] Flag clichéd phrases
- [x] Note any passages that feel "generated" rather than authored
- [x] Suggest alternatives where possible

## Findings

### AI Text Trope Patterns ✓

**Definite AI tropes found:**

1. **"Here's where it gets interesting" (line 32)** - Classic AI transition phrase. Tells rather than shows. This is a clear match to the trope list.
   - Suggested fix: Start directly with the content: "In SimCity, you don't build houses..." or bridge with a more specific observation.

2. **"Here's the thing, though:" (line 85)** - Another "here's" construction. Very AI-ish.
   - Context: "Here's the thing, though: programming has *always* been a best-effort, we'll-fix-shit-later endeavor."
   - The content is good, but the introduction is generic.
   - Suggested fix: Cut the phrase entirely and start with "Programming has always been..."

3. **"What This Means" (line 96, section header)** - Matches "What does this mean for..." trope.
   - This one is borderline—it's a clear structural signal for readers. May be worth keeping despite being formulaic.
   - Suggested alternative: "Implications" or "Taking This Forward"

**Borderline cases (AI-adjacent but defensible):**

4. **"And here's the crucial part:" (line 27)** - "And" + "here's" + "crucial" is a triple AI signal.
   - However, the emphatic announcement works rhetorically to highlight the key insight about not looking at code.
   - The content that follows is strong and specific, not generic.
   - Verdict: Worth reconsidering but not egregious.

5. **"Let me try to characterize it:" (line 56)** - "Let me" construction can feel AI-ish.
   - However, this is explicitly meta—the piece is attempting to define a new genre.
   - The self-awareness about the attempt ("try to") actually works.
   - Verdict: Keep.

6. **"What I think we're seeing" (line 55)** - Hedging + "what we're seeing" formula.
   - But this is presenting a novel thesis, so some hedging is intellectually honest.
   - Verdict: Keep.

**Pattern NOT matching but worth noting:**

7. **"Not metaphorically. Structurally." (line 12)** - Matches "Not X. Y." pattern.
   - But this is a strong rhetorical choice, not generic filler.
   - The staccato emphasis serves the argument.
   - Verdict: This is good writing, not AI slop.

8. **"isn't just 'AI-assisted development'—it's an entirely new genre" (line 6)** - Matches "X isn't just Y—it's Z" pattern.
   - But this is THE CORE THESIS stated in the summary.
   - Verdict: Keep.

### Clichéd Phrases ✓

**Good news: The piece is remarkably cliché-free.**

Checked for:
- "Game-changer" - Not found ✓
- "At the end of the day" - Not found ✓
- "Moving forward" - Not found ✓
- "Best of both worlds" - Not found ✓
- "Paradigm shift" - Not found (though "paradigm" appears in context of discussing an actual paradigm)
- "Low-hanging fruit" - Not found ✓
- "Think outside the box" - Not found ✓
- "Synergy" - Not found ✓

**One borderline business-speak phrase:**
- **"The factory must grow"** (lines 65, 111) - This is actually a Factorio meme/in-joke, not a cliché. It's contextually appropriate and the audience will recognize it.

**Overall assessment:**
The piece has a strong, distinct voice that avoids corporate/business clichés. The language is concrete and specific rather than abstract and buzzwordy. Most phrases are either:
- Direct quotes from Yegge
- Specific technical/gaming terminology (MUD, Factorio, tmux, polecats)
- Fresh metaphors ("slop fish into barrels," "tending the invisible garden")

The writing doesn't feel like it could be a LinkedIn post—it's too weird, too specific, and too opinionated.

### Passages That Feel "Generated" vs Authored ✓

**Overall verdict: This piece has a strong authorial voice. Very little feels AI-generated.**

**What makes it feel authored:**
- Specific references and deep knowledge (Blood on the Clocktower, Dwarf Fortress, Factorio mechanics, tmux)
- Opinionated asides and parentheticals (the Lamport/Paxos digression, "chimps can wreck your shit")
- Willingness to use informal language ("mad-scientist documentation," "wreck your life," "biggest fuckin' ant")
- Personal interpretation ("kept circling back to an analogy," "I think we're seeing")
- Meta-awareness about the writing itself (the Paxos risk acknowledgment)

**Sections that feel most "generated" or formulaic:**

1. **The Synthesis section's 6 enumerated properties (lines 58-69)** - This is the most list-like, taxonomic part of the piece. It reads like a structured categorization rather than flowing prose.
   - However, this might be intentional—defining a genre requires systematic enumeration.
   - The properties themselves are specific and thoughtful, not generic.
   - Verdict: Formulaic by design, not by accident.

2. **"What This Means" implications section (lines 96-108)** - Bullet-pointed takeaways for different audiences.
   - This has a "how-to" / "takeaways" structure common in AI-generated content.
   - But the advice is specific and actionable, not generic platitudes.
   - "Go play Factorio. Seriously. Build a megabase." is NOT something AI would write.
   - Verdict: Structured for clarity, but still has authorial voice.

**What's NOT generic:**
The piece never falls into the AI trap of restating obvious things in different words. Every section advances the argument. Even the recap-style moments (Synthesis, What This Means) add new insights rather than just summarizing.

**Authenticity markers:**
- Casual profanity ("biggest fuckin' ant")
- Genuine uncertainty ("We'll see," "might not live longer than 12 months")
- Specific, checkable claims (Ajit and Ryan story, Yegge quotes)
- The willingness to end on a cautionary note rather than unbridled optimism

### Suggested Alternatives ✓

**Priority fixes (definite AI tropes):**

1. **Line 32: "Here's where it gets interesting."**
   - Current: "## The SimCity/Factorio Layer\n\nHere's where it gets interesting. In SimCity, you don't build houses..."
   - Option A: "## The SimCity/Factorio Layer\n\nIn SimCity, you don't build houses..."
   - Option B: "## The SimCity/Factorio Layer\n\nThe MUD provides the interface. But the mental model is something else entirely. In SimCity, you don't build houses..."
   - Recommended: **Option A** (cleanest)

2. **Line 85: "Here's the thing, though:"**
   - Current: "Here's the thing, though: programming has *always* been a best-effort, we'll-fix-shit-later endeavor."
   - Suggested: "Programming has *always* been a best-effort, we'll-fix-shit-later endeavor."
   - Recommended: **Cut the phrase entirely.** The content is strong enough to stand alone.

3. **Line 96: "What This Means" (section header)**
   - Current: "## What This Means"
   - Option A: "## Implications"
   - Option B: "## What Now?"
   - Option C: Keep it (it's functional even if formulaic)
   - Recommended: **Option A** (more professional while staying direct)

**Optional consideration:**

4. **Line 27: "And here's the crucial part:"**
   - Current: "And here's the crucial part: **you don't actually look at the code.**"
   - Option A: "The crucial part: **you don't actually look at the code.**"
   - Option B: "But the defining characteristic of true agentic development: **you don't actually look at the code.**"
   - Option C: Keep it (the emphasis works rhetorically)
   - Recommended: **Option C** (or Option A if you want to minimize AI feel)

**Summary:**
Three definite AI tropes to fix. The piece is otherwise remarkably clean. Fixing these three instances would eliminate the most obvious AI fingerprints while preserving the strong authorial voice.