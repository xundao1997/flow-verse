# FlowVerse Evidence Policy

## Purpose

- Every implementation claim must trace to concrete evidence.
- Unknown facts remain Unknown; inference never becomes project fact through repetition.
- Evidence authorizes conclusions only within its stated scope.

## Authority by Fact Type

| Fact type | Authority order |
|---|---|
| Product intent and authorization | Current explicit user decision about that fact → user-approved V1 package or decision record → repository product specification |
| Expected behavior | Approved product brief and acceptance criteria → approved interaction/design rules → current tests and code as evidence of current behavior only |
| Approved target stack, version, or command | Current explicit user decision → approved V1 package → approved architecture/engineering decision |
| Approved architecture decision | Current explicit user decision → Accepted ADR → approved V1 package evidence |
| Current implementation fact | Source, tests, config, CI, manifest, lockfile → engineering documentation → nearby established code pattern |
| Current module, dependency, contract, and data ownership | Source/config/deployment evidence plus Confirmed ../engineering/ARCHITECTURE_BASELINE.md; a target ADR alone does not prove runtime state |
| Resolved installed version | Lockfile → installed metadata → manifest range; never memory or “latest” |
| Currently executable command and directory | Bootstrap: approved exact target command plus tool/environment verification; after bootstrap: checked-in script/config/CI plus environment verification |
| Design asset and copy | Current explicit user decision → approved V1 package artifact → approved repository design/copy specification |
| Performance target | Current explicit user decision → approved package budget → approved project performance registry |
| Performance result | Raw same-environment measurement tied to build, scenario, command, and output; a target or budget never proves a result |
| Reliability target | Current explicit user decision → approved package requirement → Confirmed ../engineering/RELIABILITY_BUDGET.md entry |
| Reliability, recovery, or failure-test result | Raw monitoring/test/restore evidence tied to build, environment, scenario, command, and output |
| Technical-debt acceptance or extension | Current explicit user decision recorded in ../engineering/TECH_DEBT_REGISTER.md; AI may only propose |

## Evidence Status

- Confirmed: directly supported by a precise source.
- Conflict: authoritative sources disagree.
- Unknown: required evidence is absent.
- N/A: proven outside the current scope.
- Assumption: explicitly labeled hypothesis used only for discussion, never implementation authorization.

## Evidence Record

Record material conclusions during V1 package intake and task planning:

| Claim | Fact type | Status | Exact evidence path and field | Conflict or gap | Decision owner |
|---|---|---|---|---|---|
| TBD | TBD | Unknown | TBD | TBD | User |

“From the project package” is not a sufficient citation. Name the file, page, frame, section, key, script, or line.

## Conflict Protocol

1. Record the competing claims and exact evidence.
2. Stop only the affected implementation path.
3. Explain user-visible, contract, data, security, and performance impact.
4. Present safe options without silently selecting one.
5. Resume only after the user records a decision or supplies stronger evidence.

## Prohibited Fabrication

AI must not invent or assert without evidence:

- API paths, methods, fields, status codes, schemas, tables, indexes, or relationships
- Frameworks, dependencies, package managers, providers, models, or versions
- Scripts, shell commands, environment variable names, ports, deployment targets, or CI behavior
- Routes, components, directories, assets, fonts, copy, permissions, roles, or security rules
- Test results, logs, screenshots, bundle sizes, latency, memory, cost, or optimization claims

Examples must be labeled “Example — not project fact” and cannot authorize code. Do not create manifests, configs, mocks, APIs, directories, or fake data merely to make an assumption appear true.
