# ADR-0010: Local middleware authentication check

- Status: Accepted
- Date: 2026-07-29
- Scope: FV1-LOCAL-MIDDLEWARE-DIAGNOSTIC
- Supersedes: The application-consumer exclusion in FV1-REMOTE-MIDDLEWARE-DEV for this diagnostic only

## Context

Native Windows development can already open loopback-only SSH forwards to the server PostgreSQL, Redis and MinIO ports. The API and Worker use PostgreSQL for readiness, but the repository had no safe local command that configured and authenticated all three middleware connections. Port reachability alone cannot prove that the selected credentials work.

This architecture check must not invent cache keys, queues, buckets, object-retention rules, schemas or production application accounts. It also must not add a second service launcher, publish server ports, print credentials or require a new client dependency.

## Decision

- `deploy/local/configure-middleware.ps1` securely prompts for the three server credentials, URL-escapes the PostgreSQL password and writes the values only to the ignored root `.env` file. Existing non-middleware environment entries are preserved.
- `deploy/local/start.ps1 middleware-check` delegates to the single native launcher owner in `scripts/start-local.ps1`.
- The API health package owns the non-business diagnostic implementation and reuses the existing PostgreSQL probe. Redis is checked with bounded `AUTH` and `PING` commands. MinIO is checked with a read-only, AWS Signature V4 `ListBuckets` request. The response bodies, bucket names and credentials are never printed.
- The three checks run concurrently with a three-second default and ten-second configuration maximum, have no automatic retry and return a non-zero process exit when any check is not ready.
- MinIO root credentials are accepted only for this bootstrap diagnostic. Future application use requires an approved least-privilege user, bucket and object contract.

## Consequences

- A developer can distinguish successful authenticated access from an open local tunnel without installing PostgreSQL, Redis or MinIO locally.
- The ignored `.env` contains plaintext development credentials and must remain local, access-controlled and uncommitted.
- Redis cache/queue use and MinIO business object operations remain unimplemented. No business dependency edge or data owner is created.

## Verification

Run API lint, format, type checks and unit tests, parse all affected PowerShell scripts, run the registered middleware check without credentials to verify truthful failure, then run it with operator-supplied credentials while the SSH tunnel is open. A complete live result requires all three services to report `ready`.
