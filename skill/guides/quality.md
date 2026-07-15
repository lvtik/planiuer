# Code Quality, Readability & Token Efficiency

Every plan MUST contain these five sections, in this order. Do not skip any; if a section is not applicable, state why in one line instead of omitting it. These are standards the implementation phases in the roadmap must inherit — not a separate cleanup phase at the end.

## 1. Quality Standards
Concrete and checkable, not aspirational.
- Language-specific baseline: linter + formatter + strictness level (e.g. clippy with `-D warnings`, `gofmt` + `govet`, `ruff` + `mypy --strict`) — name the exact tools and config
- Error handling policy in one rule: what is recoverable (handle), what is a bug (fail loudly), what is never silently swallowed
- Test expectations per component type: what MUST be tested (parsing, money, auth, anything in §1 of the security file), what MAY be skipped (glue, one-off scripts)
- CI gate: which of the above block merge vs. only warn

## 2. Readability Rules
Optimize for the next reader — which is usually you in three months, or an agent with no context.
- Naming: full words over abbreviations; the name states what it IS or DOES, never its type (`retry_limit`, not `num` or `int_val`)
- Function size heuristic: fits on one screen; does one thing nameable without "and"
- Comments explain WHY, never WHAT — a comment restating the code is a deletion candidate; a magic number without a why-comment is a defect
- Nesting: prefer early returns over arrow-shaped code; three levels deep is a refactor signal
- Consistency beats preference: match the file's existing style even when you'd choose differently

## 3. Token Efficiency
Code and docs in this project will be read by AI agents. Context is a budget — spend it on signal.
- Self-describing structure: clear names + small files mean an agent can navigate by filename and skim, instead of reading everything
- File size ceiling: split files past ~300–400 lines; an agent should be able to load one module without dragging in five
- No dead weight: no commented-out code, no unused exports, no boilerplate headers — every line an agent reads costs budget
- Docs follow progressive disclosure: README states what + how to run in under a page; details live in linked files read on demand
- Repetition is a tax: extract shared logic not just for DRY, but so a change is one read + one edit, not a repo-wide grep

## 4. Structure & Dependencies
- Module boundaries: each module has one sentence stating its responsibility; if the sentence needs "and", split it
- Dependency direction: core logic depends on nothing project-specific; I/O, UI, and platform code depend on core — never the reverse
- Third-party policy: prefer stdlib; every new dependency needs a one-line justification in the plan (ties into §3 of the security file)
- Public surface minimal: default private/internal; every exported item is a promise you maintain

## 5. Trade-offs & Open Decisions
- Where quality is deliberately relaxed (prototypes, spikes, generated code) — mark these zones explicitly so relaxed standards don't leak
- Conflicts resolved in advance: when readability and token-thrift collide, readability wins; when performance and clarity collide, clarity wins until profiling proves otherwise
- User decisions with a recommended default: test coverage target, lint strictness, comment density, docs language

Additional sections (performance budget, benchmark suite, style-guide deep dive) MAY be added after these five when the project warrants them — never before or instead of them.