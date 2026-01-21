---
# mmmorks.net-ps9u
title: Evaluate use of callbacks and cross-references
status: completed
type: task
priority: normal
created_at: 2026-01-21T02:11:29Z
updated_at: 2026-01-21T02:32:27Z
parent: mmmorks.net-uuh4
---

Assess how well the post uses internal callbacks to reinforce its novel ideas.

## Key concepts that could benefit from callbacks
- The MUD interaction model (commands → textual feedback → persistent world)
- The Factorio throughput-over-correctness philosophy
- "Tending the invisible garden"
- The heresy/corruption spread concept
- The "slot machines" / dopamine loop observation
- The Paxos/Lamport meta-commentary on obtuse analogies
- The "factory must grow" refrain

## Areas to examine
- Are novel concepts introduced early and referenced later?
- Does the conclusion call back to ideas from earlier sections?
- Are there missed opportunities to connect ideas across sections?
- Does the Paxos warning in the intro get resolved/addressed later?
- Is the "factory must grow" ending earned by earlier content?

## Checklist
- [x] Map the novel concepts introduced in each section
- [x] Identify existing callbacks and cross-references
- [x] Note missed opportunities for callbacks
- [x] Evaluate whether callbacks feel natural vs forced
- [x] Check if the conclusion effectively ties threads together

## Findings

### Novel Concepts by Section ✓

**Introduction:**
- Gas Town project
- MUD-Factorio analogy (core thesis)
- Paxos/Lamport warning about obtuse analogies

**The MUD Layer:**
- MUD interaction model (commands → textual feedback → persistent world)
- Gas Town verbs and actors (polecats, witnesses, refineries, etc.)
- "You don't actually look at the code" - code as invisible world
- Blood on the Clocktower character metaphor

**The SimCity/Factorio Layer:**
- Zoning/automation paradigm
- Four Gas Town operations
- The Refinery as bottleneck manager
- Work as "uncountable substance" / throughput thinking
- "Don't watch your agents work" - Factorio discipline
- Yegge's "workers vs factory" distinction
- Ajit and Ryan story (transparency as bottleneck)
- "Slot machines" dopamine metaphor
- Brendan Hopper's "ant colony" quote

**The Synthesis:**
- Six properties of MUD-Factorio genre
- "Tending the invisible garden"
- Corruption/heresies spreading through system

**The Skill Transfer Question:**
- Who will be good at this (Factorio players, MUD wizards, etc.)
- "Slop fish into barrels" mentality
- "Programming has always been best-effort"

**The Dark Pattern:**
- Addiction loops
- Activity feed as dopamine drip
- "Not safe" - game wrecking your life, not just code

**What This Means:**
- "The factory must grow" refrain

### Existing Callbacks and Cross-References ✓

**Strong callbacks that work well:**

1. **"The factory must grow"** - First appears in Factorio Layer (line 65) in context of throughput thinking, then returns as the powerful final line (line 111). This is earned and effective.

2. **"Slot machines" metaphor** - Yegge quote in Factorio section (line 91), returns in Dark Pattern section as "you get to see where all your slot machines landed." Natural and reinforcing.

3. **"Slop fish into barrels"** - Introduced in Factorio section (line 43) as Yegge's description of work, returns in Skill Transfer (line 83) when discussing the mentality shift. Works well.

4. **MUD interaction model** - Introduced in MUD Layer (lines 22-24), implicitly referenced in Synthesis section (line 61) when discussing "Text as primary interface to complex state." Effective structural callback.

**Weak or one-off concepts (not callbacks, but notable):**

5. **"Workers vs factory"** - Yegge's key quote (line 47) establishes the paradigm difference. Not explicitly called back, but it underpins the entire argument. Could be stronger if referenced in conclusion.

6. **Blood on the Clocktower** - Single metaphor in MUD Layer (line 26). Works as illustration, doesn't need callback.

7. **Ajit and Ryan story** - Appears once in Factorio section (lines 49-50) to illustrate throughput velocity. Powerful example but never referenced again.

