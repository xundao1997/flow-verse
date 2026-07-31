# FlowVerse V1 Technology Stack Registry

## Status Ownership

- Read package state and approved scope from ../intake/V1_PACKAGE_INTAKE.md.
- This file alone owns target-stack, resolved-runtime, and command-state facts.
- Unknown values remain “TBD — do not infer” under ../governance/EVIDENCE_POLICY.md.

## Stack Registry

| Area | Approved target | Target version/range | Exact target evidence | Target status | Resolved installed version | Runtime status |
|---|---|---|---|---|---|---|
| Runtime | CPython for API/Worker; Node.js for Web | Python 3.13.14; Node.js 24.17.0 | User-approved bootstrap versions 2026-07-14; ADR-0002; ADR-0005 | Confirmed | Python 3.13.14 in both service environments; Web lock/build verified with portable Node.js 24.17.0; host default remains 24.13.0 | Confirmed for service verification; host default Conflict |
| Backend / AI language | Python | 3.13.14 | User-approved bootstrap version 2026-07-14 | Confirmed | 3.13.14 | Confirmed |
| Frontend language | TypeScript | 5.9.3 | User-approved completion of diagnostic-bootstrap review issues, 2026-07-20; ADR-0005 | Confirmed | 5.9.3 in `services/web/pnpm-lock.yaml` | Confirmed |
| Frontend framework | React | 19.2.7 | User-approved bootstrap version 2026-07-14; npm registry verification | Confirmed | 19.2.7 in Web lockfile | Confirmed |
| Rendering / meta-framework | SPA; no meta-framework | N/A | ADR-0002 bootstrap scope | N/A | N/A | N/A |
| Build tool | Vite | 8.1.4 | User-approved bootstrap version 2026-07-14; npm registry verification | Confirmed | 8.1.4 in Web lockfile; production build executed 2026-07-21 | Confirmed |
| Package manager | uv for API/Worker; pnpm for Web | uv 0.11.28; pnpm 11.10.0 | User-approved bootstrap versions; service manifests | Confirmed | uv 0.11.28; pnpm 11.10.0; all three service lockfiles present | Confirmed |
| Router | No router in non-business bootstrap | N/A | Bootstrap excludes product navigation | N/A | N/A | N/A |
| Styling and tokens | Deferred to approved product UI slice | N/A for bootstrap | Bootstrap has no product UI | N/A | N/A | N/A |
| UI component system | None | N/A | Minimal bootstrap rule | N/A | N/A | N/A |
| Long-form editor | Deferred | N/A | Explicit bootstrap exclusion | N/A | N/A | N/A |
| Client state | Local diagnostic state only | React built-in state | FV1-DIAGNOSTIC-BOOTSTRAP; ADR-0005 | Confirmed | One request owner with cancellation, stale-response guard and no polling | Confirmed |
| Server/cache data | Redis capability plus local authenticated diagnostic; no business cache/queue consumer | Redis Open Source 8.8.0 | User server-middleware and local diagnostic decisions; ADR-0007/0010 | Confirmed provisioning and diagnostic target; business use N/A | Compose runtime plus bounded dependency-free `AUTH`/`PING` check | Unit and live authenticated diagnostic Confirmed 2026-07-30; business use N/A |
| Messaging / queue | No broker or queue | N/A | ADR-0002 | N/A | N/A | N/A |
| Background jobs / scheduler | Separate long-running Worker HTTP process plus one-shot `--check`; no business queue/scheduler | Python 3.13.14; FastAPI 0.139.0; Uvicorn 0.51.0 | User service-directory and diagnostic decisions; ADR-0002; ADR-0005 | Confirmed | `services/worker` internal status service on port 8001 | Confirmed |
| Resilience / rate limiting | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Forms and validation | TBD — do not infer | TBD | None | Unknown | TBD | Unknown |
| Backend framework | FastAPI / Uvicorn in API and Worker | FastAPI 0.139.0; Uvicorn 0.51.0 | User-approved bootstrap versions; service locks; ADR-0005 | Confirmed | Exact lock versions in both Python services | Confirmed |
| API protocol and schema | REST/OpenAPI operational endpoints only | Public `GET /health/*`, public `GET /api/v1/system/chain`, internal `GET /internal/v1/system/status` | ADR-0002; ADR-0005; contract tests | Confirmed | API/Worker contracts and timeout behavior implemented | Confirmed |
| Database / ORM | PostgreSQL / pgvector / TimescaleDB OSS / SQLAlchemy / Alembic / psycopg | PostgreSQL 18.4; pgvector 0.8.5 image capability; TimescaleDB 2.28.3 OSS image capability; SQLAlchemy 2.0.51; Alembic 1.18.5; psycopg 3.3.4 | User-approved bootstrap, middleware and extension versions; locks; native `FLOWVERSE_DATABASE_URL` contract; ADR-0004/0007/0008 | Confirmed | Python packages and server image source confirmed; target-server custom image built and PostgreSQL reached `healthy`; TimescaleDB is preloaded with bounded workers; no extension/schema is auto-created; Docker unavailable on current host | Client and server configuration Confirmed; one server build/health smoke Confirmed; SQL extension-availability query Unverified |
| Object storage | S3-compatible MinIO capability plus local authenticated diagnostic; no business bucket/user/consumer contract | MinIO `RELEASE.2025-10-15T17-29-55Z`, canonical module `v0.0.0-20251015172955-9e49d5e7a648`, source-built with Go 1.24.8 through a configurable checksum-verified Go Module proxy | User server-middleware and local diagnostic decisions; ADR-0007/0010 | Confirmed provisioning/build/diagnostic target; business use N/A | Existing `httpx` plus standard-library AWS SigV4 performs read-only `ListBuckets`; no new SDK; target server image reached `healthy` | Unit signing/auth path Confirmed; live endpoint reached but rejected the supplied access key on 2026-07-30, so authentication remains Unverified; business use N/A |
| Authentication / authorization | Not implemented in bootstrap | N/A | Explicit exclusion | N/A | N/A | N/A |
| AI provider / SDK / model | Not implemented in bootstrap | N/A | Explicit exclusion | N/A | N/A | N/A |
| Unit / component test | pytest for API/Worker; Vitest for Web | pytest 9.1.1; Vitest 4.1.9 | Service manifests/locks; npm verification | Confirmed | Exact versions installed; API 22 and Worker 6 tests passed 2026-07-30; Web 3 tests passed 2026-07-21 | Confirmed |
| Integration / E2E test | PostgreSQL integration marker; Web E2E deferred | pytest 9.1.1 | API manifest and test source | Confirmed for API integration entry; Web N/A | PostgreSQL environment absent | NotYetAvailable |
| Lint / format / typecheck | Ruff / Pyright; ESLint / Prettier / TypeScript | Ruff 0.15.20; Pyright 1.1.411; ESLint 10.6.0; `@eslint/js` 10.0.1; Prettier 3.9.5; TypeScript 5.9.3 | Service locks; approved diagnostic completion | Confirmed | Exact versions installed and commands passed 2026-07-21 | Confirmed |
| Performance tooling | Vite production build size and duration output | Vite 8.1.4 | Web manifest/lock and performance budget | Confirmed bootstrap measurement | Current build: JS 195.52 kB / 62.22 kB gzip; CSS 4.76 kB / 1.65 kB gzip; HTML 0.63 kB / 0.43 kB gzip | Confirmed local build baseline; field metrics Unverified |
| CI/CD and deployment | Native local three-service test entry plus independent server middleware Compose; no CI/CD control plane or application production deployment selected | PowerShell locally; Docker Engine 29.6.x and Compose plugin v2.24+ for server middleware | User instructions 2026-07-21/22; ADR-0006/0007 | Confirmed local and middleware targets; application production target Unknown | Local wrapper and server middleware configuration present; user-supplied target-server output shows the three middleware containers healthy | Local runtime and middleware repository conformance Confirmed; one middleware server smoke Confirmed; CI/CD/application production Unknown |
| Deployment topology / orchestrator | Local native Web/API/Worker processes; one single-host Compose project for PostgreSQL/Redis/MinIO only; application production topology Unknown | Windows processes locally; Docker Compose on the middleware server | User instructions; ADR-0004/0005/0006/0007 | Confirmed local and server-middleware targets | `deploy/local/start.ps1` and `deploy/server/middleware/compose.yml` have disjoint ownership; target server ran exactly three healthy middleware containers | Local conformance and one middleware runtime smoke Confirmed; long-duration operations and application production remain Unverified/N/A until selected |
| Developer middleware access | Local-only SSH forwarding plus ignored-environment configuration and authenticated PostgreSQL/Redis/MinIO diagnostic; no middleware public bind | Windows OpenSSH client; existing Python API runtime | User local-development instructions 2026-07-24/29; ADR-0007/0010 | Confirmed for development diagnostic; business Redis/MinIO use N/A | Tunnel helper, secure prompt configurator and registered `middleware-check` mode; no credential output or new package | Repository conformance, live forwarding, PostgreSQL and Redis authentication Confirmed; MinIO authentication Unverified |
| Logging / metrics / tracing | structlog JSON + OpenTelemetry SDK without exporter | structlog 26.1.0; OTel 1.43.0 | Service locks; ADR-0002 | Confirmed | Exact versions installed in API/Worker | Confirmed |
| Monitoring / observability | Correlated logs and local spans only | Exporter/backend/alerts N/A for bootstrap | ADR-0002 | Confirmed bootstrap boundary | request_id/trace_id verified; no backend | Confirmed boundary; production monitoring deferred |

