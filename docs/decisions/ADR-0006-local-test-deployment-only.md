# ADR-0006: Local native test deployment only

## Metadata

| Field | Value |
|---|---|
| Status | Accepted |
| Decision owner | User |
| Date | 2026-07-21 |
| Scope IDs | FV1-LOCAL-TEST-DEPLOY / FV1-LOCAL-RUNTIME |
| Evidence | User instruction to remove the Yunxiao deployment directory and add a local startup/deployment script for testing, 2026-07-21 |
| Supersedes | ADR-0003; the Yunxiao/production-delivery portions of ADR-0004 and ADR-0005 |

## Context

- The repository had a Yunxiao Flow template, ACR image-build contract and host Docker deployment script, but no bound organization, service connection, registry or host evidence.
- The current need is local architecture testing, not cloud or production delivery.
- Local development is already required to run Web, API and Worker as native processes without Docker.
- Keeping an unbound cloud template as the active deployment entry adds concepts and maintenance work that do not help current testing.

## Options

| Option | Benefits | Costs / risks | Selected |
|---|---|---|---|
| Keep Yunxiao beside local startup | Preserves a future cloud starting point | Continues to expose an unused and unverified current deployment path | No |
| Replace the active deployment entry with a local native wrapper | One test command, no duplicate orchestration, matches the current environment | No current production deployment target | Yes |
| Add local Docker or Compose deployment | More production-like process isolation | Contradicts the approved native-local requirement and adds unnecessary runtime dependencies | No |

## Decision

- Remove `deploy/yunxiao` and its Flow, ACR and host Docker implementation files.
- Add `deploy/local/start.ps1` as the stable local test deployment entry. It delegates to `scripts/start-local.ps1`, whose default full-stack mode remains `all`.
- Local deployment remains native and Docker-free. Web runs in the foreground; API and Worker are bounded child processes and are cleaned up on exit.
- No CI/CD control plane or production deployment topology is currently selected. Any future cloud or production delivery requires a new approved decision and executable evidence.
- Service Dockerfiles remain packaging artifacts only; they are not part of the active local test command or an approved production deployment target.

## Consequences

### Positive

- Testers see one deployment directory and one command aligned with their actual environment.
- The wrapper reuses the verified launcher, so environment loading, ports, health waits, logs and cleanup have one owner.
- No cloud identifiers, credentials, Docker daemon or network are required for local architecture checks.

### Negative

- The repository no longer contains a ready-to-bind cloud pipeline template.
- Image promotion, production rollout and production rollback are deferred until a production target is selected.

## Reliability, Performance and Recovery

- Missing runtimes or lockfiles fail during preflight/startup rather than reporting success.
- The optional root `.env` does not override process-level variables and its values are not printed.
- API/Worker health and the truthful 503 diagnostic behavior remain unchanged.
- Performance impact is N/A: the wrapper adds no runtime hop and delegates to the existing launcher.
- Recovery is process-level: stop the foreground command and clean up only its child processes. Restoring cloud delivery requires a future decision, not rollback of local data.

## Verification

- `powershell -ExecutionPolicy Bypass -File deploy/local/start.ps1 preflight`
- Existing native Web-to-API-to-Worker smoke test.
- Existing API, Worker, Web and architecture quality commands.

## Revisit Triggers

- A real test/staging/production environment is selected.
- CI automation, container promotion, remote host deployment or rollback becomes a release requirement.
