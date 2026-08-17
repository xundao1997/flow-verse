# ADR-0024: V1.0～V1.2 累计发布与服务端能力激活

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-13 |
| Scope IDs | FV1-ROADMAP-DIRECTION / FV1-ROADMAP-REVIEW |
| Evidence | `../intake/V1_PACKAGE_INTAKE.md` 中 `FV1-ROADMAP-DIRECTION=APPROVED` 与 `FV1-ROADMAP-REVIEW=IN_REVIEW`；`../product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md`；`../product/V1_PRODUCT_BRIEF.md`；`../uiux/ACCEPTANCE_CRITERIA.md`；`../tasks/V1_IMPLEMENTATION_PLAN.md`；`../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md` 2.4、15.1、TD-23～TD-25 |
| Supersedes | N/A |

Allowed status values: Proposed, Accepted, Rejected, Deprecated, Superseded.

用户已确认路线的顺序与主题；本 ADR 只提议其精确累计激活、兼容和回退方式。`FV1-ROADMAP-REVIEW` 尚为 `IN_REVIEW`，因此本文不是范围批准或实现放行。

## Context

- Problem: 外部 PRD v1.1 将小说创作、真实投放、反馈、分析、人类决定和 successive Cycle 表达为完整 V1 合同；用户又确认按 V1.0、V1.1、V1.2 逐步交付。如果只重命名版本，V1.0 可能被后续运营字段阻断，或前端隐藏未启用页面但后端仍可通过深链/命令产生半成品状态。
- Confirmed requirements: V1.0 是首个实现版本；V1.1、V1.2 为累计追加，V1.2 闭合完整小说创作到运营循环；路线主题为 V1.0 小说、V1.1 AI 分析与运营复盘、V1.2 复盘驱动 AI 创作与闭环效果；V2.0 金融研究使用独立产品合同。
- Constraints: 原始 PRD/UIUX receipt 不得改写；精确分版、UIUX、AC、Prompt/API/Schema 尚待整体 Review 和用户批准；现有业务代码不存在；每版均需独立 Scope/Contract/Operational/Outcome Gate，不能以未来能力补齐当前版本。
- Current module/contract/data/reliability facts: 代码服务目录已确认，但业务模块、API 和 Schema 未批准。CreationBaseline 与 OperationValidationBaseline 的拆分、每版 first-due AC 和 capability 名称目前都是 IN_REVIEW 候选。
- Why a decision is required now: 实施顺序、数据迁移、路由、UIUX、Prompt family、回归范围和发布回退都需要一个权威的“能力何时可用”合同。

## Options

| Option | Benefits | Costs / risks | Complexity | Lock-in | When valid |
|---|---|---|---|---|---|
| A. 一次性交付完整 V1 | 与原始完整生命周期表述直接一致 | 首次价值和验证延后；大范围并行导致合同割裂风险 | High | Medium | 团队、周期和证据支持一次性发布时 |
| B. 三个独立产品/代码分支 | 每版边界看似清楚 | 数据、状态机和回归分裂；迁移及维护成本高 | High | High | 产品语义和用户群真正独立时；当前不成立 |
| C. 单一产品/代码线的累计 capability 激活 | V1.0 可独立完成；后续复用正式事实与审计；可渐进验收和回退 | 需要严格版本矩阵、服务端 gate、兼容迁移和累计回归 | Medium | Low | 当前推荐候选 |
| D. 仅靠前端隐藏后续页面 | 实现表面简单 | 深链/API 可绕过；产生非法状态；无法审计不可用原因 | Low | Medium | 不满足当前安全和一致性要求 |
| E. 延后精确分版 | 避免过早承诺 | 所有业务实现继续阻断 | Low now | None | 同源文档无法达成一致时 |

## Decision

- Chosen option: **Proposed Option C**。如本 ADR 被接受，V1.0、V1.1、V1.2 在同一产品和兼容代码线上累计激活；每版必须不依赖后续版即可满足自己的 Outcome Gate。
- Scope:
  - V1.0 激活 CreationBaseline、参考使用链、首版 AI/人工候选、人工 Review、正式小说事实、不可变快照、导出、恢复和到期治理。V1.0 的 AI 是首版候选创作；不包括真实投放、反馈、运营决定或 Cycle 效果。
  - V1.1 在 V1.0 全量回归上激活 OperationValidationBaseline、正式包装/发布计划、一次真实 ActualRelease、反馈快照、AnalysisInputManifest、AI 分析候选、正式分析和用户正式决定。`CONTINUE_OBSERVING` 是阶段动作，不是 HumanDecision，也不能满足有效 Cycle 完成门。
  - V1.2 在 V1.0/V1.1 全量回归上激活正式决定到下一轮方案/ExecutionBinding/候选/新正式版本/相邻有效 Cycle N+1 投放的 lineage、Cycle N/N+1 比较、个人价值判断与后续 Cycle N+2 入口（正常路径示例为 1→2→3）。效果只允许表达支持程度、干扰与未知，不宣称因果或市场验证。
  - 服务端 capability 是 route/action/command 的权威。未到期的新建/命令返回结构化不可用原因且不产生业务副作用；未知深链 fail closed。历史对象只在获批兼容规则下只读或继续完成，不由前端单独推断。
  - 每版使用 versioned capability/activation revision 与 first-due/cumulative 验收矩阵。后一版发布必须回归所有前版适用 AC、可靠性、安全、可访问性和性能门。
  - 每版business capability manifest与operational allowlist分离。H0 production同时退役Web Check页面、public `GET /api/v1/system/chain`和`GET /internal/v1/system/status`，只保留另行批准的5行health：API `OPS-API-001..003`与Worker私网`OPS-WORKER-001..002`。它们不计入107行business Public或10行business Internal catalog，不解锁业务capability，也不证明任何发布门。
  - Schema/API 默认 additive expand/contract；旧 Web/API/Worker 在批准兼容窗口共存。产品版本号不自动要求 REST major 变化，只有破坏性协议变更另行决策。
