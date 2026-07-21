# ADR-0004: Native local startup and Yunxiao host Docker delivery

## Status

Accepted by the user on 2026-07-16. Supersedes the local Compose boundary in
ADR-0002 and resolves the production-runtime target left Unknown by ADR-0003.

## Context

The service-directory bootstrap initially supplied a Compose file for local
integration. The user has clarified two distinct execution environments:

- Local development starts the service processes directly and does not use
  Docker or Docker Compose.
- Cloud delivery uses Yunxiao. Production hosts run the built ACR images
  directly with Docker rather than Compose or Kubernetes.

API can already run as a native Python process. Worker currently exposes only a
one-shot dependency check. Web has no source tree or lockfile and its manifest
contains unresolved dependency versions. PostgreSQL is required but no local or
production provisioning owner has been selected.

## Options considered

| Option | Benefits | Costs |
|---|---|---|
| Keep Compose for local development | One command can describe several processes | Contradicts the explicit local-development decision and makes Docker a local prerequisite |
| Native local processes with an external PostgreSQL connection | Matches the developer environment; service failures and logs remain direct | Developers must provide PostgreSQL and start ready services explicitly |
| Use the production host-Docker path locally | Maximum environment similarity | Requires Docker locally and contradicts the selected boundary |

## Decision

- Remove root `compose.yaml`; it is not a supported local or production entry.
- Local startup uses `scripts/start-local.ps1` and the service-native tools.
  The script loads an optional root `.env` without printing values and never
  replaces an environment variable already set in the process.
- API starts in the foreground on the confirmed Uvicorn command. Worker retains
  the accurately named `worker-check` command until a real long-running worker
  contract exists. Web startup fails with an actionable message until its
  dependency decision, source and lockfile are resolved.
- PostgreSQL is supplied independently and reached through
  `FLOWVERSE_DATABASE_URL`; this decision does not select installation,
  managed-service, backup or production ownership.
- Service Dockerfiles remain because Yunxiao Flow builds Web/API/Worker images
  and publishes them to ACR.
- The production deployment target is Yunxiao Flow `VMDockerDeploy` against
  managed host groups whose machines have Docker installed. Production does not
  use Compose, ACK or SAE.
- Do not create an executable host deployment job until the Web image, Worker
  daemon entry, production database/configuration, host groups, ports,
  health-check and rollback behavior are confirmed. A required deployment
  script must not be replaced by a fake or one-shot `docker run` success.

## Trade-offs and consequences

- Local development has no Docker dependency and each process exposes its own
  logs and exit code.
- There is not yet a one-command full-stack start because two of three code
  services do not have valid long-running native contracts.
- Local and production execution differ. Service-native checks plus future
  image/host smoke tests must cover that gap.
- Removing Compose also removes an in-repository PostgreSQL provisioning
  shortcut; readiness remains degraded until a developer supplies a database.
- The confirmed production component is precise, but cloud conformance remains
  Unverified until a host group and deployment run exist.

## Revisit triggers

- Web obtains an approved manifest, lockfile, source and production command.
- Worker obtains an approved long-running delivery/consumption contract.
- PostgreSQL provisioning and secret delivery are confirmed for local and
  production environments.
- Host-group health, rollout and rollback controls are approved and tested.