Target status values: Proposed, Confirmed, Conflict, Unknown, N/A.

The approved product/UIUX package supplies design identifiers, example routes, example request names, and TypeScript shapes. They are reference inputs, not approved runtime, API, schema, dependency, or executable-command evidence.

Proposed records a user-indicated direction but is not sufficient for bootstrap or business implementation until the V1 package or an explicit user decision confirms the exact target and version/range.

Runtime status values: Confirmed, NotYetInstalled, Unknown, Conflict, N/A.

## Confirmed direct dependency pins

| Service | Direct pins |
|---|---|
| API | Python 3.13.14; FastAPI 0.139.0; Uvicorn 0.51.0; Pydantic 2.13.4; pydantic-settings 2.14.2; SQLAlchemy 2.0.51; Alembic 1.18.5; psycopg 3.3.4; structlog 26.1.0; OpenTelemetry 1.43.0; httpx 0.28.1; pytest 9.1.1; Ruff 0.15.20; Pyright 1.1.411 |
| Worker | Python 3.13.14; FastAPI 0.139.0; Uvicorn 0.51.0; Pydantic 2.13.4; pydantic-settings 2.14.2; SQLAlchemy 2.0.51; psycopg 3.3.4; structlog 26.1.0; OpenTelemetry 1.43.0; httpx 0.28.1; pytest 9.1.1; Ruff 0.15.20; Pyright 1.1.411 |
| Web | Node.js 24.17.0; pnpm 11.10.0; React 19.2.7; React DOM 19.2.7; Vite 8.1.4; TypeScript 5.9.3; ESLint 10.6.0; `@eslint/js` 10.0.1; typescript-eslint 8.63.0; Prettier 3.9.5; Vitest 4.1.9 |

