# ADR-0007: Single-server middleware Docker Compose

- Status: Partially superseded by ADR-0008
- Decision date: 2026-07-22
- Scope: FV1-SERVER-MIDDLEWARE-DEPLOY
- Decision owner: User
- Related: ADR-0002, ADR-0004, ADR-0005, ADR-0006
- Supersedes: The remote middleware-target Unknown in ADR-0006 only; native local application startup remains unchanged

## Context

The user needs the second-stage server prepared before application business work begins and explicitly selected PostgreSQL, Redis, and MinIO. The existing `deploy/local` path is a native Windows test entry and must remain Docker-free. The supplied Compose file demonstrates the desired operational shape but contains hard-coded credentials and different middleware.

FlowVerse still has no approved business schema, cache contract, object-storage contract, RAG ingestion contract, application production topology, backup policy, or high-availability target. The selected server middleware must therefore be provisioned as capability without inventing business consumers or authoritative data flows.

## Options considered

1. Install all three services directly on the host. This reduces container layers but makes repeatable versioning, resource isolation, and recovery documentation host-specific.
2. Run three independently managed containers. This keeps container isolation but scatters the shared network, secret, volume, health, and lifecycle contract.
3. Use one server-only Docker Compose project for exactly PostgreSQL, Redis, and MinIO. This provides one auditable configuration while remaining separate from native local application startup.
4. Add Elasticsearch/OpenSearch or TimescaleDB now. No approved current consumer or measured need exists, so this adds operational cost without evidence.

## Decision

Use option 3 under `deploy/server/middleware`:

- PostgreSQL 18.4 is the authoritative relational store. pgvector 0.8.5 is compiled into its image for the confirmed future RAG variation, but no extension or schema is created automatically.
- Redis Open Source 8.8.0 is a non-authoritative runtime capability. AOF uses `everysec`; the `noeviction` policy fails writes explicitly at capacity instead of silently evicting coordination data. No application dependency is yet approved.
- MinIO is built from the exact `RELEASE.2025-10-15T17-29-55Z` security-fix source tag because the available older prebuilt release does not contain that fix. It provides only an S3-compatible capability; users, buckets, retention, and application contracts remain deferred.
- Secret values live only in untracked server files mounted through Compose secrets. They are absent from Compose, `.env.example`, image layers, and repository documentation.
- Ports bind to loopback by default. Containers use named persistent volumes, health checks, bounded local logs, restart policies, process limits, and explicit CPU/memory limits.
- Initial disk capacities are operational targets enforced by host storage provisioning, because portable Compose files cannot enforce named-volume disk quotas.
- Docker Engine 29.6.x and Compose plugin v2.24+ are the target server runtime. This is a single-host bootstrap, not evidence of production readiness or high availability.

## Consequences

Positive consequences are repeatable versions, clear secret isolation, truthful resource boundaries, and a future path for RAG without a separate vector database. Elasticsearch/OpenSearch and TimescaleDB remain excluded until search/analytics evidence confirms them.

Trade-offs are a source build for MinIO, single-host failure exposure, operator-owned host disk provisioning, and added license/maintenance review. MinIO's archived upstream and Redis/MinIO license terms must be accepted operationally before production. Backups, restore drills, TLS, monitoring, application credentials, schema migrations, and successful server execution remain Unverified and require follow-up scopes.

## Verification and recovery

Static verification includes Compose/config review, secret scanning, architecture checks, and documentation consistency. On the target server, run `docker compose config --quiet`, build the pinned images, start the project, and require three healthy services. The current workstation has no Docker, so runtime conformance is Unverified.

Routine recovery uses `docker compose down` and preserves named volumes. Never use `down -v` as rollback. If this decision is replaced, create a superseding ADR, stop only these containers, preserve all data volumes, and migrate or restore data through a separately approved plan.
