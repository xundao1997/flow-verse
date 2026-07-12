# FlowVerse V1 Package Intake

## Package Review State

**AWAITING_PACKAGE**

This global state describes receipt/review of the latest package revision. Code gates read the matching row in Approval Scopes, not this global state.

Allowed transitions:

- AWAITING_PACKAGE → IN_REVIEW
- IN_REVIEW → BLOCKED or APPROVED
- BLOCKED → IN_REVIEW after new evidence or a user decision
- APPROVED → IN_REVIEW when a revised package changes approved facts
- Any replaced package revision → SUPERSEDED

- Only the user may approve an intake scope or resolve product and architecture conflicts.
- Do not write business code before the state is APPROVED for that implementation slice.
- A non-business engineering bootstrap may begin after the bootstrap scope, target stack, and exact bootstrap plan are approved.
- If the package contains source, determine whether it is the implementation baseline or reference material before editing it.

## Approval Scopes

| Scope ID | Package revision | Scope type and description | State | Exact evidence / decision | Approved by and date | Deferred unrelated Unknowns |
|---|---|---|---|---|---|---|
| TBD | TBD | Bootstrap or implementation slice — do not infer | AWAITING_PACKAGE | None | None | TBD |

Each scope row follows the same review transitions independently. A revised package moves only affected rows back to IN_REVIEW; unaffected APPROVED rows remain valid unless the user supersedes them.

APPROVED accepts the package revision and named scope; it does not claim every future subsystem is fully specified. Unknown facts outside the active scope remain deferred and do not block unrelated work.

## Receipt Record

| Field | Value |
|---|---|
| Package name | TBD — do not infer |
| Original location | TBD — do not infer |
| Received date and timezone | TBD — do not infer |
| Size and file count | TBD — do not infer |
| Integrity hash | TBD — do not infer |
| Declared V1 revision | TBD — do not infer |
| User-designated authority | TBD — do not infer |

Preserve the original package unchanged. Extract or convert only into a separate working location.

## Artifact Classification

Classify every artifact as one of:

- Authoritative specification
- Implementation baseline
- Reference
- Draft
- Example
- Generated output
- Historical material, only when the user explicitly identifies it as historical

Record exact path, type, status, scope, dependencies, and conflicts. Do not treat visual similarity or filename wording as authority.

## Required Inventory

### Product and Design

- Product scope, user journeys, pages, navigation, states, copy, and acceptance
- Design files, frames, components, tokens, breakpoints, motion, accessibility, and responsive behavior
- Fonts, icons, images, illustrations, licenses, export rules, and source-of-truth ownership
- Empty, loading, error, offline, recovery, permission, destructive, and unsaved states

### Engineering

- Source roots, manifests, lockfiles, runtime, language, frameworks, build tools, and package manager
- Users/load/data scale, team expertise, phase roadmap, domain complexity, real-time, compliance, budget, and deployment constraints needed for architecture decisions
- Module boundaries, owners, dependency direction, public contracts, data/invariant ownership, process/deployment boundaries, and external adapters
- Routing, state, data access, editor, API/schema, backend, database, auth, AI provider/SDK, and storage
- Lint, format, typecheck, unit, integration, E2E, build, performance, CI/CD, deployment, and observability
- Existing architecture decisions, compatibility promises, temporary paths, TODO/FIXME/HACK, and baseline technical debt
- Environment variable names and configuration contracts without recording secret values

### Performance and Operations

- Target browsers, devices, CPU, network, cache state, data scale, document size, concurrency, and session duration
- Bundle/asset budgets, route readiness, input/background persistence when specified, API, AI latency/cost, memory, and regression thresholds
- Critical flows, availability SLI/SLO, error budget, RTO/RPO, capacity, timeout/retry/idempotency, degradation, isolation, health, and failure-test requirements
- Privacy, security, retention, backup/restore evidence, recovery, rate-limit, cancellation, rollout, rollback/forward recovery, and operational ownership

## Required Outputs

- Update ../governance/EVIDENCE_POLICY.md evidence records for material decisions.
- Populate ../engineering/TECH_STACK.md with Confirmed, Conflict, Unknown, or N/A entries.
- Populate ../engineering/ARCHITECTURE_BASELINE.md without inventing modules or dependencies.
- Classify applicable targets and controls in ../engineering/RELIABILITY_BUDGET.md.
- Initialize baseline entries in ../engineering/TECH_DEBT_REGISTER.md and register any Proposed ADR in ../decisions/DECISION_LOG.md.
- Reconcile ../product/V1_PRODUCT_BRIEF.md and ../uiux/ without silently overriding current user instructions.
- Confirm project-specific entries in ../engineering/PERFORMANCE_BUDGET.md.
- Convert ../tasks/V1_IMPLEMENTATION_PLAN.md into a file-level plan.
- List missing evidence, conflicts, assumptions, exclusions, and user decisions.

## Approval Gate

Intake can become APPROVED only when:

- Inventory and artifact classification are complete for the approved scope.
- Product, design, implementation-baseline, and source-of-truth ownership are explicit for that scope.
- Architecture context needed by the selected patterns is Confirmed or the pattern is deferred.
- Task-relevant architecture target rows are Confirmed or N/A; implementation conformance may remain NotYetImplemented until the approved slice is built.
- Reliability Applicability is classified as Required, Optional, or N/A for the due scope; required target/verification states follow their Gate stage.
- Target technology, target version/range, bootstrap command, API, asset, and environment decisions required by the first approved slice are Confirmed or N/A.
- Resolved installed versions and generated project commands may remain NotYetInstalled / NotYetAvailable until the approved engineering bootstrap.
- The measurement plan and environment needed to establish initial lab budgets are approved; baseline-dependent thresholds have an explicit post-bootstrap confirmation gate.
- Required reliability target, recovery, capacity, observability, and failure-test plans have an explicit confirmation gate.
- Conflicts and missing decisions that affect the approved scope are resolved by the user.
- Acceptance criteria map to package evidence and a bootstrap or file-level implementation plan.
