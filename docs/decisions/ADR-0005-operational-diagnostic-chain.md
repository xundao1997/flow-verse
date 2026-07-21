# ADR-0005: Operational diagnostic chain and three-service runtime

## Metadata

| Field | Value |
|---|---|
| Status | Accepted |
| Decision owner | User |
| Date | 2026-07-20 |
| Scope IDs | FV1-DIAGNOSTIC-BOOTSTRAP / FV1-LOCAL-RUNTIME / FV1-DELIVERY-BOOTSTRAP |
| Evidence | User instruction to fix all reviewed deployment blockers, 2026-07-20; architecture review findings; ADR-0002 and ADR-0004 |
| Supersedes | The no API-to-Worker network-contract and one-shot-only Worker portions of ADR-0002 and ADR-0004 |

## Context

- FlowVerse already has separate Web, API and Worker service directories, but the
  Web source is absent and the Worker is not reachable as a native long-running
  process.
- The user needs one non-business page that proves the deployed Web can reach the
  API and that the API can reach a dependency-ready Worker.
- A process-only ping can report a false ready state while PostgreSQL is
  unavailable. Container-local `127.0.0.1` also cannot identify another service.
- Local development must remain native and Compose-free. Production remains
  direct Docker on Yunxiao-managed host groups.

## Options

| Option | Benefits | Costs / risks | Complexity | Lock-in | When valid |
|---|---|---|---|---|---|
| Keep independent health endpoints only | No new service edge | Cannot prove the browser-to-Worker chain | Low | None | Individual service checks only |
| Synchronous operational diagnostic contract | Small, observable, easy to exercise; no broker | Adds a bounded API-to-Worker runtime dependency for this endpoint | Low | HTTP only | Selected bootstrap diagnostic |
| Introduce a queue and asynchronous job contract | Closer to future business execution | Invents delivery, persistence, retry and idempotency semantics | High | Broker | Future approved business execution only |

## Decision

- Add `GET /api/v1/system/chain` as the Web-facing operational diagnostic
  contract.
- Add `GET /internal/v1/system/status` as the API-to-Worker diagnostic contract.
  It checks the Worker's PostgreSQL dependency and returns either ready or an
  explicit unavailable reason.
- The API checks its own PostgreSQL probe and the Worker concurrently. The chain
  returns HTTP 200 only when both services are dependency-ready; otherwise it
  returns a typed HTTP 503 response.
- API-to-Worker calls have a two-second deadline and no automatic retry.
- Local development starts Web, API and Worker as native processes. Production
  containers share one user-defined Docker network: Web proxies to
  `flowverse-api:8000`, and API receives
  `FLOWVERSE_WORKER_BASE_URL=http://flowverse-worker:8001`.
- The Web page is an operational Check surface only. It is not a product home,
  authentication surface, workflow builder or business API consumer.

## Rationale and Trade-Offs

- The synchronous diagnostic is the smallest contract that proves all three
  deployment services can communicate.
- Reusing each service's PostgreSQL probe prevents a reachable process from being
  labelled ready when its required dependency is unavailable.
- A same-origin Web proxy avoids a permissive CORS policy and keeps local and
  production browser requests consistent.
- The endpoint adds one directed API-to-Worker edge. This edge is operational and
  does not authorize business task dispatch, queues, retries or shared source.

## Impact

- Modules and ownership: Web owns presentation, API owns aggregation, Worker owns
  Worker readiness, and each Python service retains its own PostgreSQL probe.
- Public contracts: the two versioned JSON schemas become compatibility surfaces.
  Mixed versions degrade safely through invalid-response or connection reasons.
- Reliability: finite deadlines, zero retries, explicit 503 degradation,
  correlated request/trace IDs and full exception evidence are required.
- Performance: one user-triggered or initial diagnostic makes one API probe and
  one Worker request in parallel. There is no polling.
- Security: no credentials are returned. The Worker endpoint remains container-
  network/internal-host only and is not published by the host deployment script.
- Deployment: images are promoted together by immutable references. Health checks
  must pass before deployment succeeds; failure triggers the repository host
  script's previous-image rollback path.
- Technical debt: none accepted. Cloud binding and a successful Yunxiao run remain
  environment evidence, not source-code claims.

## Implementation and Verification

- Add focused API HTTP-client/chain tests and Worker HTTP contract tests.
- Add Web parser tests and production build verification.
- Add native `worker`, `web` and `all` startup modes and a bounded host deployment
  script for Yunxiao Docker deployment.
- Run the registered architecture self-test/check, backend quality suites, Web
  lint/format/typecheck/test/build and local Web-to-API-to-Worker smoke test.
- Rollout order is Worker, API, Web. Rollback uses the previous image references in
  the same order and the unchanged host-managed environment file.

## Revisit Triggers

- A business execution slice needs delivery, persistence, retry, idempotency,
  cancellation or result retrieval.
- The diagnostic gains another consumer or exposes sensitive operational detail.
- Service placement changes from one Docker host/network to an orchestrator.
- The two-second deadline or no-retry policy fails measured reliability needs.

