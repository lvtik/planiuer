# First-Run Correctness

Every plan MUST contain these five sections, in this order. Do not skip any; if a section is not applicable, state why in one line instead of omitting it. Goal: code that compiles and behaves correctly on the first run — not because of luck, but because uncertainty was removed BEFORE writing.

## 1. Verify Before Writing
Most first-run failures are wrong assumptions, not wrong logic. Kill assumptions first.
- API/library contracts: for every external API or unfamiliar library call, check the actual signature, return type, and error behavior against current docs or source — NEVER from memory. Version drift is the #1 cause of plausible-looking broken code
- Environment facts: confirm the runtime version, platform quirks, and available tooling before choosing features (e.g. does the target still ship an EFI-only bootloader? Is this glibc or musl?)
- Data shape: obtain one real sample of every input (API response, file format, CLI output) and design against the sample, not the imagined shape
- List remaining unverified assumptions explicitly — each one is a place the code may break on run one

## 2. Design for Verifiability
Structure the work so correctness is observable at every step, not only at the end.
- Slice vertically: the first milestone is the thinnest end-to-end path that runs (hello-world through the full stack), then thicken — never build all layers "to spec" and integrate at the end
- Every phase from the roadmap ends with a concrete runnable check: a command + its expected output, written in the plan
- Prefer designs where failure is loud and early: strict parsing at boundaries, asserts on invariants, fail-fast config validation at startup — a crash at launch beats corruption at hour three
- Types as proof: encode invariants in the type system where the language allows (newtypes, enums over stringly-typed state, non-nullable by default) so entire bug classes can't compile

## 3. Write in Checkable Increments
- Increment size rule: never write more code than can be verified in one step — one function + its test, one endpoint + one curl, one parser + one sample file
- Compile/lint/typecheck after EVERY increment, not at the end; a type error in 30 fresh lines is trivial, in 800 it's archaeology
- Stub the unknown: if a dependency is unverified (§1), isolate it behind a thin interface so a wrong assumption forces a one-file fix, not a rewrite
- Edge cases in first draft, not in review: empty input, zero, one, boundary, unicode, missing file, network timeout — enumerate the list per component in the plan

## 4. Pre-Run Checklist
The plan MUST include a checklist run before first execution:
- Clean-environment build: fresh clone + documented setup steps only — catches the "works on my machine because of undeclared state" class
- All inputs present: sample data, env vars, config files named in one place with defaults or clear errors when missing
- Failure-path glance: for each external call — what happens when it fails? "Nothing handled" is an answer; write it down as accepted risk
- Reread the diff cold: read the code top-to-bottom as if reviewing a stranger's PR; off-by-ones and inverted conditions are caught by reading far more cheaply than by running

## 5. When First Run Still Fails
Plan the debugging before it's needed — panic-debugging destroys clean code.
- Error messages carry context: every error path includes what was attempted and with what values — "failed to parse config: missing key 'port' in /etc/app.toml", never "error: invalid input"
- One-command repro: the failing case must be reducible to a single command a human or agent can rerun
- Fix at the assumption, not the symptom: when a §1 assumption proves wrong, update the verification note AND the code — otherwise the same wrong assumption resurfaces in the next component
- Two failed fix attempts on the same bug = stop and re-verify the underlying contract (docs, source, real data) instead of a third guess

Additional sections (property-based testing, fuzzing plan, formal invariants) MAY be added after these five when the project warrants them — never before or instead of them.