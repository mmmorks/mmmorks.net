Title: Vibe Coding is a MUD Version of Factorio
Date: 2026-01-20
Category: Articles
Tags: ai, software-development, vibe-coding, agents
Slug: vibe-coding-mud-factorio
Summary: The emerging paradigm of agentic coding tools like Gas Town represents an entirely new genre of interaction -- think Factorio played through a text adventure interface.

Steve Yegge [announced](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) his [Gas Town project](https://github.com/steveyegge/gastown) on New Year's Day 2026, and reading through its 25 pages of mad-scientist documentation, I kept circling back to an analogy that felt more right the longer I sat with it:

**Vibe coding is a MUD version of Factorio.**

(There's a risk here, by the way, wrapping technical insights in playful narrative can backfire spectacularly. Leslie Lamport's "The Part-Time Parliament" paper introduced the Paxos algorithm through such an obtuse fictional Greek parliament story that it took two decades before anyone understood or used it. Yegge's betting the opposite: that the MUD aesthetic *illuminates* rather than obscures. We'll see.)

[TOC]

## The MUD Layer

If you're old enough to remember Multi-User Dungeons -- those text-based virtual worlds from the dialup era -- Gas Town might trigger some unexpected nostalgia.

For those who missed that era: A MUD is a text interface where you type commands and receive textual descriptions of a world with state, actors, and emergent behaviour. You issue `look` and get a room description. You issue `attack goblin` and combat unfolds. The world exists whether you're watching or not.

Gas Town works surprisingly similarly. The verbs are different -- `gt sling`, `gt seance`, `gt nudge`, `gt handoff` -- but the interaction model is almost identical. You're issuing commands into a persistent world populated by autonomous actors (Yegge's "polecats," "witnesses," "refineries") that continue operating when you look away.

The feedback loop is pure MUD: command, textual confirmation of state change, wait, check the activity feed to see what happened while you were away. Yegge's tmux UI is basically a split-screen MUD client showing multiple "rooms" (sessions) at once. The naming conventions reinforce this -- Polecats, the Refinery, the Witness, the Deacon, Dogs. These aren't abstractions. They're *characters* in a world -- like the Drunk, the Poisoner, and the Baron in Blood on the Clocktower, each with their own quirks and roles. You're playing a game where your party is made up of NPCs, each belonging to a distinct character class with persistent identities, and you're issuing them quests (molecules).

The key difference: **you don't actually look at the code.** Just like in a MUD, you don't get to peek behind the curtain and inspect the room data structures directly. Your entire interaction with the codebase is mediated through agent windows, you issue commands, read their responses, check status dashboards. The code is as invisible to you as the MUD server's memory was. Your reality is constructed entirely from text that agents feed you.

## The Factorio Layer

In Factorio, you don't craft iron plates by hand (after the first few minutes) -- you lay down miners, furnaces, and belts, and let the factory run. It's the same mindset as SimCity or RollerCoaster Tycoon: you're designing systems, not executing individual actions.

Gas Town is exactly this. You're not writing code. You're:

1. **Designing protomolecules** -- these are like blueprint books in Factorio. Pre-configured workflow templates you can stamp down.
2. **Cooking formulas** -- a macro expansion phase, similar to Factorio's circuit network logic.
3. **Slinging convoys** -- this is placing a factory module and letting inserters do the work.
4. **Watching dashboards** -- the Charmbracelet TUI with expanding trees is your Factorio production graph.

The **Refinery** is the bottleneck manager -- the equivalent of the one belt that everything has to merge through before hitting the main bus. Merge Queue problems are *throughput problems*, not logic problems.

Yegge describes work as "an uncountable substance that you sling around freely, like slopping shiny fish into wooden barrels at the docks. Most work gets done; some work gets lost." This is Factorio thinking. You don't care about individual iron plates. You care about iron plates *per minute*. Throughput over correctness-per-item.

And crucially: **don't watch your agents work.** Yegge's advice is explicit -- give them marching orders, let them run, then read their output when they're done. "Spend your time reading agent responses and giving them direction -- not watching them work." This is exactly Factorio discipline. You don't stare at the smelting array. You go design the next production line.

Yegge himself validates this framing explicitly: "coding agent shops are going to wake up, realize that they have built workers when I've built a factory." Workers execute tasks. Factories process throughput. The distinction is architectural, not incremental.

