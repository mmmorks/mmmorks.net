Title: Claude Code is a CLI Building Sim
Date: 2026-01-20
Category: Essays
Tags: ai, vibe-coding
Slug: vibe-coding-terminal-tycoon
Summary: The emerging paradigm of agentic coding tools represents an entirely new genre of interaction -- a building sim played through a text interface.

Claude Code is Anthropic's agentic coding tool -- a CLI where you describe what you want in natural language, and an AI agent writes the code, runs commands, and iterates on the results. You don't write code directly. You issue intents into a terminal and watch an agent execute them.

Something about this interaction feels different from other programming tools I've used. Not just faster or more convenient, but *categorically* different -- like the relationship between player and game has shifted.

Steve Yegge noticed the same thing. On New Year's Day 2026, he [announced](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) [Gas Town](https://github.com/steveyegge/gastown) -- an orchestration layer for running *multiple* Claude Code agents in parallel. As I read through its 25 pages of mad-scientist documentation, the framing clicked:

**Gas Town is a CLI building sim.**

[TOC]

## Clear as MUD

If you're old enough to remember MUDs -- Multi-User Dungeons, the CLI games that ruled the dialup era -- Gas Town might trigger some unexpected nostalgia.

For those who missed that era: A MUD is a text interface where you type commands and receive textual descriptions of a world with state, actors, and emergent behaviour. You issue `look` and get a room description. You issue `attack goblin` and combat unfolds. The world exists whether you're watching or not.

Gas Town works surprisingly similarly. The verbs are different -- `gt sling`, `gt seance`, `gt nudge`, `gt handoff` -- but the interaction model is almost identical. You're issuing commands into a persistent world populated by autonomous actors (Yegge's "polecats," "witnesses," "refineries") that continue operating when you look away.

The feedback loop is pure MUD: command, textual confirmation of state change, wait, check the activity feed to see what happened while you were away. Yegge's tmux UI is basically a split-screen MUD client showing multiple "rooms" (sessions) at once. The naming conventions reinforce this -- Polecats, the Refinery, the Witness, the Deacon, Dogs. These aren't abstractions. They're *characters* in a world, each with their own quirks and roles. You're playing a game where your party is made up of NPCs, each belonging to a distinct character class with persistent identities, and you're issuing them quests (molecules).

This heavy theming is a gamble. Leslie Lamport's "The Part-Time Parliament" introduced the Paxos consensus algorithm through an elaborate fictional Greek parliament -- and the narrative was so obtuse that the algorithm went ignored for nearly two decades until Lamport published a stripped-down "Paxos Made Simple" version. Yegge is betting the opposite: that MUD aesthetics *illuminate* rather than obscure. I think he's right -- but only for readers already fluent in the idiom. If you've played MUDs or automation games, "sling a convoy of molecules to the refinery" immediately evokes the right mental model: queued work, bottlenecks, autonomous processing. If you haven't, it's as opaque as Lamport's Byzantine legislators. The difference is that Yegge's target audience -- developers already drawn to CLI tools and automation -- skews heavily toward people who *have* played these games.

The key difference: **you don't actually look at the code.** Just like in a MUD, you don't get to peek behind the curtain and inspect the room data structures directly. Your entire interaction with the codebase is mediated through agent windows: you issue commands, read their responses, check status dashboards. The code is as invisible to you as the MUD server's memory was. Your reality is constructed entirely from text that agents feed you.

## The Building Sim Layer

In Factorio, you don't craft iron plates by hand (after the first few minutes) -- you lay down miners, furnaces, and belts, and let the factory run. It's the same mindset as SimCity or RollerCoaster Tycoon: you're designing systems, not executing individual actions.

Gas Town is exactly this. You're not writing code. You're:

1. **Designing protomolecules** -- pre-configured workflow templates you can stamp down, like zoning districts in SimCity or blueprint books in Factorio.
2. **Cooking formulas** -- a macro expansion phase, like setting up ride pricing rules in RollerCoaster Tycoon.
3. **Slinging convoys** -- placing a module and letting it run, like dropping a power plant and watching the grid light up.
4. **Watching dashboards** -- the Charmbracelet TUI is your city overview screen, showing what's thriving and what's backed up.

The **Refinery** is the bottleneck manager -- the equivalent of that one belt in Factorio where everything has to merge before reaching your central production line. Merge Queue problems are *throughput problems*, not logic problems.

Yegge describes work as "an uncountable substance that you sling around freely, like slopping shiny fish into wooden barrels at the docks. Most work gets done; some work gets lost." This is building sim thinking. You don't care about individual guests or iron plates. You care about flow *per minute*. Throughput over correctness-per-item.

And crucially: **don't watch your agents work.** Yegge's advice is explicit -- give them marching orders, let them run, then read their output when they're done. "Spend your time reading agent responses and giving them direction -- not watching them work." This is building sim discipline. You don't watch individual Sims commute to work. You go zone the next neighbourhood.

Yegge himself validates this framing explicitly: "coding agent shops are going to wake up, realize that they have built workers when I've built a factory." Workers execute tasks. Factories process throughput. The distinction is architectural, not incremental.

Yegge cites an early example: Ajit and Ryan, two ex-Amazon devs using coding agents, moved so fast their teammates couldn't keep up. "2 hours ago!? That's ancient!" became an actual complaint. They had to develop explicit rules: "everything you do has to be 100% transparent and announced, all the time." This is what throughput-over-correctness looks like in practice -- you move so fast that *transparency becomes the bottleneck*, not code quality.

