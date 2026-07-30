# ADR-0009: Lightweight server middleware capacity defaults

- Status: Accepted
- Decision date: 2026-07-23
- Scope: FV1-SERVER-MIDDLEWARE-DEPLOY / FV1-SERVER-DATA-EXTENSIONS
- Decision owner: User
- Related: ADR-0007, ADR-0008
- Supersedes: The original runbook capacity defaults under ADR-0007 and the initial PostgreSQL/TimescaleDB worker-cap values in ADR-0008 only

## Context

The original single-host plan reserved substantial headroom for later application and data workloads. The user has explicitly requested smaller middleware defaults for the current architecture deployment test. The prior manual edit created invalid relationships: PostgreSQL shared buffers and Redis `maxmemory` exceeded their container limits, MinIO reserved 512 GiB against a 1 GiB limit, and `.env.example` still overrode the edited Compose fallbacks with the old profile.

This decision changes only configurable resource defaults. It does not change middleware versions, service topology, data ownership, secrets, ports, volumes, disk plans, extension activation, application dependencies, or production-readiness claims.

## Decision

Use one consistent lightweight profile in both `compose.yml` fallbacks and `.env.example`:

- PostgreSQL: 2 CPU, 1 GiB reservation, 2 GiB limit, 512 MiB shared buffers, 50 connections, six worker processes and two TimescaleDB background workers.
- Redis: 1 CPU, 512 MiB reservation, 1 GiB limit and 512 MiB `maxmemory`, retaining AOF `everysec` and `noeviction`.
- MinIO: 1 CPU, 512 MiB reservation and 1 GiB limit.
- The middleware-only test host baseline is at least 4 vCPU and 8 GiB RAM. Use at least 8 vCPU and 16 GiB RAM before co-locating application services or running concurrent ingestion, indexing, backup or compaction work.

All values remain overridable through the untracked server `.env`. The existing 300/20/500 GiB named-volume capacity plan remains documentation rather than a portable quota. BuildKit source compilation is outside service runtime limits and requires separate transient host headroom.

## Consequences

The profile is internally consistent and reduces idle host allocation for architecture verification. It also reduces concurrency and cache headroom; Redis will reject writes at its explicit limit, PostgreSQL may saturate its connection/worker bounds, and MinIO can become memory constrained during heavier object activity. No production throughput, latency, RAG scale, stock-ingestion scale, backup window, RTO or RPO is established.

## Verification and recovery

Static verification must confirm that reservations do not exceed hard limits, PostgreSQL shared buffers remain below its limit, Redis `maxmemory` remains below its limit, both configuration sources match, and the existing three-service/secret/volume contracts remain unchanged. The target server must still pass Compose validation, image build and three-service health checks.

If observation shows pressure, raise values in the untracked `.env` and recreate the affected containers without `-v`. Named volumes and data remain intact; resource rollback never requires volume deletion.