Yegge cites an early example: Ajit and Ryan, two ex-Amazon devs using coding agents, moved so fast their teammates couldn't keep up. "2 hours ago!? That's ancient!" became an actual complaint. They had to develop explicit rules: "everything you do has to be 100% transparent and announced, all the time." This is what throughput-over-correctness looks like in practice -- you move so fast that *transparency becomes the bottleneck*, not code quality.

As Brendan Hopper told Yegge in his [follow-up article](https://steve-yegge.medium.com/the-future-of-coding-agents-e9451a84207c): "when work needs to be done, nature prefers colonies. Nature builds ant colonies, while Claude Code is the world's biggest fuckin' ant." The metaphor isn't about making one worker smarter -- it's about deploying many workers in coordination.

## The Synthesis: FactorioMUD as Genre

What I think we're seeing is an emergent genre that doesn't have a good name yet.

**FactorioMUD** (or maybe "Code Tycoon"?) has these properties:

1. **Declarative intent, emergent execution.** You describe what you want (design molecule, sling convoy, lay out mining outpost) and autonomous agents figure out the how. You observe outcomes, not processes.

2. **Text as primary interface to complex state.** You can't see the factory floor -- and in true agentic development, you don't look at the code directly either. Your entire perception of the system comes through agent reports, activity feeds, status lines, and dashboard summaries. Like a MUD where you never see the actual room data structures, the codebase exists "behind the curtain" while you interact with it purely through textual descriptions. Yegge calls this "tending the invisible garden" -- you do regular sweeps (code review, then bug fixes, then more code review), hoping that most of the time you don't find anything bad. The only way to be sure is to keep doing it.

3. **Persistent world with ephemeral actors.** The Beads database is like the Factorio map -- it persists. The polecats are like construction bots -- they come and go, but the infrastructure remains.

4. **Throughput as the core metric.** Not correctness-per-task, but *flow*. Some fish escape, some bugs get fixed three times, but the factory must grow.

5. **Debugging becomes systems thinking.** You're not stepping through code. You're asking "why is the Refinery backed up?" or "why isn't the Deacon nudging this worker?" You're tuning a simulation.

6. **Corruption spreads through the system.** Yegge calls them "heresies" -- wrong guesses that agents make about how things work, which get enshrined in code and propagate to other agents. Like a Factorio factory that starts producing the wrong intermediate product, or a MUD where a false rumor becomes canonical lore, bad patterns infect your invisible codebase and have to be "sniffed out and eradicated."

## Who Will Be Good At This?

If this genre is real, then the people who will be *best* at agentic orchestration might not be the best traditional programmers. They might be:

- **Factorio megabase builders** who understand throughput, bottlenecks, and ratio optimization
- **Dwarf Fortress players** who are comfortable with emergent chaos and text-based situational awareness
- **MUD wizards** who built complex world systems with text commands and triggers
- **Excel power users** who think in terms of formulas propagating through dependency graphs
- **Ops/SRE folks** who already think in terms of observability, alerts, and self-healing systems

The skill isn't "coding" in the traditional sense. It's **workflow architecture** + **simulation intuition** + **comfort with text as interface**.

This might explain why some senior engineers struggle with vibe coding while some less-experienced developers take to it naturally. If you've spent 20 years optimizing your ability to write precise, correct code, the "slop fish into barrels" mentality feels wrong. But if you grew up on automation games where the whole point is building systems that run without you, the mental model transfers directly.

You might worry this sounds like embracing sloppiness. But most commercial software development has *always* been a best-effort, we'll-fix-it-later endeavor. We've always shipped with bugs. The question has always been: how close is it? How good are your tests? Vibe coding isn't introducing sloppiness to a previously pristine craft -- it's making explicit what was always implicit. The difference is scale and velocity.

## The Addictive Loop

If the FactorioMUD analogy holds, though, there's a darker parallel worth examining.

One thing both Factorio and MUDs are notorious for is *addiction*. The "one more belt" / "one more quest" / "just check the activity feed" loop.

Gas Town seems primed for this. The activity feed is a dopamine drip. Convoys landing is XP. Yegge himself describes cycling through workers to check their results: "Then we get to the fun part. You get to see where all your slot machines landed." The constant need to "keep feeding the engine" means you never feel *done*. When Yegge mentions needing a third Claude Code account by end of week, the real issue is the *compulsion* to keep the factory running, not the cost.

This might be the real reason Gas Town "is not safe" for most people. Autonomous agents can wreck your codebase -- but the *game* can wreck your life.

I don't think Gas Town specifically will be how we all code in two years. Yegge himself says it might not live longer than 12 months. But the *paradigm* -- the FactorioMUD genre -- feels like a genuine discovery about how humans can effectively direct swarms of AI agents.

Unlike Lamport's Paxos paper, where the Greek parliament narrative obscured the algorithm for two decades, Yegge's MUD aesthetic seems to illuminate rather than obscure. The metaphor isn't decoration -- it captures something essential about the interaction model that a dry technical description would miss.

The implications:

**For tool builders:** The interface matters more than the AI. A MUD with great verbs and clear world-state reporting might outperform a fancy GUI that hides the simulation.

**For developers:** If you want to get good at this, go play Factorio. Seriously. Build a megabase. Learn to think in throughput. Get comfortable with "good enough" item flow rather than perfect item placement.

**For organizations:** The people who are good at this won't necessarily be your best coders. They might be your best project managers, your ops people, or that one weird employee who has 2000 hours in automation games.

**For everyone:** Pay attention to the addiction mechanics. If you find yourself unable to stop watching the activity feed, that's not a feature -- that's a bug in your relationship to the tool.

---

## A Warfare Parallel

There's a parallel here that keeps nagging at me: modern warfare.

Over the past decade, drone operators have become some of the most effective combatants in contemporary conflicts. And the skills that make a good drone pilot turn out to be... not what you'd expect. Not the physical conditioning of special forces, not years of flight school, but pattern recognition, situational awareness from multiple screens, comfort with controller interfaces. The [Air Force and Space Force now actively recruit from gaming communities](https://airforcegaming.com/). The skills of an FPS player -- tracking multiple targets, making split-second decisions from abstracted representations of reality -- transfer better to drone warfare than traditional combat training.

Is something similar happening to software development?

The argument of this essay, if I'm being honest with myself, isn't just that Factorio skills *help* with vibe coding. It's a more uncomfortable suggestion: that the skills which made someone a great traditional programmer -- meticulous attention to syntax, deep knowledge of language internals, the ability to hold complex state in your head and manipulate it precisely -- might matter less than the ability to think in systems, manage throughput, and stay comfortable when you can't see what's actually happening.

There's another gaming skill that might matter even more: reading the meta.

In competitive games, the "meta" is the current landscape of optimal strategies -- what works, what counters what, what's fallen out of favour. It shifts constantly as patches land, new techniques emerge, and counter-strategies develop. The players who succeed long-term aren't those who perfect one approach and stick with it. They're the ones who sense when the meta is shifting and adapt before everyone else catches on.

The AI tooling landscape has this quality. What's optimal today -- the specific agents, workflows, prompt patterns -- might be obsolete in six months. Gas Town itself might not outlive the year. The skill isn't mastering *this* tool; it's developing intuition for how the whole space is evolving and repositioning accordingly. That's not a traditional engineering skill. It's a competitive gaming skill.

If all this is true, we might be watching a shift as dramatic as the one from cavalry to tanks, or from dogfighting to drones. Not a gradual evolution where old skills remain valuable, but a genuine discontinuity where the new masters come from unexpected places.

But here's the uncomfortable flip side: if the interface is a game, it inherits gaming's darker patterns too. The same Factorio instincts that help you think in throughput also make you susceptible to "one more belt." The same competitive drive that helps you read the meta keeps you grinding when you should step away. The people most naturally suited to this paradigm might also be the most vulnerable to its compulsive loops -- the activity feed as endless dopamine drip, convoys landing like slot machine payouts.

I don't know if any of this is right. The parallels might be too cute -- warfare and software development are different in fundamental ways, and the gaming comparisons could be misleading us. Traditional programming skills surely still matter *somewhere* in the stack. Someone has to build the agents, train the models, debug the infrastructure.

But the question feels worth asking: In five years, will the best "developers" be people who never learned to program in the traditional sense -- but who know how to read a meta, think in throughput, and manage systems they can't directly see?

The factory must grow. But you still get to decide whether you're running it, or whether it's running you.
