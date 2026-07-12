# FlowVerse V1 Technology Stack Registry

## Status Ownership

- Read package state and approved scope from ../intake/V1_PACKAGE_INTAKE.md.
- This file alone owns target-stack, resolved-runtime, and command-state facts.
- Unknown values remain “TBD — do not infer” under ../governance/EVIDENCE_POLICY.md.

## Stack Registry

| Area | Approved target | Target version/range | Exact target evidence | Target status | Resolved installed version | Runtime status |
|---|---|---|---|---|---|---|
| Runtime | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Backend / AI language | Python | TBD — awaiting V1 package | User direction, 2026-07-12 | Proposed | TBD | Unknown |
| Frontend language | TypeScript | TBD — awaiting V1 package | User direction, 2026-07-12 | Proposed | TBD | Unknown |
| Frontend framework | React | TBD — awaiting V1 package | User direction, 2026-07-12 | Proposed | TBD | Unknown |
| Rendering / meta-framework | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Build tool | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Package manager | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Router | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Styling and tokens | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| UI component system | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Long-form editor | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Client state | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Server/cache data | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Messaging / queue | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Background jobs / scheduler | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Resilience / rate limiting | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Forms and validation | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Backend framework | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| API protocol and schema | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Database / ORM | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Authentication / authorization | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| AI provider / SDK / model | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Unit / component test | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Integration / E2E test | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Lint / format / typecheck | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Performance tooling | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| CI/CD and deployment | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Deployment topology / orchestrator | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Logging / metrics / tracing | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Monitoring / observability | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |

Target status values: Proposed, Confirmed, Conflict, Unknown, N/A.

Proposed records a user-indicated direction but is not sufficient for bootstrap or business implementation until the V1 package or an explicit user decision confirms the exact target and version/range.

Runtime status values: Confirmed, NotYetInstalled, Unknown, Conflict, N/A.

## Command Registry

| Task | Approved exact command | Working directory | Exact evidence | Evidence status | Execution status |
|---|---|---|---|---|---|
| Bootstrap / install | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Development | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Lint / format | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Typecheck | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Unit test | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Integration / contract test | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| E2E test | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Architecture / dependency check | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Contract compatibility check | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Reliability / failure test | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Technical-debt reference check | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Production build | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Performance test | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |

Evidence status values: Confirmed, Conflict, Unknown, N/A.

Execution status values: Available, NotYetAvailable, Unavailable, Conflict, N/A.

## Greenfield and Version Rules

- A user decision or approved V1 package may Confirm a target technology, target version/range, and bootstrap command before files exist.
- A lockfile proves the resolved installed version after bootstrap; it does not authorize the target choice.
- Approved preparation may create only prerequisite files explicitly listed in the bootstrap plan; it may not execute a NotYetAvailable command.
- The bootstrap command may run only after Confirmed evidence and Available execution state are verified.
- Bootstrap creates only the minimum manifests, config, lockfile, quality gates, and measurement entry points required by the approved target; it adds no product behavior.
- After bootstrap, record resolved versions and verify generated commands before business implementation.
- Business code uses only task-relevant target and runtime entries that are Confirmed.
- A transitive package is not authorization to import or architect around it; never use “latest”.
- Alternatives, upgrades, new dependencies, and version changes require approval plus compatibility and performance impact.
- Update this registry in the same change that alters confirmed tooling.
