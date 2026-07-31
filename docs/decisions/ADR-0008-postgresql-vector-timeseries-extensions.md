# ADR-0008: PostgreSQL vector and time-series extension bundle

- Status: Accepted
- Decision date: 2026-07-22
- Scope: FV1-SERVER-DATA-EXTENSIONS
- Decision owner: User
- Related: ADR-0002, ADR-0007
- Supersedes: The TimescaleDB exclusion in ADR-0007 only; the three-container middleware topology remains unchanged

## Context

ADR-0007 prepared PostgreSQL with pgvector for future RAG and deferred TimescaleDB until a confirmed need existed. The user has now explicitly requested pgvector and TimescaleDB together so the same server can support simple RAG and the later stock stage. Both technologies are PostgreSQL extensions; deploying TimescaleDB as a second database container would create another data authority, duplicate operations, and complicate joins and transactions without evidence.

No RAG ingestion schema, embedding dimension, vector index, market-data schema, hypertable, retention policy, compression policy, or application consumer is approved yet. Packaging extension binaries must not silently create those contracts.

## Options considered

1. Keep pgvector only and defer TimescaleDB. This preserves the current image but ignores the newly confirmed stock/time-series requirement.
2. Add a separate TimescaleDB service beside PostgreSQL. This duplicates the database control plane and creates an unapproved cross-database ownership boundary.
3. Package pgvector and TimescaleDB OSS in the existing PostgreSQL image, preload TimescaleDB, and let future approved migrations create extensions and domain schemas.
4. Add a dedicated vector database or pgvectorscale now. Simple RAG has no measured need for another store or vector acceleration layer.

## Decision

Use option 3 while retaining exactly three middleware containers:

- PostgreSQL remains version 18.4 and the sole relational authority.
- TimescaleDB 2.28.3 OSS is selected because it is the current stable bug-fix release with PostgreSQL 18 support. It is compiled with `APACHE_ONLY=1` so Timescale License features are not included.
- pgvector remains fixed at 0.8.5. Both extensions are built in an isolated stage and copied into the existing `postgres:18.4-bookworm` runtime, preserving its Debian/glibc and data-volume compatibility baseline.
- `shared_preload_libraries=timescaledb` prepares PostgreSQL for later activation. Timescale telemetry is disabled, automatic tuning is disabled in favor of the explicit Compose resource configuration, and TimescaleDB background workers are initially capped at four within eight PostgreSQL worker processes.
- No upstream initialization script is copied into the runtime image. Neither `vector` nor `timescaledb` is automatically created in any database. Future Alembic migrations own `CREATE EXTENSION`, tables, hypertables, indexes, dimensions, retention, compression, upgrade order, and rollback evidence.
- pgvector is the simple-RAG capability. TimescaleDB is the stock/time-series capability; it is not required for vector similarity search.

## Consequences

Positive consequences are one PostgreSQL operational boundary, transactional joins between future relational/vector/time-series data, no fourth service, and early availability of both confirmed extension variations.

Trade-offs are a longer source-build step, a preload-time memory/process cost, and coupled PostgreSQL/extension upgrade testing. Backup and restore must preserve compatible extension binaries before restoring schemas that depend on them. The image build depends on the tagged TimescaleDB and pgvector sources. No RAG or stock performance claim is established without representative data and measurements.

## Verification and recovery

Static verification confirms exact versions, exactly three Compose services, TimescaleDB preload limits, removal of automatic extension creation, and absence of secrets. The target server must build the image, require all containers healthy, and query `pg_available_extensions` for `vector` 0.8.5 and `timescaledb` 2.28.3 before any schema migration.

The current host has no Docker, so build/runtime conformance remains Unverified. Container rollback may rebuild the previous image while preserving the PostgreSQL volume only before either extension is created. After extension-backed schemas exist, downgrade or removal requires an approved database migration/restore plan and must never be attempted by deleting the volume.
