# FlowVerse server middleware

This directory provisions exactly three single-server middleware services for the FlowVerse V1/second-stage environment. It does not start the Web, API, or Worker and does not replace the native local entry under `deploy/local`.

## Selected versions

| Service | Version | Purpose |
|---|---:|---|
| PostgreSQL | 18.4 | Authoritative relational data store |
| pgvector | 0.8.5, built into PostgreSQL | Future simple-RAG vector capability; no extension, dimension, index or schema is created automatically |
| TimescaleDB OSS | 2.28.3, built into PostgreSQL | Future stock/time-series capability; no extension, hypertable or policy is created automatically |
| Redis Open Source | 8.8.0 | Non-authoritative cache/runtime state capability; no application consumer is wired yet |
| MinIO | `RELEASE.2025-10-15T17-29-55Z`, built from source | S3-compatible object storage capability; no application consumer or bucket is created yet |

TimescaleDB is compiled from its official 2.28.3 source with `APACHE_ONLY=1`; licensed Timescale features are intentionally excluded. Both PostgreSQL extensions are built in a separate stage while the runtime remains `postgres:18.4-bookworm`. MinIO's repository is archived and the selected tag is its last published security-fix release. Redis 8 uses a tri-license and MinIO is AGPLv3. Complete operational maintenance and license review before treating this single-host setup as production-ready.

## Initial server capacity plan

For middleware-only architecture testing and light data, use at least 4 vCPU, 8 GiB RAM, and 1 TiB of reliable SSD/NVMe storage. Use 8 vCPU and 16 GiB RAM or more before co-locating application services or running concurrent RAG ingestion, stock-data import, vector indexing, backup, or compaction workloads.

| Service | CPU limit | Memory reservation / limit | Persistent-volume capacity plan |
|---|---:|---:|---:|
| PostgreSQL | 2 CPU | 1 GiB / 2 GiB | 300 GiB |
| Redis | 1 CPU | 512 MiB / 1 GiB | 20 GiB |
| MinIO | 1 CPU | 512 MiB / 1 GiB | 500 GiB |

Compose enforces CPU and memory limits, but Docker named volumes do not have a portable Compose disk-quota setting. The capacity labels in `compose.yml` are documentation, not enforcement. Provision the Docker data root or three backing volumes on appropriately sized host partitions/LVM volumes, keep at least 15% free space, and configure disk alerts before storing real data.

This lightweight profile also limits PostgreSQL to 50 connections, 512 MiB of shared buffers, six worker processes and two TimescaleDB background workers. Redis `maxmemory` is 512 MiB so AOF and process overhead remain below its 1 GiB container limit. These are bootstrap boundaries, not measured production sizing; observe container memory, database connections and ingestion behavior before increasing workload. First-time BuildKit compilation is outside these runtime limits and may require temporary host headroom.

## One-command start

Run this command from the repository root on the Linux server:

```bash
bash deploy/server/middleware/start.sh
```

The script creates `.env` from `.env.example` only when `.env` is absent, generates only missing or empty secret files, validates the Compose model, builds the pinned PostgreSQL and MinIO images from the inline recipes in `compose.yml`, starts all three services, and waits up to 300 seconds for their health checks. It never prints or replaces a non-empty existing secret. Set `FLOWVERSE_WAIT_TIMEOUT_SECONDS` in the shell before running the command if the first source build needs a longer health wait.

The first run downloads base images and compiles pgvector, TimescaleDB and MinIO, so it can take substantially longer than later cached builds. The build context is empty by design through `.dockerignore`; secret files and repository content are not sent to the image builder.

The MinIO builder resolves the release tag to its fixed canonical module version `v0.0.0-20251015172955-9e49d5e7a648`, downloads that exact module through `FLOWVERSE_GO_PROXY`, and builds from the downloaded module directory with the release metadata explicitly injected. This avoids a VCS or `direct` fallback and the unrelated deprecated-version lookup performed by `go install @version`. The proxy defaults to the Aliyun Go Module mirror confirmed reachable from the target server, while `FLOWVERSE_GO_SUMDB=sum.golang.org` keeps module checksum verification enabled. These values affect only the disposable builder stage and are not present in the MinIO runtime image. Override the proxy in the untracked `.env` only when another environment requires a different trusted module proxy; do not disable `GOSUMDB`.

