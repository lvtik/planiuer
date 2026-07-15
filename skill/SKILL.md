---
name: planning-large-projects
description: >
  Produces deep, structured plans for large or complex projects: decomposes scope into
  phases and milestones, maps dependencies and critical path, surfaces risks and unknowns,
  defines success criteria, and sequences work into an actionable roadmap. Use when the
  user asks to plan, architect, scope, roadmap, break down, or estimate a substantial
  piece of work — a new system, service, migration, rewrite, product launch, or
  multi-week/multi-person effort — or says things like "where do I start", "how should I
  approach this", or "help me think this through". Not for single tasks, quick fixes, or
  work already scoped.
---

# Planning Large Projects

## Process
Read the files in this order. Do not start writing the plan before step 1 is done.

1. **`RULES.md` — always, first.** It is the router and the contract: it defines which
   guides apply to this project (§2), how deep each section goes (§3), the output
   format (§1), and the quality bar (§4–5). Where anything conflicts, RULES.md wins.
2. **`guides/core.md` — always.** The five mandatory sections of every plan.
3. **Conditionally**, per RULES.md §2:
   - `guides/security.md` — security & privacy sections
   - `guides/quality.md` — code quality, readability, token efficiency
   - `guides/first-run.md` — first-run correctness; its §1 verification tasks go
     INSIDE roadmap phases, not in an appendix

## Result
Produce a single `PLAN.md` following the output contract in RULES.md §1
(header block → summary → body in guide order → decision log → next actions).
State at the top which guides were applied or skipped, with a one-line reason each.

## Examples
If unsure how deep to go for a given project size, skim the one example in
`examples/` that matches the scale (e.g. `examples/small-cli.md`,
`examples/multi-week-service.md`), then match its depth — not its content.