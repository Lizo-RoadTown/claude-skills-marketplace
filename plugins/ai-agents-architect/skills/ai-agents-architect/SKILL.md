---
name: ai-agents-architect
description: A decision framework for autonomous-agent architecture. Helps decide where on the autonomy spectrum the agent sits (suggester, assistant, operator, autonomous), pick a loop pattern (ReAct, Plan-and-Execute, Tree-of-Thoughts), choose between single-agent and multi-agent designs, and decide when to introduce an orchestrator. Use when designing a new agent app, diagnosing stuck or drifting agents, or considering whether to split an agent into multiple. Refuses tool overload, infinite tool loops without a cap, and multi-agent splits without a real reason.
license: Apache-2.0
compatibility: Agent Skills compatible (Claude Code, Cursor, Gemini CLI, OpenCode, and others — see agentskills.io/clients)
metadata:
  author: Liz Osborn
  version: "0.1.0"
  homepage: "https://github.com/Lizo-RoadTown/claude-skills-marketplace"
---

# AI Agents Architect

A decision-framework skill for autonomous-agent architecture. Use this skill
when the task touches:

- Designing a new agent app or service
- Deciding between single-agent and multi-agent structures
- Picking between ReAct, Plan-and-Execute, and other agent loops
- Deciding when (and whether) to introduce an orchestrator
- Diagnosing why an agent is stuck in loops, drifting, or over-spending tokens

---

## Step 1 — Decide how much autonomy

Before picking architecture, decide where the agent sits on the **autonomy
spectrum**:

| Level | Description | Architectural needs |
|---|---|---|
| **Suggester** | Proposes actions; user approves each one | Stateless single call; simple |
| **Assistant** | Acts within tight rails; reports back | Most current AI apps live here |
| **Operator** | Multi-step action with checkpoints | Robust error handling, retry logic |
| **Autonomous** | Runs unsupervised on goals; escalates exceptions only | Hard guardrails, memory, observability, kill switches |

Each level needs different architecture. **Get this wrong and the project
fights itself.** A suggester doesn't need a memory layer; an autonomous agent
without one is unsafe.

---

## Step 2 — Pick the loop pattern

Three reference patterns. Pick deliberately — don't default.

### ReAct (Reason + Act)

On each turn: **reason** about what to do next → **act** by calling a tool →
**observe** the result → repeat until done or budget exhausted.

- **Good for:** tasks where the right next step depends on what just happened
- **Watch for:** infinite loops, getting stuck on sub-problems
- **Required:** iteration cap, escape valve

### Plan-and-Execute

Two phases: agent produces a complete **plan** (a list of steps), then
**executes** each step. Optionally re-plans if a step fails.

- **Good for:** tasks with knowable shape — research jobs, ETL pipelines, multi-step transformations
- **Watch for:** brittle plans that go stale during execution
- **Required:** ability to detect "the plan no longer matches reality"

### Tree-of-Thoughts / Explore-and-Backtrack

Agent explores **several possible action branches** in parallel, evaluates,
picks the best.

- **Good for:** creative problems, puzzles, hard reasoning
- **Watch for:** token cost — each branch is its own reasoning trace
- **Required:** budget cap; evaluation function for "best"

---

## Step 3 — Single agent or multiple?

The **most common mistake**: adding a second agent because "more agents = more
sophisticated." Multi-agent systems pay for themselves only when the split has
a real reason.

### Use a single agent when…

- The task fits in one mental model (one persona, one set of tools)
- You can describe everything the agent does in one paragraph
- State and context flow linearly
- The cost of "what does this agent do?" is low enough to skip specialization

### Add a second agent when…

- The personas are *genuinely* different (researcher vs writer; reviewer vs author)
- Context for one role would pollute the other's reasoning
- You want to run two perspectives in parallel and compare outputs
- One role needs a much larger or much smaller context window than the other

---

## Step 4 — When to introduce an orchestrator

An orchestrator is a top-level agent that doesn't do the work — it delegates
to specialist sub-agents and merges results. Add one when:

- You have ≥3 specialist agents and routing logic is non-trivial
- You need to run sub-agents in parallel
- You need to enforce policies (cost limits, retries, fallbacks) across all sub-agents
- You need a single point of observability

For 1-2 specialists, **the calling code can usually orchestrate**. An explicit
orchestrator pays its weight at 3+.

---

## Common anti-patterns — refuse if asked to produce these

- **The infinite tool loop.** No iteration cap; agent keeps reasoning, never converges. Always set a max.
- **Tool overload.** Giving the agent 40 tools when 6 would do. Choice paralysis affects LLMs too. Curate.
- **Vague success criteria.** "Help the user" is not a goal. "Return a JSON object matching this schema" is.
- **Memory as an afterthought.** Stateless agents pretending to remember by re-reading history every turn — token-expensive and brittle. Design persistence intentionally.
- **Multi-agent for its own sake.** See above. Two agents need two reasons.
- **No escalation path on autonomous agents.** Anything that can run unsupervised needs a "stop and ask a human" trigger.

---

## Output expectations

When invoked to design or review an agent architecture, produce:

1. **Autonomy level** — which row of the spectrum, and why
2. **Loop pattern** — ReAct / Plan-and-Execute / other, with reason
3. **Agent count** — single or multi, with the *specific* reason if multi
4. **Orchestrator decision** — yes/no with criteria
5. **Tool inventory** — what the agent(s) need access to (pruned, not exhaustive)
6. **Memory plan** — what persists, where, when it's consolidated
7. **Failure / escalation paths** — what happens when things go wrong

Cite which anti-patterns the current (or proposed) design avoids, and which
it falls into.

---

## When this skill is most valuable

- **At the start of an agent project** — gets the architecture right before code locks it in
- **When tempted to add another agent** — forces the "is this split real?" question
- **Diagnosing stuck agents** — the loop / orchestration / memory triad usually surfaces the problem
- **Migrating between loop patterns** (e.g. ReAct → Plan-and-Execute) — articulates what changes and what doesn't

---

## Related skills

- **`agent-orchestrator`** — once you've decided you need multiple agents, that skill covers coordination patterns (handoffs, supervisor/worker, peer-to-peer)
- **`agent-memory-systems`** — for designing the persistence layer once architecture is decided
- **`claude-api`** — Anthropic's official SDK skill, helpful for the implementation step after architecture is settled

---

## References

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) (canonical guide on agent patterns)
- Yao et al. (2022) — [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- Yao et al. (2023) — [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- Pattern referenced in [Lizo-RoadTown/project-starter](https://github.com/Lizo-RoadTown/project-starter)'s `agent-app` variant