Redis starts its small configuration wrapper as root only long enough to read the root-only Compose secret and create a protected temporary configuration file. The wrapper then delegates to the image's official entrypoint, which fixes `/data` ownership when required and drops the Redis server process to the `redis` user. Do not make `secrets/redis_password` world-readable and do not add a Compose-level `user: redis`, because either change breaks this security and startup contract.

## Manual secret preparation (optional)

Run these commands on the Linux server from this directory. They create values without placing them in tracked configuration:

```bash
cp .env.example .env
umask 077
openssl rand -base64 48 | tr -d '\n' > secrets/postgres_password
openssl rand -base64 48 | tr -d '\n' > secrets/redis_password
openssl rand -hex 16 | tr -d '\n' > secrets/minio_root_user
openssl rand -base64 48 | tr -d '\n' > secrets/minio_root_password
chmod 600 \
  secrets/postgres_password \
  secrets/redis_password \
  secrets/minio_root_user \
  secrets/minio_root_password
```

Do not use the generated MinIO root account from applications. Create a dedicated least-privilege application user after the service is healthy; that policy is intentionally not invented in this bootstrap.

## Manual validation and start

The server target is Docker Engine 29.6.x with Docker Compose plugin v2.24 or newer:

```bash
docker compose config --quiet
docker compose build --pull
docker compose up -d --wait --wait-timeout 300
docker compose ps
```

Both custom image recipes live inside `compose.yml`; there are no independent middleware Dockerfiles to invoke or keep in sync.

All published ports bind to `127.0.0.1` by default. Keep them private and use a firewall, SSH tunnel, or a separately approved TLS proxy instead of changing the bind address to a public interface. Future application containers may join the explicit `flowverse_middleware` network after their connection contracts are approved.

Stop the services without deleting data:

```bash
docker compose down
```

Never run `docker compose down -v` during routine deployment or rollback: `-v` permanently removes the named data volumes. Keep this deployment directory, including `compose.yml`, the untracked `.env`, `start.sh`, and all four secret files; running containers may survive its deletion temporarily, but later restart, recreation, upgrade, and recovery would fail. Backups, restore drills, TLS, monitoring, high availability, bucket/user provisioning, `CREATE EXTENSION vector`, `CREATE EXTENSION timescaledb`, and application connection strings remain separate approved work owned by future migrations.

## Runtime checks

`docker compose ps` must report all three containers as healthy. If not, inspect bounded log output without printing secret files:

```bash
docker compose logs --tail=200 postgres
docker compose logs --tail=200 redis
docker compose logs --tail=200 minio
```

After the PostgreSQL image is healthy, verify that both extension binaries are available without changing any database schema. These commands load only the non-secret `.env` values:

```bash
set -a
. ./.env
set +a
docker compose exec -T postgres psql \
  -U "$FLOWVERSE_POSTGRES_USER" \
  -d "$FLOWVERSE_POSTGRES_DB" \
  -c "SELECT name, default_version FROM pg_available_extensions WHERE name IN ('timescaledb', 'vector') ORDER BY name;"
```

The expected available versions are TimescaleDB 2.28.3 and vector 0.8.5. pgvector provides vector similarity search for RAG; TimescaleDB is prepared for market time-series data and is not required for RAG itself.

The current development workstation has no Docker runtime, so repository checks validate this configuration statically. On 2026-07-23, user-supplied target-server output confirmed that the corrected PostgreSQL and MinIO images built and that PostgreSQL, Redis, and MinIO all reached Docker `healthy` state. This is one deployment smoke result, not evidence for extension activation, long-duration stability, workload capacity, backup/restore, TLS, monitoring, or high availability.
