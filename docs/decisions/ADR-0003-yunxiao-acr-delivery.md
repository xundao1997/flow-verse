# ADR-0003: Yunxiao Flow and ACR delivery boundary

## Status

Accepted by the user on 2026-07-15 for the delivery control plane. The
production runtime target remains Unknown.

## Context

ADR-0002 created independent Web, API and Worker images and a Compose topology.
The user has clarified that Docker Compose is not the formal deployment path.
The repository must integrate with Alibaba Cloud Yunxiao Flow for source
binding, image construction and controlled delivery.

The Alibaba Cloud organization, service connections, ACR region/repositories,
build cluster and production runtime have not been supplied. The unresolved
runtime could be an ECS host, ACK, SAE or another separately approved target.

## Options considered

| Option | Benefits | Costs |
|---|---|---|
| Treat root Compose as production deployment | Minimal configuration | No managed source binding, artifact promotion or cloud authorization boundary; contradicts the user decision |
| Yunxiao Flow builds service images and publishes them to ACR | Matches the selected control plane; service connections keep credentials out of Git; images are independently traceable | Cloud-side binding and ACR repositories must be provisioned; the repository alone cannot prove a successful run |
| Add ACK, SAE or ECS deployment configuration now | Could complete a specific CD path | Invents a production target, network and rollback contract that the user has not selected |

## Decision

- Root `compose.yaml` is local-development tooling only and is not a production
  release contract.
- Yunxiao Flow is the formal CI control plane. It binds the current GitHub
  repository and `v1` branch through a Yunxiao service connection.
- Flow uses one `ACRDockerBuild` job for each of `services/web`, `services/api`
  and `services/worker`, publishing separate artifacts to separately configured
  ACR repositories.
- Images use `${CI_COMMIT_ID}-${BUILD_NUMBER}` tags. Floating `latest` tags are
  excluded from the delivery contract.
- Source credentials and ACR credentials exist only in Yunxiao service
  connections. Secret application configuration may later use private Yunxiao
  variables or variable groups after the runtime contract is approved.
- No production deploy job or runtime manifest is created until the user selects
  the production target and approves its security, reliability, network,
  database migration, health and recovery controls.

## Trade-offs and consequences

- Repository code now describes the intended image build topology while
  environment authority remains in the Yunxiao organization.
- The source-controlled template contains unresolved, visibly named
  placeholders rather than guessed cloud identifiers.
- A local YAML parse proves syntax only. It does not prove that service
  connections, ACR networking, Flow components or image builds work.
- The Web build remains blocked by the separately recorded TypeScript/ESLint
  package conflict. The template must not have its trigger enabled until that
  conflict and the missing Web lockfile are resolved.
- Production release and rollback remain blocked rather than being simulated by
  Compose or an unapproved host/Kubernetes script.

## Revisit triggers

- The user selects ECS, ACK, SAE or another production runtime.
- A staging/production promotion and approval policy is confirmed.
- An ACR instance/region/network model and secret-management owner are supplied.
- A successful Yunxiao run provides image-build and push evidence.