8. **Brendan Hopper's ant colony quote** - Appears once (line 51). Effective standalone, but could tie into conclusion about individual vs collective productivity.

### Missed Opportunities for Callbacks ✓

**Critical miss:**

1. **Paxos/Lamport warning (line 14)** - The intro raises a provocative meta-question: will the MUD aesthetic illuminate or obscure, like Lamport's obtuse Greek parliament framing? This is NEVER resolved in the conclusion. This is the biggest missed callback in the piece. The conclusion should explicitly answer: does the MUD-Factorio framing illuminate? (Based on the piece's argument, clearly yes.)

**Significant misses:**

2. **"Tending the invisible garden" (line 61)** - Beautiful phrase introduced in Synthesis section, never referenced again. Could tie into Dark Pattern section (are you tending a garden or feeding an addiction?) or conclusion (what does responsible garden-tending look like?).

3. **Corruption/heresies spreading (line 69)** - Fascinating concept about wrong patterns infecting the codebase. Never referenced in implications or conclusion. Could tie into the "not safe" warning—it's not just that chimps can wreck code, but that wrong ideas spread like disease.

4. **Ajit and Ryan transparency story (lines 49-50)** - Perfect illustration of throughput velocity creating new bottlenecks. Could callback in Dark Pattern section (velocity creates compulsion) or conclusion (organizational implications of this speed).

**Minor misses:**

5. **"Don't watch your agents work" (line 45)** - Yegge's explicit advice. Ties directly to Dark Pattern section's addiction warning (can't stop watching activity feed), but the connection isn't made explicit. The irony could be highlighted: you're advised not to watch, but the tool makes watching addictive.

6. **"Workers vs factory" distinction (line 47)** - Core paradigm shift. Could be referenced in conclusion when discussing implications for organizations or tool builders.

### Natural vs Forced Callbacks ✓

**Assessment: The existing callbacks feel natural and earned.**

The callbacks that do exist ("factory must grow," "slot machines," "slop fish") don't feel forced because:
- They're tied to concrete Yegge quotes, not just abstract concepts
- They serve dual purposes (establish concept + provide evidence)
- They return at moments where they add meaning, not just for symmetry

**Why this works:**
The piece doesn't do callbacks for callback's sake. When "the factory must grow" returns at the end, it's not just echoing earlier text—it's recontextualizing it. The first appearance (line 65) is about throughput as metric. The final appearance (line 111) is about who controls whom. Same phrase, different weight.

**Risk of adding more:**
Given that the existing callbacks are subtle and organic, adding heavy-handed callbacks could damage the piece's voice. Any additions should follow the same principle: return to a concept only when it gains new meaning in the new context, not just to remind readers it existed.

### Conclusion Thread-Tying ✓

**Partial success—some threads tied, others left hanging.**

**What the conclusion does well:**
- Final line ("The factory must grow. But you get to decide...") ties together the Factorio metaphor and addiction warning elegantly
- "What This Means" section provides practical implications for different audiences (tool builders, developers, organizations, everyone)
- Stays grounded—doesn't overpromise or get grandiose

**What threads are left hanging:**

1. **Paxos/Lamport meta-question (CRITICAL)** - The intro explicitly asks whether the MUD aesthetic will illuminate or obscure. The conclusion never answers this. Given the piece's entire argument is that the analogy IS illuminating, this should be stated.

2. **Heresies/corruption concept** - Introduced as a fascinating risk of the paradigm (wrong patterns spreading through the invisible codebase), but never appears in the "What This Means" implications. This is a significant oversight for tool builders and organizations.

3. **Skill transfer insight** - The provocative idea that traditional programmers might not be best at this gets airtime in its own section but doesn't tie into the conclusion's advice.

4. **Invisible garden metaphor** - Beautiful image that could anchor the conclusion's final advice about responsible use.

**Overall assessment:**
The conclusion is solid but incomplete. It successfully lands the Factorio-addiction connection, but leaves several rich conceptual threads dangling. The piece would be stronger if the conclusion explicitly acknowledged it has answered the Paxos question (yes, the analogy illuminates) and integrated the corruption/heresy risk into its implications.