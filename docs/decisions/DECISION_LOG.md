# FlowVerse Architecture Decision Log

## Rules

- Store decisions in this directory using the pattern ADR-NNNN-short-title with a Markdown extension.
- AI drafts Proposed decisions; only the user marks them Accepted.
- Never edit an Accepted decision to rewrite history; supersede it with a new ADR.
- Update this log when an ADR status changes.

## Decisions

| ID | Title | Status | Scope | Decision date | Supersedes | File |
|---|---|---|---|---|---|---|

| ADR-0001 | Modular monolith and process topology | Superseded | FV1-ARCH-BASELINE / FV1-BOOTSTRAP | 2026-07-14 | None | [ADR-0001-modular-monolith-topology.md](ADR-0001-modular-monolith-topology.md) |
| ADR-0002 | Service directory topology | Accepted | FV1-ARCH-BASELINE / FV1-BOOTSTRAP | 2026-07-15 | ADR-0001 | [ADR-0002-service-directory-topology.md](ADR-0002-service-directory-topology.md) |
| ADR-0003 | Yunxiao Flow and ACR delivery boundary | Superseded | FV1-DELIVERY-BOOTSTRAP | 2026-07-15 | Production-delivery portion of ADR-0002; superseded by ADR-0006 | [ADR-0003-yunxiao-acr-delivery.md](ADR-0003-yunxiao-acr-delivery.md) |
| ADR-0004 | Native local startup and Yunxiao host Docker delivery | Partially superseded | FV1-LOCAL-RUNTIME / FV1-DELIVERY-BOOTSTRAP | 2026-07-16 | Local Compose portion of ADR-0002; delivery portion superseded by ADR-0006 | [ADR-0004-native-local-and-yunxiao-host-docker.md](ADR-0004-native-local-and-yunxiao-host-docker.md) |
| ADR-0005 | Operational diagnostic chain and three-service runtime | Partially superseded | FV1-DIAGNOSTIC-BOOTSTRAP / FV1-LOCAL-RUNTIME / FV1-DELIVERY-BOOTSTRAP | 2026-07-20 | No-network-contract and one-shot-only Worker portions of ADR-0002/0004; delivery portion superseded by ADR-0006 | [ADR-0005-operational-diagnostic-chain.md](ADR-0005-operational-diagnostic-chain.md) |
| ADR-0006 | Local native test deployment only | Accepted | FV1-LOCAL-TEST-DEPLOY / FV1-LOCAL-RUNTIME | 2026-07-21 | ADR-0003; Yunxiao/production-delivery portions of ADR-0004/0005 | [ADR-0006-local-test-deployment-only.md](ADR-0006-local-test-deployment-only.md) |
