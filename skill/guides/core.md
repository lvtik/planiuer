# Core Planning

Every plan MUST contain these five sections, in this order. Do not skip any; if a section is not applicable, state why in one line instead of omitting it.

## 1. Functionality
What the project does, as concrete capabilities — not marketing language.
- Core features, each one line: "user can X" / "system does Y"
- Explicit non-goals: what is out of scope for v1
- Primary user/consumer of each feature

## 2. Tech Stack
For every layer (language, framework, storage, infra, CI/CD):
- The chosen tool AND the reason in one sentence
- One rejected alternative and why it lost
- Version constraints or platform requirements that affect the design

## 3. Implementation Roadmap
Break the work into ordered phases:
- Each phase has a goal, a deliverable, and a "done when" criterion
- Mark dependencies between phases explicitly ("blocked by phase 2")
- Flag the riskiest phase and put it as early as dependencies allow
- Estimate relative size (S/M/L), not calendar dates, unless the user gave dates

## 4. Caveats & Risks
- Known technical risks and the fallback for each
- Assumptions the plan silently depends on — state them so they can be challenged
- Things that will bite later if ignored now (migrations, auth, i18n, licensing)

## 5. User Decisions
Decisions that belong to the user, not the plan:
- List each open choice with 2–3 options and a recommended default
- Never silently pick for the user on anything expensive to reverse

Additional sections (testing strategy, security review, cost estimate) MAY be added after these five when the project warrants them — never before or instead of them.