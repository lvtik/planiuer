# planiuer

**A planning skill for AI coding agents.** It teaches your agent to stop guessing and produce a real plan before it writes a single line of code.

Install it once, then ask Claude, Codex, or OpenCode to plan something big. Instead of a vague wall of bullet points, you get a `PLAN.md` you can actually act on.

---

## What problem does this solve?

Ask an AI agent to "build me a VPN bot" and it will happily start typing. Twenty files later you find out it picked a database you didn't want, forgot authentication entirely, and made three decisions that are expensive to undo.

planiuer puts a planning step in front of that. The agent decomposes the work into phases, names the risks, and — importantly — brings the decisions that are *yours* back to you instead of quietly choosing for you.

## What you get

Every plan is one `PLAN.md` with a fixed shape:

| Part | What's in it |
| --- | --- |
| **Header** | Project, goal in one sentence, date, version |
| **Summary** | 10 lines max — what's being built, the stack, the biggest risk, first milestone |
| **Body** | The applicable sections (see below) |
| **Decision log** | One table, all open choices, options + recommended default + cost to reverse |
| **Next actions** | 3–5 tasks small enough to start today |

The body is assembled from four guides, applied only when relevant:

- **Core** (always) — features and non-goals, tech stack with a reason for every pick *and* one rejected alternative, an ordered roadmap where every phase has a "done when", risks with fallbacks, and the decisions left to you.
- **Security** (network-facing, multi-user, or handles user data) — threat model specific to your project, data inventory, controls mapped to threats, privacy posture, incident plan.
- **Quality** (anything with code) — exact linter/formatter config, error-handling policy, readability rules, module boundaries, dependency direction.
- **First-run** (whenever code gets written) — verify API signatures against real docs before writing, slice vertically, work in checkable increments, pre-run checklist.

Skipped guides aren't silently dropped — the plan says which were skipped and why, in one line each.

## Why it's good

- **It says "I don't know."** Unknowns get listed as unknowns with a plan to resolve them, instead of being papered over with confident wording.
- **Claims are checkable.** "SQLite handles our write load (≤50 writes/s per docs)" — not "SQLite should be fine."
- **Nothing expensive is decided behind your back.** If it's costly to reverse, it's in the decision log for you to answer. That's a rule, not a suggestion.
- **The plan matches the project.** A weekend tool gets ≤3 pages. A multi-month effort gets full sections. Bloat is treated as a defect equal to shallowness — if a section could be pasted into any other project's plan unchanged, it gets deleted.
- **It kills the "looks right, doesn't run" failure.** The first-run guide forces the agent to check real API signatures and real data samples instead of writing from memory. Version drift is the number one source of plausible-looking broken code.
- **It has a kill switch.** Every plan states up front what result would mean stopping the project — so you don't drift into sunk-cost territory.
- **It stays alive.** Material changes bump the version and get a changelog line. When reality contradicts the plan, the plan gets updated the same day.
- **Works with your agent.** Claude, Codex, and OpenCode — same skill, installed to all of them at once.

## When to use it

**Good fit:** a new system or service, a migration, a rewrite, a product launch, anything multi-week or multi-person. Also good when you're just staring at a problem thinking "where do I even start?"

**Bad fit:** single tasks, quick fixes, or work that's already scoped. Don't plan a typo.

---

## Install

You need Python 3 and at least one of Claude, Codex, or OpenCode already installed.

### macOS / Linux

```sh
curl -fsSL https://raw.githubusercontent.com/lvtik/planiuer/main/install.py | python3 -
```

### Windows (PowerShell)

```powershell
iwr -useb https://raw.githubusercontent.com/lvtik/planiuer/main/install.py | python3 -
```

### From a clone

```sh
git clone https://github.com/lvtik/planiuer.git
cd planiuer
python3 install.py
```

The installer finds every supported agent on your machine and copies the skill into each one's `skills/` directory:

| Agent | Installed to |
| --- | --- |
| Claude | `~/.claude/skills/planning-large-projects` |
| Codex | `~/.codex/skills/planning-large-projects` |
| OpenCode | `~/.config/opencode/skills/planning-large-projects` |

Agents you don't have are skipped. Re-running the installer overwrites the existing copy, so that's how you update.

## Use it

Nothing to invoke. Just ask your agent to plan something:

- *"Plan a Telegram bot that issues WireGuard configs across a multi-country server fleet."*
- *"I want to migrate our Postgres monolith to event sourcing. Where do I start?"*
- *"Help me think through a CLI that verifies file checksums against a manifest."*

The agent reads the skill, works out which guides apply, and writes `PLAN.md`.

## Examples

Two worked examples ship with the skill:

- [`skill/examples/small-cli.md`](skill/examples/small-cli.md) — a Rust checksum CLI. Security guide skipped (local, single-user, no network). ~50 lines.
- [`skill/examples/multi-week-service.md`](skill/examples/multi-week-service.md) — a Go WireGuard bot. All four guides. ~90 lines.

They exist so the agent can calibrate depth to your project's size. Match the depth, not the content.

## Layout

```text
install.py                     installer
skill/
  SKILL.md                     entry point — tells the agent what to read, in what order
  RULES.md                     the contract: output format, which guides apply, depth, quality bar
  guides/
    core.md                    features, stack, roadmap, risks, decisions
    security.md                threat model, data, controls, privacy, incidents
    quality.md                 standards, readability, structure, trade-offs
    first-run.md               verify, design for verifiability, increments, checklist
  examples/
    small-cli.md
    multi-week-service.md
```

## License

MIT
