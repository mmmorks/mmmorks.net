---
# mmmorks.net-dto4
title: Cross-check blog post against original Gas Town article
status: completed
type: task
priority: normal
created_at: 2026-01-21T00:16:22Z
updated_at: 2026-01-21T02:02:13Z
parent: mmmorks.net-k1qp
---

Review the blog post alongside Steve Yegge's original Gas Town article (markdown available in sources directory) to ensure:

- Accurate representation of Gas Town's features and concepts
- Correct terminology (polecats, refineries, witnesses, molecules, convoys, etc.)
- No mischaracterization of how the system works
- Proper attribution of Yegge's quotes and ideas
- Verify technical details like the tmux UI, Beads database, merge queue behavior

This is a fact-checking pass to make sure the MUD-Factorio analogy is built on solid ground and doesn't misrepresent the actual Gas Town implementation.

## Fact-Check Results

**Verified quotes and attributions:**
- ✓ "tending the invisible garden" - Gas Town Emergency Manual, correctly attributed
- ✓ "heresies" - Gas Town Emergency Manual, correctly attributed and explained
- ✓ "workers vs factory" - The Future of Coding Agents article, exact quote verified
- ✓ "don't watch your agents work" - Gas Town Emergency Manual: "Spend your time reading agent responses and giving them direction — not watching them work"
- ✓ "slot machines" - Gas Town Emergency Manual: "You get to see where all your slot machines landed"
- ✓ "slopping shiny fish into wooden barrels" - Welcome to Gas Town, exact quote verified

**Verified terminology:**
- ✓ Polecats - ephemeral per-rig workers
- ✓ Refinery - handles Merge Queue
- ✓ Witness - watches over polecats
- ✓ Deacon - daemon beacon, runs patrols
- ✓ Dogs - Deacon's helpers
- ✓ Molecules - workflows/chained beads
- ✓ Convoys - work-order/ticketing system
- ✓ Protomolecules - workflow templates
- ✓ Beads - atomic unit of work, Git-backed
- ✓ tmux UI - verified as primary UI

**All facts verified. Blog post accurately represents Gas Town concepts and quotes.**