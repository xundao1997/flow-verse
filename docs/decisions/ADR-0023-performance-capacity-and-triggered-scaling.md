# ADR-0023: 性能基准、容量与证据触发扩展

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../engineering/PERFORMANCE_BUDGET.md`；`../engineering/RELIABILITY_BUDGET.md`；`../engineering/V1_SERVICE_MIDDLEWARE_AND_OPERATIONS_DESIGN.md`；外部 PRD 容量与处理边界（hash 见 `../intake/V1_PACKAGE_INTAKE.md`） |
| Supersedes | N/A |

## Context

- PRD 已确认普通交互 P95、参考处理和上传容量边界，但 H0 环境、夹具、并发、样本、命令和回归阈值尚未批准。
- 当前只有诊断 Web bundle 与单次 middleware smoke；没有业务负载结果。
- Redis、读副本、broker、partition、pgvector 和 TimescaleDB 都应由瓶颈证据触发。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. 固定 H0 profile + 分段测量 + 触发式扩展 | 可复现、避免过早优化 | 需要夹具/环境/工具治理 | Medium | 当前候选 |
| B. 先堆缓存/副本/队列 | 看似有余量 | 增加一致性和运维面，问题来源不明 | High | 已有明确瓶颈才成立 |
| C. 仅生产观察 | 最贴近真实用户 | 发布前风险大、难做N-1/上限 | Low initially | 只能补充不能替代lab |
| D. 无性能门 | 开发快 | 无法证明PRD目标与容量 | Low | 不可接受 |

## Decision

- Proposed option A：为 H0/V1.0、H1/V1.1、H2/V1.2 建独立且累计 benchmark profile。
- H0 输入至少覆盖 PRD 的 20 文件/任务、10 MB/文件、50 万字符/文件、200 万字符/任务、300 页 PDF 上限，以及默认 20 章大纲+前 3 章；划分 short/target/limit，包含 cold/warm。
- 记录 build/config/environment、浏览器/viewport、数据 seed、cache state、单用户+管理员、AI/provider stub/real class、样本/窗口和原始结果。精确工具、并发与 warning/failure delta 必须另行批准。
- 分段测量 Web navigation/render/save/IME、API handler/serialization、PG query/lock/pool/WAL、Worker queue/claim/step、ObjectStore、SSE、Prompt pre/post-validation、provider wait 与成本。
- 生产 HA profile 加 N-1、burst/backlog、soak 和 recovery workload；失去一故障域后必须满足批准预算或进入批准降级。
- 只有测量达到批准触发器才启用 Redis cache/wakeup、PG read replica/partition、broker/outbox、pgvector/TimescaleDB、服务提取或多区域。

## Rationale and Trade-Offs

- 测量先于优化，避免把复杂度当性能。
- 接受建立代表性夹具和重复运行的成本，换取可解释容量与回归门。
- PRD 上限是正确性/处理边界，不自动等同于吞吐或并发承诺。

## Impact

- 每个性能结果绑定精确版本并保存 P50/P95/P99、error、queue age、pool/lock wait、CPU/memory/IO、对象吞吐和成本。
- 高基数 ID/hash/Prompt version 不进入 metric label；可使用有界 workloadClass/promptFamily/modelProfile/provider。
- 缺少环境、命令或原始结果保持 Unverified；不得用容器 limit、索引存在或架构图标 Passed。

## Implementation and Verification

- 先在 TECH_STACK 登记性能工具/命令为 Confirmed+Available，再执行 H0 baseline。
- 回归比较需要噪声基线、相同 profile 与批准阈值；报告冷/热、失败和资源曲线。
- 负载、soak、N-1、queue saturation、large object 和 long-session 均有 stop condition，不能拖垮共享环境。

## Revisit Triggers

- PRD 容量/并发、SLO、硬件/云平台、AI provider、数据保留、第二用户或 V2 金融 workload 改变。