As Brendan Hopper told Yegge in his [follow-up article](https://steve-yegge.medium.com/the-future-of-coding-agents-e9451a84207c): "when work needs to be done, nature prefers colonies. Nature builds ant colonies, while Claude Code is the world's biggest fuckin' ant." The metaphor emphasizes deploying many workers in coordination, not making one worker smarter.

## The Terminal Tycoon Genre

What I think we're seeing is an emergent genre that doesn't have a good name yet. Let's call it **Terminal Tycoon**.

The genre has a core loop: you issue declarative intents, autonomous agents execute them, and you observe outcomes through text. But what makes it a *genre* rather than just a tool category is how these properties reinforce each other to create a distinct mode of interaction.

**Declarative intent, emergent execution.** You describe what you want (design molecule, sling convoy, lay out mining outpost) and autonomous agents figure out the how. You observe outcomes, not processes. This is the foundation -- without it, you're just using a fancy command line.

**Text as primary interface to complex state.** You can't see the factory floor -- and in true agentic development, you don't look at the code directly either. Your entire perception of the system comes through agent reports, activity feeds, status lines, and dashboard summaries. Like a MUD where you never see the actual room data structures, the codebase exists "behind the curtain" while you interact with it purely through textual descriptions. Yegge calls this "tending the invisible garden" -- you do regular sweeps (code review, then bug fixes, then more code review), hoping that most of the time you don't find anything bad. The only way to be sure is to keep doing it.

**Persistent world with ephemeral actors.** The Beads database is like your city or theme park -- it persists. The polecats are like construction crews or maintenance staff -- they come and go, but the infrastructure remains. This separation matters because it means you're building something that outlasts any individual session.

**Throughput as the core metric.** Not correctness-per-task, but *flow*. Some fish escape, some bugs get fixed three times, but the factory must grow. Once you accept this, you stop optimizing for perfection and start optimizing for velocity -- which changes everything about how you work.

**Debugging becomes systems thinking.** You're not stepping through code. You're asking "why is the Refinery backed up?" or "why isn't the Deacon nudging this worker?" You're tuning a simulation. This follows naturally from the text-mediated interface -- when you can't inspect directly, you reason about behaviour from observable symptoms.

**Corruption spreads through the system.** Yegge calls them "heresies" -- wrong guesses that agents make about how things work, which get enshrined in code and propagate to other agents. Like a SimCity traffic pattern that gridlocks because you zoned industry wrong three hours ago, or a MUD where a false rumor becomes canonical lore, bad patterns infect your invisible codebase and have to be "sniffed out and eradicated." This is the cost of throughput-over-correctness: errors compound rather than staying isolated.

## Who Will Be Good At This?

If this genre is real, then the people who thrive at agentic orchestration might not be the best traditional programmers. They might be Factorio megabase builders who understand throughput and bottlenecks. MUD wizards who built complex world systems with text commands and triggers. Ops and SRE folks who already think in terms of observability, alerts, and self-healing systems.

The skill isn't "coding" in the traditional sense. It's **workflow architecture** + **simulation intuition** + **comfort with text as interface**.

This might explain a pattern I've noticed anecdotally: some senior engineers struggle with vibe coding while some less-experienced developers take to it naturally. I don't have data on this -- it's a hypothesis based on conversations and observations, not a study. But the mechanism is plausible. If you've spent 20 years optimizing your ability to write precise, correct code, the "slop fish into barrels" mentality feels wrong. Your hard-won instincts actively fight the paradigm. But if you grew up building systems that run without you -- whether that's Factorio factories, Kubernetes clusters, or Discord bots -- the mental model transfers directly.

You might worry this sounds like embracing sloppiness. But most commercial software development has *always* been a best-effort, we'll-fix-it-later endeavor. We've always shipped with bugs. The question has always been: how close is it? How good are your tests? Vibe coding makes explicit what was always implicit in the craft. The difference is scale and velocity.

## The Addictive Loop

If the Terminal Tycoon analogy holds, though, there's a darker parallel worth examining.

One thing building sims are notorious for is *addiction*. The "one more belt" / "one more quest" / "just check the activity feed" loop.

Gas Town seems primed for this. The activity feed is a dopamine drip. Convoys landing is XP. Yegge himself describes cycling through workers to check their results: "Then we get to the fun part. You get to see where all your slot machines landed." The constant need to "keep feeding the engine" means you never feel *done*. When Yegge mentions needing a third Claude Code account by end of week, the real issue is the *compulsion* to keep the factory running, not the cost.

This might be the real reason Gas Town "is not safe" for most people. Autonomous agents can wreck your codebase -- but the *game* can wreck your life.

I don't think Gas Town specifically will be how we all code in two years. Yegge himself says it might not live longer than 12 months. But the *paradigm* -- the Terminal Tycoon genre -- feels like a genuine discovery about how humans can effectively direct swarms of AI agents. The metaphor isn't decoration -- it captures something essential about the interaction model that a dry technical description would miss.

If this framing is right, it suggests the interface matters more than the underlying AI. A MUD with great verbs and clear world-state reporting might outperform a fancy GUI that hides the simulation. It also suggests that the people who thrive in this paradigm won't necessarily be your best coders -- they might be your best project managers, your ops people, or that one weird employee who has 2000 hours in automation games.

And if you want to get good at this? Go play building sims. Seriously. Build a megabase in Factorio, a megacity in SimCity. Learn to think in throughput. Get comfortable with "good enough" flow rather than perfect placement.

But pay attention to the addiction mechanics. If you find yourself unable to stop watching the activity feed, that's not a feature -- that's a bug in your relationship to the tool.

The factory must grow. But you still get to decide whether you're running it, or whether it's running you.
