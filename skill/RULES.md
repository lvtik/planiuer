# Plan Standards

Rules governing every plan this skill produces, regardless of project type. Read this first; the topic files (guides/core.md, guides/security.md, guides/quality.md, guides/first-run.md) define WHAT goes in a plan — this file defines what a plan IS.

## 1. Output Contract
Every plan is a single markdown document with this skeleton:
- **Header block**: project name, one-sentence goal, date, plan version (v1, v2…)
- **Summary**: ≤10 lines a reader can act on without reading further — what's being built, the chosen stack in one line, the single biggest risk, the first milestone
- **Body**: the required sections from each applicable topic file, in topic-file order (Core → Security → Quality → First-Run)
- **Decision log**: every open decision from all sections, collected in ONE table at the end — option A/B/C, recommended default, cost to reverse. The user answers here, not scattered across forty pages
- **Next actions**: the first 3–5 concrete tasks, each small enough to start today

## 2. Which Files Apply
- `guides/core.md`: always
- `guides/security.md`: network-facing, multi-user, or handles user data — otherwise one line: "local single-user tool, security file skipped"
- `guides/quality.md`: anything involving implementation (skip for pure research/strategy plans)
- `guides/first-run.md`: always when code will be written; its §1 verification tasks MUST appear as explicit tasks inside roadmap phases, not as an appendix
- State at the top of the plan which files were applied and which were skipped, with the one-line reason

## 3. Depth Calibration
Plan size must match project size — a bloated plan is a defect equal to a shallow one.
- Weekend project / single tool: each section ≤ half a page; total plan ≤ 3 pages
- Multi-week solo project: full sections; total ≤ 8 pages
- Multi-person or multi-month: full sections + the optional extras where warranted
- Test: if a section could be pasted into any other project's plan unchanged, it is boilerplate — delete or specialize it

## 4. Plan Quality Bar
A plan passes only if all of these hold:
- **Actionable**: every roadmap phase starts with a verb and ends with a "done when" a stranger could verify
- **Falsifiable**: claims are checkable — "SQLite handles our write load (≤50 writes/s per docs)" not "SQLite should be fine"
- **Traceable**: every control maps to a threat, every task to a phase, every phase to a feature; orphans indicate a hole
- **Honest**: unknowns are listed AS unknowns with a plan to resolve them — never papered over with confident wording
- **Decision-complete**: nothing expensive to reverse is silently pre-decided; it's in the decision log or it's a violation

## 5. Plan Lifecycle
A plan is a living document, not a ceremony performed once.
- Version on change: material scope/stack changes bump the version and get one line in a changelog at the bottom — never silently rewrite history
- Reality beats plan: when implementation contradicts the plan, update the plan the same day; a stale plan is worse than none because it's trusted
- Re-plan triggers: a phase overruns its size estimate by 2×, a §1 assumption from FIRST_RUN.md falls, or the user changes a logged decision — any of these forces a plan review, not a quiet workaround
- Kill criteria: state up front what result would mean stopping the project — plans without a kill condition drift into sunk-cost territory

Additional meta-sections (stakeholder sign-off, budget tracking) MAY be added when the project warrants them — never before or instead of these five.