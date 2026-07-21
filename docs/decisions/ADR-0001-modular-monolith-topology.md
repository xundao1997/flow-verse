# ADR-0001: FlowVerse V1 bootstrap architecture

## Status

Superseded by ADR-0002 on 2026-07-15. The historical decision was accepted by the user on 2026-07-14.

## Context

FlowVerse V1 needs a runnable non-business foundation while product schemas, providers, production scale and deployment ownership remain deferred. The approved product requires singular data ownership and directed dependencies but does not require independently deployed business services.

## Options considered

| Option | Benefits | Costs |
|---|---|---|
| Modular monolith with Web, API and Worker processes | Explicit boundaries, simple transactions, low operational cost | API and Worker release from one backend codebase |
| Independent microservices | Independent scaling and releases | Distributed contracts and operations before supporting evidence exists |
| One synchronous Web/API process | Lowest process count | Does not establish the approved long-running Worker lifecycle |

## Decision

- Use one React Web application and one Python modular-monolith backend codebase running as separate API and Worker processes.
- Use PostgreSQL 18.4 as the only bootstrap stateful service with SQLAlchemy, psycopg and Alembic. The baseline migration creates no business table.
- Reserve an S3-compatible object-storage boundary but select no provider, adapter, container or credentials in this slice.
- Do not add Redis, a broker, microservices, GraphQL, WebSocket, Kubernetes or a separate result service.
- Establish nine behavior-free module boundaries. Cross-module dependencies must use public entry points and remain acyclic.
- Expose only `GET /health/live`, `GET /health/ready` and `GET /health/dependencies`.
- Use bounded PostgreSQL probes, structured JSON logs, request/trace correlation and an OpenTelemetry SDK without an exporter.
- The Worker supports only bounded `--check` execution; it has no business queue or handler.
- Use exact dependency pins and lockfiles. Unpublished or incompatible proposed versions remain blocked until the user selects a valid replacement.

## Trade-offs and consequences

- Independent scaling and provider-specific object storage are deferred.
- PostgreSQL can support future atomic product invariants without inventing the business schema now.
- Health fails honestly when PostgreSQL is unavailable while liveness avoids dependency-driven restart storms.
- Monitoring backend, alerting, production sampling, backup/restore proof and production SLO verification are not claimed.

## Revisit triggers

Revisit only for measured independent scaling or release ownership, a confirmed second implementation, an approved file/provider slice, runtime security support, or a production deployment decision.
