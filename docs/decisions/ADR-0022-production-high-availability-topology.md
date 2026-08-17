# ADR-0022: 单区域多故障域生产高可用拓扑与分层就绪

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-13 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../intake/V1_PACKAGE_INTAKE.md` 中 `FV1-ROADMAP-REVIEW=IN_REVIEW`；`../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md` 12.1、12.5～12.8、TD-20/TD-22；`../engineering/RELIABILITY_BUDGET.md`；`../engineering/ARCHITECTURE_BASELINE.md` |
| Supersedes | N/A |

Allowed status values: Proposed, Accepted, Rejected, Deprecated, Superseded.

本 ADR 未接受、未实现、未做故障演练。当前单主机 PostgreSQL/Redis/MinIO Compose 仍只用于开发和架构验证，不构成生产 HA 证据。

## Context

- Problem: 用户要求方案面向高可用和高性能，但当前仓库只确认了本地三服务和单主机中间件。简单部署两个 PostgreSQL 数据节点不能形成安全多数派；共享 readiness 会让可选依赖故障级联摘除所有 API；公网与 Worker 内部入口混用会放大安全和资源争用风险。
- Confirmed requirements: 现有 99% 内部 MVP 可用性是产品底线；工作主页确定性入口不能因 Bot/provider 故障不可用；正式事实必须保持单 writer、强一致约束和可恢复；RTO 4 小时。99.9%、精确故障包络和生产拓扑仍为 Proposed/Unknown。
- Constraints: 生产区域、厂商、预算、运维团队、LB/TLS/DNS、托管或自建、初始副本数、连接池和容量尚未确认；不能凭“两副本”声称 N-1 容量；Redis 当前无业务消费者，单节点 MinIO 不具生产 HA 证明。
- Current module/contract/data/reliability facts: Web、API、Worker 是已批准的服务目录；API/Worker 业务合同仍未实现。PostgreSQL 是权威状态候选，Worker 应通过 lease/fencing 受控执行；public API 与 internal Worker API 应保持不同可达性和预算。
- Why a decision is required now: 生产部署、正式数据写入、滚动发布、容量测试和恢复设计都依赖统一的故障域、选主、fencing、入口和 readiness 语义。

## Options

| Option | Benefits | Costs / risks | Complexity | Lock-in | When valid |
|---|---|---|---|---|---|
| A. 单主机应用与中间件 | 成本和操作最简单 | 任一主机故障全停；不满足 HA 方向；不能验证 N-1 | Low | Low | 本地/非生产验证 |
| B. 两数据节点自行选主 | 资源较少 | 网络分区时无法形成安全 quorum；可能 split-brain 或失去写入 | Medium | Medium | 不适用于当前正式单 writer 目标 |
| C1. 单区域多故障域，三个data-bearing PG节点；writer提交至少由一个合格同步standby确认，另有可证明quorum/fencing控制 | 单个data node/standby丢失后仍有同步冗余候选；保持单writer | 第三个数据副本、同步延迟、容量和控制面成本更高 | High | Low/Medium，逻辑合同不绑定厂商 | 需要在失去一个data fault domain后继续formal write且N-1证据通过时 |
| C2. writer+唯一同步data standby+独立第三票/等价控制面；失去该standby时formal write fail closed | 资源较少；不会把“两节点可投票”误当安全多数派 | 唯一同步standby故障会牺牲正式写可用性；必须显式计入SLI/error budget | Medium/High | Low/Medium | 可接受丢standby即正式只读，且降级/恢复证据通过时 |
| D. 多区域 active-active | 区域级在线能力潜力高 | 跨区一致性、双写、fencing、延迟、成本和运营复杂度最高 | Very High | High | 仅区域 RTO/RPO、数据驻留和负载证据明确要求时 |
| E. 延后生产部署 | 不提前锁定厂商或成本 | 生产发布保持阻断 | Low now | None | owner、预算或故障包络无法批准时 |

## Decision

- Chosen option: **Proposed C-family，C1/C2 尚待 decision owner 二选一**。本 ADR 在具体模式、故障域和适用发布门被接受前不完整，代码/部署不得静默代选。共同目标为单区域多故障域、单 writer；区域灾难先采用独立 application recovery set 恢复，不在 V1 建设 active-active。
- Scope:
  - Web 使用带内容 hash 的不可变制品和原子版本切换；L7 入口跨批准故障域。
  - API 和 Worker 的初始生产形态各至少覆盖两个批准故障域，但精确副本数和资源只能由 N-1 负载证据确定。API 无状态；会话、幂等和 receipt 位于权威存储。Worker 以 lease/heartbeat/fencing 保证单一合法执行 owner。
  - `C1`要求三个data-bearing节点跨批准故障域；每次formal commit至少收到一个当前合格同步standby确认，且promotion还需可证明控制面的多数派、replication eligibility和旧主fencing。单一standby/数据故障域丢失后，只有另一同步standby资格与N-1容量仍可证才继续formal write；eligible集合不得自动缩为空或在成员资格不明时降成异步，受控reconfiguration期间不确定则fail closed。
  - `C2`要求writer+唯一同步data standby+独立第三票/等价控制面；该standby丢失、落后、资格不明或同步确认不可用时，所有formal write立即fail closed，直到同步冗余恢复、追平并验证。静态Shell、本地普通draft和可证明安全的历史只读可按批准合同继续；不得切成异步模式形成隐性数据损失窗口。
  - 两模式都使用稳定writer endpoint、单writer；只有多数派、同步资格和旧主fencing都可证明才允许提升，两个data节点不得自行互选。精确同步参数、确认集合、超时和恢复阈值必须由批准拓扑与测量产生。
  - `/api/v1` public endpoint 与 `/internal/v1` Worker endpoint 可落到同一受控 API 副本集，但网络可达性、workload identity、路由、限流、并发预算和 readiness 必须隔离；公网不得存在通往 `/internal/*` 的路由。
  - `liveness` 只证明进程可响应；public readiness、internal readiness 和 capability readiness 分开。API 可在同一 `GET /health/ready` method/path 上由受控listener/probe audience服务器侧固定并回显`PUBLIC/INTERNAL` scope：PUBLIC只看writer/schema/public pool，INTERNAL另看workload identity、claim-result schema与internal pool；客户端参数/头不能选scope，任一scope故障不得交叉摘流。PostgreSQL writer/Schema 不安全时相应正式接流失败；ObjectStore/provider/Redis/observability 故障只关闭受影响 capability 或启用批准旁路，不级联摘除全部 API，也不得通过ready直接调用Worker。
  - 对象存储必须有跨故障域耐久候选；当前单节点 MinIO 不能直接提升为生产 HA。Redis 无消费者时不进入关键路径；启用任一角色需单独审批其复制、淘汰、容量和降级。
- Explicit non-goals:
  - 不选择云厂商、编排器、LB、DNS、TLS、托管数据库、对象存储或 Redis 产品，也不批准精确副本/CPU/内存/连接池数。
  - 不把 99.9% 写成 Confirmed SLO；不承诺区域级 RPO=0；不建设多区域 active-active。
  - 不把只读副本用于正式新鲜度、命令后读取、capability 或 receipt；不让公共入口回退到内部路由。
  - 不把同步副本替代备份，也不由此 ADR 接受 ADR-0018 的恢复实现。

## Rationale and Trade-Offs

- Requirement-linked rationale: quorum/fencing守住单writer但不能制造第二份同步数据；因此必须明确选择“第三个data-bearing节点”或“丢唯一同步standby即formal-write fail closed”。分层readiness让可选依赖故障局部化；多故障域加N-1测试把HA转成可验证性质。
- Trade-offs accepted: 为消除单点、split-brain 和共享健康级联风险，接受更多基础设施、跨域延迟、部署控制和演练成本。
- Negative consequences: 同步复制可能增加写延迟；C1增加数据节点成本，C2增加丢standby时的正式写不可用；控制面故障时正式写入会fail closed；副本存在不代表容量充足；单区域仍不能抵御区域灾难。
- Mitigations: 用实际延迟/容量证据决定同步范围和资源；保留本地草稿/静态 Shell/安全只读降级；独立备份恢复覆盖区域与逻辑灾难；error-budget 策略和多区域触发器另行批准。

## Impact

- Modules, ownership, and dependency direction: Web → public API；Worker → private internal API；两类入口到同一模块化 API 可复用实现但不可共享无界预算。API/Worker 不形成双向业务调用环；平台/运维、安全、数据 owner 仍需指定。
- Public contracts, data, compatibility, and migration: 需稳定 public/internal endpoint、workload identity、readiness/capability 和 writer endpoint 合同。混合版本只在获批兼容窗口内共存，迁移由唯一受控 migrator 执行。
- Reliability, failure, recovery, and operations: 单副本由LB摘流；Worker lease到期后受fencing重领；quorum或旧主fencing不可证时停止自动提升并关闭正式写入；C2还在唯一同步standby不合格时关闭formal write。ObjectStore/provider/Redis/observability按capability局部降级。
- Performance and capacity: 必须验证失去一个批准故障域后剩余资源仍满足核心 SLO 与背压；同步复制、入口隔离和连接池需纳入端到端 P50/P95/P99、峰值与 soak。当前无结果。
- Security, privacy, and compliance: 内部 endpoint 仅私网/受控网络可达并使用独立 workload identity；公网路由、限流和权限 fail closed；secret、TLS、最小权限和审计由后续合同批准。
- Deployment, rollout, rollback/forward recovery: 先 expand migration，再滚动新 API/Worker；各入口 readiness 通过后接流；摘流需 draining，Worker 先停 claim。若 HA 方案未接受或演练失败，只能退回非生产单主机验证，生产发布保持阻断；发生不可逆迁移后用 forward-fix 或 ADR-0018 的完整恢复。
- Technical debt introduced or retired: 若实现，可退休单主机生产和两节点伪 quorum 风险；在 SLO、厂商、owner、容量、演练未冻结前保留明确的发布阻断，而不是隐性债务。

## Implementation and Verification

- File-level plan: 接受后先更新架构/可靠性/性能注册表和生产部署 ADR，再审批具体 manifest、网络、身份、迁移与 runbook。当前 ADR 不授权修改部署或代码。
- Architecture/contract/failure/performance checks:
  - 静态验证公网无 `/internal/*` 路由，public/internal identity、限流和 readiness 独立；测试同一ready path的受控listener/audience scope、响应scope、客户端伪造拒绝，以及public/internal pool或身份故障不交叉摘流。
  - 演练单 Web/API/Worker 副本、整个故障域、SSE 断线、provider/ObjectStore/Redis/observability 故障和 capability 局部降级。
  - PostgreSQL演练主节点故障、每个data fault domain丢失、第三票/控制面丢失、旧主无法fencing、事务中切换、timeline/唯一性与实际RPO。C1必须证明任一单data-node丢失后剩余同步确认与N-1容量；C2必须证明唯一同步standby一旦不合格就无formal commit，并在追平/验证后有界恢复。任何split-brain、异步风险窗口或不可证明单writer为失败。
  - 在 N-1 条件下跑批准的数据集、峰值和 soak，记录端到端延迟、错误、积压、连接池、复制延迟和恢复时间。未测量均为 Unverified。
- Mixed-version or migration sequence: Schema expand → 兼容应用 canary → 分入口 readiness → 流量切换 → 观察 → contract 清理。旧应用不得写入新版本无法理解的正式状态；删除兼容路径需单独批准。
- Success and failure evidence: 需要明确的C1/C2批准记录、拓扑/配置快照、同步commit证据、健康与capability响应、路由探测、故障时间线、fencing日志、数据一致性、N-1性能和回退/恢复结果。架构图、第三票或副本数量本身不是Passed证据；当前全部Unverified。

## Revisit Triggers

- Confirmed scale or load threshold: N-1 压测、连接/积压或同步复制延迟不能满足已确认预算；阈值由实际基线产生。
- New consumer or implementation: Redis 进入任一业务角色、采用自建分布式 MinIO、拆分服务、引入第二地区或新的内部消费者。
- Reliability/performance budget change: SLO 从 99% 调整、区域故障纳入在线包络、RTO/RPO/错误预算或数据驻留改变。
- Due phase/date: 生产设计冻结和任何正式预发布之前；未接受、未定 owner 或未演练时生产保持阻断。