## Command Registry

| Task | Approved exact command | Working directory | Exact evidence | Evidence status | Execution status |
|---|---|---|---|---|---|
| API install | `uv sync --project services/api --python 3.13.14` | Repository root | API manifest/lock; executed with exact local uv 0.11.28 path on 2026-07-15 | Confirmed | Available after uv installation |
| Worker install | `uv sync --project services/worker --python 3.13.14` | Repository root | Worker manifest/lock; executed with exact local uv 0.11.28 path on 2026-07-15 | Confirmed | Available after uv installation |
| Web install | `corepack pnpm@11.10.0 --dir services/web install --frozen-lockfile` | Repository root | Web manifest/lock; executed with Node 24.17.0 and pnpm 11.10.0 on 2026-07-21 | Confirmed | Available with exact Node runtime |
| API development | `.venv\Scripts\python.exe ..\..\scripts\run_uvicorn.py flowverse_api.api.main:app --app-dir src --host 127.0.0.1 --port 8000` | `services/api` | API manifest/source and Windows psycopg-compatible launcher; executed with ready PostgreSQL probe 2026-07-30 | Confirmed | Available |
| Worker check | `..\.venv\Scripts\python.exe -m flowverse_worker --check` | `services/worker/src` | Worker source; executed 2026-07-15 | Confirmed | Available; requires database configuration for success exit |
| Native local preflight | `powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1 preflight` | Repository root | User decision 2026-07-16; ADR-0004; executed 2026-07-16 | Confirmed | Available |
| Native local API | `powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1 api` | Repository root | User decision 2026-07-16; ADR-0004; executed with health probes 2026-07-16 | Confirmed | Available after API install |
| Native local Worker | `powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1 worker` | Repository root | ADR-0005; Worker HTTP source and script | Confirmed | Available after Worker install |
| Native local Worker check | `powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1 worker-check` | Repository root | User decision 2026-07-16; ADR-0004; configuration-failure path executed 2026-07-16 | Confirmed | Available after Worker install; requires database configuration for success; not a daemon |
| Native local Web | `powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1 web` | Repository root | ADR-0004/0005; Web source/lock and script | Confirmed | Available with Node.js 24.17.0 |
| Native local full stack | `powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1 all` | Repository root | ADR-0005; script preflight 2026-07-21 | Confirmed | Available with three service runtimes; PostgreSQL configuration required for a fully-ready chain |
| Local test deployment | `powershell -ExecutionPolicy Bypass -File deploy/local/start.ps1` | Repository root | User instruction 2026-07-21; ADR-0006; local wrapper | Confirmed | Available; defaults to `all` and accepts every native launcher mode |
| Local middleware tunnel validation | `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File deploy/local/start-middleware-tunnel.ps1 -Server example.com -SshUser test-user -ValidateOnly` | Repository root | User local-development instruction 2026-07-24; tunnel script and runbook | Confirmed | Available; passed without opening a network connection 2026-07-24; live use requires an operator-supplied SSH host/user and optional identity file |
| Local middleware authentication check | `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File deploy/local/start.ps1 middleware-check` | Repository root | User local middleware diagnostic instruction 2026-07-29; ADR-0010; launcher and tests | Confirmed | Available after the ignored root `.env` is configured; failure path Passed; PostgreSQL and Redis live authentication Passed; MinIO credentials require correction |
| Server middleware one-command deployment | `bash deploy/server/middleware/start.sh` | Repository root | User instruction 2026-07-22; middleware Compose and runbook | Confirmed | Available on the target server; corrected component build/start path Passed, exact updated one-command rerun Unverified; Docker absent locally |
| Server middleware config validation | `docker compose config --quiet` | `deploy/server/middleware` | User instructions 2026-07-22; ADR-0007/0008; Compose source | Confirmed | Passed on the target server before the successful build; NotYetAvailable locally |
| Server middleware image build | `docker compose build --pull` | `deploy/server/middleware` | User instructions 2026-07-22/23; ADR-0007/0008; PostgreSQL-extension and deterministic MinIO inline Compose recipes | Confirmed | Passed on the target server for the corrected PostgreSQL and MinIO images; NotYetAvailable locally |
| Server middleware start and health | `docker compose up -d --wait --wait-timeout 300` then `docker compose ps` | `deploy/server/middleware` | User instructions 2026-07-22; ADR-0007/0008; middleware runbook | Confirmed | Target-server `docker ps` reported PostgreSQL, Redis and MinIO healthy in one smoke observation; NotYetAvailable locally |
| PostgreSQL extension availability | `set -a; . ./.env; set +a; docker compose exec -T postgres psql -U "$FLOWVERSE_POSTGRES_USER" -d "$FLOWVERSE_POSTGRES_DB" -c "SELECT name, default_version FROM pg_available_extensions WHERE name IN ('timescaledb', 'vector') ORDER BY name;"` | `deploy/server/middleware` | User extension instruction 2026-07-22; ADR-0008; middleware runbook | Confirmed | Available on the target server but not yet executed; must report timescaledb 2.28.3 and vector 0.8.5 without creating either extension |
| Web lint / format | `corepack pnpm@11.10.0 --dir services/web run lint` / `corepack pnpm@11.10.0 --dir services/web run format:check` | Repository root | Web manifest/lock; executed 2026-07-21 | Confirmed | Available with Node.js 24.17.0 |
| Web typecheck | `corepack pnpm@11.10.0 --dir services/web run typecheck` | Repository root | Web manifest/lock; executed 2026-07-21 | Confirmed | Available with Node.js 24.17.0 |
| Web unit test | `corepack pnpm@11.10.0 --dir services/web run test` | Repository root | Web manifest/tests; 3 tests passed 2026-07-21 | Confirmed | Available with Node.js 24.17.0 |
| Web production build | `corepack pnpm@11.10.0 --dir services/web run build` | Repository root | Web manifest/lock; executed 2026-07-21 | Confirmed | Available with Node.js 24.17.0 |
| API lint / format | `.venv\Scripts\ruff.exe check --no-cache .` / `.venv\Scripts\ruff.exe format --check --no-cache .` | `services/api` | API manifest; executed 2026-07-15 | Confirmed | Available |
| Worker lint / format | `.venv\Scripts\ruff.exe check --no-cache .` / `.venv\Scripts\ruff.exe format --check --no-cache .` | `services/worker` | Worker manifest; executed 2026-07-15 | Confirmed | Available |
| API typecheck | `.venv\Scripts\pyright.exe` | `services/api` | API manifest; executed 2026-07-15 | Confirmed | Available |
| Worker typecheck | `.venv\Scripts\pyright.exe` | `services/worker` | Worker manifest; executed 2026-07-15 | Confirmed | Available |
| API unit test | `.venv\Scripts\pytest.exe -p no:cacheprovider -m "not integration"` | `services/api` | API manifest/tests; executed 2026-07-15 | Confirmed | Available |
| Worker unit test | `.venv\Scripts\pytest.exe -p no:cacheprovider` | `services/worker` | Worker manifest/tests; executed 2026-07-15 | Confirmed | Available |
| PostgreSQL integration test | `.venv\Scripts\pytest.exe -p no:cacheprovider -m integration` | `services/api` | API integration test | Confirmed | NotYetAvailable: PostgreSQL/Docker absent |
| Alembic migration-head check | `.venv\Scripts\alembic.exe heads` | `services/api` | API manifest/config/migration source | Confirmed | Available; database connection not required |
| E2E test | N/A for non-business bootstrap | N/A | No product UI | N/A | N/A |
| Architecture / dependency check | `python scripts\check_architecture.py` | Repository root | ADR-0002 and script; executed 2026-07-15 and 2026-07-16 | Confirmed | Available |
| Architecture checker self-test | `python -m unittest scripts.test_check_architecture` | Repository root | Checker tests; 5 tests passed 2026-07-21 | Confirmed | Available |
| Contract compatibility check | `.venv\Scripts\pytest.exe -p no:cacheprovider tests\unit\test_health.py` | `services/api` | API health contract tests | Confirmed | Available |
| Reliability / failure test | API and Worker unit commands above plus real degraded API startup | Service directories / repository root | Tests and execution evidence 2026-07-15 | Confirmed | Available except real PostgreSQL path |
| Technical-debt reference check | TBD — do not infer | TBD | None | Unknown | NotYetAvailable |
| Performance test | `corepack pnpm@11.10.0 --dir services/web run build` | Repository root | Web build output and Performance Budget | Confirmed bootstrap measurement | Available; field performance remains Unverified |

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