- Explicit non-goals:
  - 不改写或重新打包外部 PRD/UIUX 原件；不声称仓库增补已通过最终评审。
  - 不把 V1.0、V1.1、V1.2 拆成微服务、数据库或长期维护分支；不建设通用 feature-flag/Workflow 平台。
  - 不批准 V1.0 导入完整既有连载；不预建 V2 金融表、路由、Prompt 或领域状态机。
  - 不定义精确 API、Schema、依赖、部署参数或发布时间；不降低横切发布门。

## Rationale and Trade-Offs

- Requirement-linked rationale: 累计激活同时保留完整 V1 生命周期和用户要求的阶段价值；服务端 capability 防止 UI 隐藏造成绕过；两个 Stage 0 基线避免 V1.0 被运营信息耦合。
- Trade-offs accepted: 接受持续维护版本矩阵、兼容窗口、迁移和累计回归的成本，换取小步交付与可回退性。
- Negative consequences: AC 与 UIUX 需要 first-due 标注；后续字段必须可选/版本化；历史对象在降级时可能存在只读路径；运营中同时支持混合版本更复杂。
- Mitigations: 一份权威 release traceability；每版四道门；服务端返回 capability reason；契约测试覆盖当前/上一版；破坏性清理延至观察窗和恢复演练后。

## Impact

- Modules, ownership, and dependency direction: 领域 owner 仍唯一；版本层只决定模块能力是否激活，不接管数据。V1.1/V1.2 依赖 V1.0 正式事实，反向依赖禁止；V2 只复用经证实的底层机制。
- Public contracts, data, compatibility, and migration: 需要 capability/readiness、activation revision、历史对象兼容和结构化 unavailable reason 候选合同。迁移使用 expand → 双版本兼容 → activate → observe → contract。
- Reliability, failure, recovery, and operations: 后续模块/provider/Bot/Worker故障不得阻断V1.0已正式内容的查询、编辑和恢复；Worker/JIT/DeliveryStore故障按job owner显示为AI execution、P03参考处理或D11导出请求。新文档处理和新/重复导出生成fail closed；只有ObjectStore当前证明目标version、完整性、授权与可读字节的既有生成包仍可preview/download。发布切换和回退必须保留正式事实、请求receipt及审计。
- Performance and capacity: 每版用其代表性工作负载验证，后一版还需回归前版关键路径；不能用 V1.0 负载证明 V1.2 Cycle/分析容量。
- Security, privacy, and compliance: capability 在服务端按身份、对象、版本和政策计算；前端不构成授权边界；未激活命令 fail closed 并留可审计原因。
- Deployment, rollout, rollback/forward recovery: 可回退到上一批准 activation revision，让新建/命令关闭并维持前版能力。若后版已有正式数据，不删除或覆盖；按批准策略只读/完成在途工作。Schema 越过不可逆点后使用 forward-fix，不以旧制品强行解释新状态。
- Technical debt introduced or retired: 退休“完整 V1 一次性交付”和“仅前端隐藏”歧义；新增版本矩阵维护成本，但必须被 traceability 和 contract tests 显式拥有。

## Implementation and Verification

- File-level plan: 本轮只同步 Product Brief、PRD 增补、AC、UIUX、Implementation Plan、技术方案和 Prompt 规范。接受后才可设计 capability/API/Schema、迁移和 feature activation；当前不授权业务代码。
- Architecture/contract/failure/performance checks:
  - traceability 检查每个 requirement/AC/UIUX scenario/Prompt family/模块与 `firstDueIn`、`cumulative`、owner 和证据。
  - 契约/E2E 检查未激活深链与命令无副作用、原因一致，上一版独立工作，后版激活后前版全量回归。
  - 混合 Web/API/Worker 版本和迁移中断测试；历史对象在 downgrade 下按批准规则可读且不被错误新建。
  - H0 production router/build/dependency测试成对deny Check/public-chain/internal-status诊断三件套，同时确认批准的5行`OPS-API-001..003/OPS-WORKER-001..002`只存在于独立operational allowlist；typed job故障测试确认新处理/导出关闭且既有包必须取得ObjectStore当前证明。
  - 每版分别执行安全、强制`DataSafetyGate`（含恢复）和性能门；只有`UD-AVL-01`明确使`AvailabilityGate`适用于该发布时才执行N-1/failover可用性门。缺少到期命令或结果标Unverified，不标Passed；未适用N-1不得阻断基础H0，也不得支持HA声明。
- Mixed-version or migration sequence: 先 deploy 可兼容读取/忽略新字段的代码，执行 expand migration，验证旧能力，再激活新 capability；观察后才 contract。回退优先撤销 activation；不得先做破坏性 Schema 回滚。
- Success and failure evidence: 同源版本矩阵无冲突、package gate 最终批准、对应 ADR/合同 Accepted、实际 activation receipt、前后版契约/E2E/恢复/性能原始结果。只修改文档不构成成功证据。

## Revisit Triggers

- Confirmed scale or load threshold: 某版本新增负载破坏前版 SLO/N-1，或维护多版本兼容显著超过获批交付能力。
- New consumer or implementation: 已有作品导入、第二类小说工作流、外部发布自动化、金融 bounded context 或破坏性 API major。
- Reliability/performance budget change: 任一版本的 SLO、RTO/RPO、性能、成本或错误预算改变。
- Due phase/date: V1.0 Scope Gate 前最终接受；V1.1/V1.2 各自 Scope/Contract Gate 重新核验；未批准时业务实现保持阻断。
