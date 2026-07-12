# FlowVerse Change Policy

## Automation Boundary

- AI may inspect, plan, split tasks, edit code, run checks, and self-review within an explicitly requested goal.
- AI must not invent or change product direction, UIUX principles, acceptance criteria, or success metrics.
- Stop for human confirmation when a change affects those constraints or requires a new dependency, backend contract, architecture decision, destructive action, security boundary, or sensitive data.

## Before Editing

1. Read ../../AGENTS.md, any nearer directory-scoped instructions, and the source-of-truth documents.
2. Confirm ../intake/V1_PACKAGE_INTAKE.md is APPROVED for the active slice and task-relevant target/runtime TECH_STACK.md facts satisfy the bootstrap or business gate.
3. Inspect current code, tests, configuration, manifests, lockfiles, CI, and Git status.
4. Identify affected modules/owners, dependency edges, contracts, data, pages/components, reliability, tokens, and performance budgets.
5. Classify the change as Local, Contract, or Structural and write a plan with evidence, acceptance, ADR/debt impact, reliability/performance, verification, and recovery.
6. State files and systems intentionally left unchanged.

## Adding Code

- Place code in the established directory and follow nearby patterns.
- Place responsibility in its owning module and expose only the smallest required public contract.
- Reuse existing components and canonical tokens before creating new ones.
- Do not add UI, animation, state, chart, AI-provider, or backend libraries without approval.
- New dependencies require measured bundle, runtime, startup, memory, maintenance, and security impact.
- Cover applicable default, loading, empty, error, disabled, and success states.
- Add or update focused tests for changed behavior.

## Architecture and Evolution

- Local: stays inside a Confirmed module and changes no public contract, dependency direction, data ownership, security, reliability, or deployment semantics; no ADR is required.
- Contract: changes an API, event, exported type, config, route, schema, or persistent format; document consumers, compatibility, release order, migration, and rollback/forward recovery.
- Structural: changes an architecture-level public/data/deployment boundary, dependency direction, data ownership, architecture technology, or reliability/security strategy; draft an ADR and obtain user approval first.
- A local high-cohesion module extracted inside a Confirmed boundary remains Local when it changes no public contract, dependency direction, owner, data, security, reliability, or deployment semantics.
- Production dependencies remain directed and acyclic; cross-module access uses public contracts, never private internals or another owner's storage/state.
- First use stays local. Extract only for a second real consumer, an approved second implementation/phase, or a confirmed external volatility boundary.
- Do not add shared/utils dumping grounds, god modules, pass-through wrappers, central switches, universal stores/services, or behavior-free abstractions.
- Architecture exceptions and temporary compatibility paths require a Proposed debt entry with owner, expiry, and exit criteria; AI cannot Accept the risk.
- Hot-path abstraction must include performance evidence; “decoupling” does not excuse extra calls, serialization, rendering, or memory cost.

## Modifying Code

- Preserve public props, APIs, stored data, and navigation unless the task authorizes a breaking change.
- Keep business state out of presentation primitives and page orchestration out of base components.
- Centralize reusable copy and tokens; do not scatter duplicated literals.
- Do not modify unrelated files or reformat untouched areas.
- Do not add speculative memoization, caching, lazy loading, workers, concurrency, or indexes without evidence and measurement.

## Deleting or Moving

- Verify references, generated outputs, imports, routes, tests, and documentation before deletion.
- Explain the reason, affected references, compatibility impact, and rollback or recovery path.
- Never delete design specifications, acceptance criteria, or rollback evidence as cleanup.

## Backend Boundary

- UIUX work is frontend-only by default.
- Do not change API schemas, database models, authentication, AI runtime, workflow runtime, or providers unless explicitly requested.
- If frontend-only work is insufficient, report the exact contract gap, compatibility impact, and required tests before editing backend code.

## Verification and Handoff

- Run the narrowest relevant checks first, then repository-wide checks required by CI.
- Execute the production-build workflow in PERFORMANCE_BUDGET.md for performance-sensitive changes.
- Execute applicable architecture/contract checks and the gates in RELIABILITY_BUDGET.md.
- Review the diff for scope, secrets, generated files, regressions, performance, and forbidden UI patterns.
- Report changed files, behavior, module/contract/ADR/debt changes, checks, reliability evidence, visual evidence, applicable performance before/after or N/A with reason, Unverified items, and remaining risks.
