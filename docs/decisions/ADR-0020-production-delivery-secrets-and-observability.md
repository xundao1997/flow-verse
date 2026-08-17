# ADR-0020: 生产交付、Secret、可观测性与回退

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-ROADMAP-REVIEW |
| Evidence | `../engineering/TECH_STACK.md`；`../engineering/V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`；`../engineering/RELIABILITY_BUDGET.md`；`ADR-0022-production-high-availability-topology.md` |
| Supersedes | 仅在接受后 supersede ADR-0006 对未来生产交付保持 Unknown 的部分；当前 N/A |

## Context

- 当前批准路径是本地原生应用与单主机中间件 Compose；没有应用生产平台、CI/CD、artifact registry、LB/TLS/DNS、secret backend、monitoring backend 或 on-call。
- 服务 Dockerfile 只是历史 packaging artifact，不是批准生产交付线。
- 高可用和性能无法在没有发布身份、指标、告警、回退和故障证据的环境中证明。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. 托管应用/数据库/对象服务 | 运维负担低、内建多故障域候选 | 厂商成本/锁定与能力差异 | Medium | 团队较小且区域/合规满足时 |
| B. 自运维编排 + 自建数据面 | 控制力强 | 7×24、升级、fencing、备份和安全成本高 | High | 团队与运维证据充分时 |
| C. 单主机 Compose 直接生产 | 最快 | 单点、无安全/回退/恢复闭环 | Low initially | 仅开发/隔离测试，不可作为当前生产候选 |
| D. 延后平台选择 | 不提前锁厂商 | 生产发布保持阻断 | Low now | 当前可用于文档/本地实现阶段 |

## Decision

- 当前仍选择 option D；同时定义未来生产选择门，不在本文发明厂商、区域、副本数或精确资源。
- 生产候选必须支持不可变、content-addressed artifact；Web/API/Worker 独立 rollout；签名/来源验证；环境分离；非个人 registry；最小权限 runtime identity。
- Public/internal 网络入口分离，TLS everywhere；应用不读取 root middleware credential。Secret 来自批准 backend，支持轮换、审计和不落日志。
- 配置采用版本化 schema、启动前校验和安全默认；Prompt/model/policy/business config 使用应用层 activation，不靠环境变量热改正式语义。
- OpenTelemetry/structured logs 接可替换 backend；先定义低基数 SLI、告警 owner、runbook、保留和 exporter 满载行为，再声明 SLO。
- rollout 使用 readiness/capability、small-batch/canary、自动或人工 stop gate；rollback 优先切换旧 artifact/activation，Schema 跨不可逆点后 forward-fix。

## Rationale and Trade-Offs

- 保留托管与自建选项，避免在团队/预算/区域未知时制造伪确定性。
- 接受生产发布暂时 Blocked；换取部署、安全、可观测和恢复合同先闭合。
- telemetry 不是权威 audit；exporter 故障有界丢弃/缓冲并告警，不阻断正式事务。

## Impact

- 生产拓扑必须与 ADR-0022、数据安全/可用性两层门、ObjectStore 和 PG HA 选项一起批准。
- 每次发布绑定 artifact/config/schema/Prompt activation 和 traceability evidence。
- 当前 middleware Compose 与本地启动继续用于开发，不被静默升级为生产路径。

## Implementation and Verification

- 选型前提供团队、预算、区域、合规、SLO/RPO、运维/值班能力比较。
- 验证 artifact provenance、secret rotation、TLS、public/internal isolation、mixed version、canary stop、rollback/forward-fix 和 telemetry outage。
- HA/failover/performance/restore 原始证据绑定精确 build/config/environment；一次 `healthy` 不算通过。

## Revisit Triggers

- V1.0 production pre-release；用户批准云/机房/区域；团队/预算变化；SLO、数据驻留或供应商生命周期改变。

