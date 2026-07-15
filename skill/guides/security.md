# Security & Privacy Planning

Every plan MUST contain these six sections, in this order. Do not skip any; if a section is not applicable, state why in one line instead of omitting it. Scale depth to the project — a CLI tool gets a paragraph per section, anything network-facing or multi-user gets the full treatment.

## 1. Threat Model
Who attacks this and what do they get? No generic boilerplate — name threats specific to THIS project.
- Assets worth protecting, ranked: credentials, user data, keys, infrastructure access
- Attacker profiles that actually apply: opportunistic scanner, malicious user, compromised dependency, insider — cut the ones that don't
- Attack surface inventory: every input, endpoint, file parse, deserialization, IPC channel, and third-party callback
- Explicit non-threats: what you are consciously NOT defending against, and why

## 2. Data Inventory & Classification
You cannot protect data you haven't listed.
- Every category of data collected, generated, or passed through — one line each
- Classify each: public / internal / sensitive / secret
- For each sensitive+ item: where it lives, how long it lives, who can read it
- Data you deliberately do NOT collect — minimization is a design decision, record it

## 3. Controls & Mitigations
Map each threat from §1 to a control. Unmapped threats are accepted risks and belong in §6.
- AuthN and AuthZ model: who proves identity how, and what boundary enforces permissions
- Secrets handling: where keys/tokens live (env, keychain, vault), how they rotate, what must never touch the repo or logs
- Input handling: validation and encoding strategy at every trust boundary from §1
- Transport and at-rest encryption: what is encrypted, with what, and what deliberately isn't
- Dependency policy: how supply-chain risk is handled (lockfiles, audit cadence, pinning, minimal deps)

## 4. Privacy Posture
Separate from security — this is about what the system does with data even when working as intended.
- Telemetry and logging: exactly what is recorded, whether it can contain PII, retention period
- Third parties that receive any user data, and what they receive
- User rights: can a user export their data? Delete it? What actually happens on delete?
- Regulatory surface if any (GDPR, COPPA, regional data-residency) — one line naming which apply and the single biggest obligation each creates

## 5. Failure & Incident Plan
Assume a control fails.
- Blast radius per §2 class: what leaks if the DB leaks? If a token leaks?
- Detection: how would you even know? Logs, alerts, canaries — name the mechanism
- Response basics: kill switch / key rotation / user notification path, each one line
- Recovery: backups exist? Tested? Who restores?

## 6. Accepted Risks & Open Decisions
- Every threat consciously left unmitigated, with the reason (cost, likelihood, scope)
- Security/privacy choices that belong to the user, each with 2–3 options and a recommended default — e.g. "local-only storage vs. synced", "anonymous telemetry vs. none"
- Never silently accept a risk that is expensive to reverse (data collection scope, encryption scheme, ID format)

Additional sections (pen-test plan, compliance checklist, abuse/fraud modeling) MAY be added after these six when the project warrants them — never before or instead of them.