# ADR-0002: Service directory topology

## Status

Accepted by the user on 2026-07-15. Supersedes ADR-0001.

## Context

The first bootstrap placed API and Worker code in one `backend/` directory. The user requires the repository and implementation to express deployment services as separate directories and business/platform modules to have explicit owners.

## Options considered

| Option | Benefits | Costs |
|---|---|---|
| Keep one backend source tree with two process entry points | Maximum code reuse | Repository does not express the required service boundary |
| Separate Web, API and Worker code services | Explicit build/release ownership and independent dependency sets | Small bootstrap runtime helpers are duplicated and must remain behaviorally aligned |
| Split every business module into a network service | Maximum physical isolation | Premature distributed contracts, transactions and operations |

## Decision

- Place deployable code in `services/web`, `services/api`, and `services/worker`.
- Give API and Worker independent Python manifests, lockfiles, virtual environments, package namespaces, tests and Docker images.
- The API service owns eight bootstrap module declarations: identity/access, task lifecycle, creative reference, creative content, review/compliance, release/cycle, feedback/decision and governance/operations.
- The Worker service owns the AI execution module declaration and the bounded `--check` entry point.
- No service may directly import another service's Python namespace. A future API/Worker business interaction requires a separately approved public asynchronous contract; none is invented in this bootstrap.
- PostgreSQL remains the sole bootstrap stateful dependency. The API owns the empty Alembic baseline; both API readiness and Worker startup may probe PostgreSQL with finite deadlines.
- Keep the existing operational HTTP contract and exclude Redis, brokers, business schemas, provider SDKs and object-storage implementations.

## Trade-offs and consequences

- Service autonomy is visible in the repository and each service can evolve its dependency set independently.
- A small amount of logging/settings/PostgreSQL-probe bootstrap code is duplicated to prevent a hidden source dependency between services. Extraction requires a confirmed second shared lifecycle, not syntax similarity alone.
- There is no API-to-Worker network contract yet, so no business job can be dispatched in this slice.
- The architecture check verifies singular module ownership, public module imports, dependency cycles and direct cross-service import violations.

## Revisit triggers

Revisit runtime-helper duplication after both services have a confirmed shared change lifecycle, and define an API/Worker contract only when an approved business execution slice specifies delivery, retry, idempotency, persistence and recovery semantics.
