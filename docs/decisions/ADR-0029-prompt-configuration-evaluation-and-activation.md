# ADR-0029: Prompt 配置、评测、执行绑定与受控激活

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-13 |
| Scope IDs | FV1-ROADMAP-REVIEW |
| Evidence | `../intake/V1_PACKAGE_INTAKE.md` 中 `FV1-ROADMAP-REVIEW=IN_REVIEW`；`../ai/SYSTEM_DECISION_PROMPTS.md` 4、11～14；`../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md` 9.5～9.11、TD-27/TD-28；`../product/V1_ROADMAP_AND_DECISION_PRD_AMENDMENT.md` 5、11；`../uiux/ACCEPTANCE_CRITERIA.md` |
| Supersedes | N/A |

Allowed status values: Proposed, Accepted, Rejected, Deprecated, Superseded.

本文只提议系统决策 Prompt 的生产治理，不含小说写作 Prompt。当前没有批准的 Golden Set、rubric、阈值、模型调用或线上对照结果，任何 Prompt 均不得据此声称有效或 Active。

## Context

- Problem: Prompt 效果取决于模板、context builder、provider/model、参数、输入快照、输出 Schema、政策和评测证据。把这些全部放进一个“Effect Bundle”会使每次输入都让配置评测失效；只保存 Prompt 文本又无法重建某次执行或判断某个版本为何被激活。
- Confirmed requirements: Prompt 是核心资产；模型输出始终是候选；正式事实由人确认；需要可版本化、可评测、可审计、可撤销、可回退。用户要的是各阶段系统/模型决策 Prompt，不是正文写作提示词。
- Constraints: provider/model/价格/政策、Golden Set、rubric、阈值、评测 owner、生产数据库 Schema 和 exact API 仍未批准；一个默认用户和一个管理员的 MVP 事实不自动证明职责分离可执行；线上真实数据和双轨费用需单独授权。
- Current module/contract/data/reliability facts: 技术方案和 Prompt 规范已提出 family、G0～G3、human/judge 校准、pairwise、shadow/pilot/canary、revoke 和 no-AI fallback，但均为 IN_REVIEW；当前没有 Prompt registry 实现。
- Why a decision is required now: 若不先冻结不可变对象和激活权威，A05 容易退化为在线自由编辑器，执行无法重建，评测证据与生产输入混淆，回退也无法确定目标。

## Options

| Option | Benefits | Costs / risks | Complexity | Lock-in | When valid |
|---|---|---|---|---|---|
| A. 只版本化 Prompt 文本 | 简单、直观 | 无法冻结模型/renderer/schema/policy；不可重建真实执行 | Low | Low | 仅离线原型 |
| B. 单一 Effect Bundle 包含配置、评测和每次输入 | 一个对象看似完整 | 输入变化导致评测绑定不断失效；激活与执行历史难分离 | Medium | Medium | 不适合生产治理 |
| C. 拆分 PromptConfigBundle、EvaluationBinding、ExecutionBinding，权威激活修订独立保存 | 配置效果、评测证据和单次执行可分别追踪；可撤销/回退 | 需要更多实体、hash、工作流、权限和对账 | Medium/High | Low，provider/store 可通过窄合同替换 | 当前推荐候选 |
| D. 直接采用外部 Prompt 平台为权威 | 功能成熟、搭建快 | vendor lock-in、数据/权限/审计边界未知；可能绕过产品治理 | Medium | High | 经数据、安全、成本和迁移评审后 |
| E. 不启用 AI，保持人工/确定性流程 | 安全、可恢复 | 缺少 AI 决策辅助价值 | Low | None | 无批准配置/评测/owner 时的首版安全回退 |

## Decision

- Chosen option: **Proposed Option C，且 Option E 是首版无 last-known-good 时的强制安全回退**。
- Scope:
  - `PromptConfigBundle` 不可变地冻结 family/version/parent、规范化模板字节及content/canonical hash、renderer/context-builder/retrieval/chunker、typed variable schema、allowed label/action taxonomy、精确 provider/model/profile/adapter、采样/推理参数、context/output限制、tool/output/family payload Schema与Review/合规/数据政策/产品版本。任一项改变创建新 config ID/hash。
  - `EvaluationBinding`不可变地把candidate PromptConfig与`DIRECT|PAIRED`模式绑定到分层数据集、rubric/阈值/零容忍项、deterministic validator、人标/校准。DIRECT只作绝对维度补充；PAIRED另冻结`PROMPT_ONLY|FACTORIAL|BASELINE_GATE` basis、control ref/hash、change-set、CANDIDATE/CONTROL arm及盲化A/B顺序交换计划。PROMPT_ONLY的control必须是PromptConfig，两arm使用相同provider/exact model/profile/adapter、参数、基础输入/context/case且只改变声明的Prompt因子；BASELINE_GATE的control必须是typed HUMAN/NO_AI baseline且不创建control provider TARGET lane；FACTORIAL在plan中封闭允许的control kind、全部因子和组合，typed baseline同样无provider lane，且不得单归因Prompt。可选独立judge PromptConfig、精确candidate/control/judge model/profile/参数/schema、runtime/environment fingerprint、按arm/role的repeat/randomization/seed policy、有界call plan、结果Schema与审批同样进入canonical hash；human-only禁止JUDGE call。只有API finalizer证明全部plan/hard-fail/所需人审及basis对应证据集合闭合（DIRECT=candidate，PROMPT_ONLY=两个provider arm+换位，BASELINE_GATE=candidate+typed baseline authority，FACTORIAL=冻结plan组合）、实际定义逐项匹配且无stale后，才幂等分配终态revision；同一source authorization至多一个RUN_RESULT/REQUALIFICATION，partial/failure保持Unverified。
  - BASELINE_GATE的typed HUMAN/NO_AI control必须由不可变`typed-baseline-artifact/v1`和独立人工批准receipt定义，冻结适用key、case/input/rubric/schema、provenance、限制与职责分离；它是CONTROL arm evidence但不产生provider TARGET lane、ModelCall、usage或费用。其JUDGE只等待candidate TARGET receipt与baseline artifact/authority receipt；PROMPT_ONLY仍要求两个provider arm，FACTORIAL按冻结factor/control plan判别。
  - `ExecutionBinding`在provider调用前为每个**单模型lane attempt**冻结purpose/role/arm、PromptConfig/EvaluationBinding ref/hash、解析后的provider/model/profile/adapter、参数、typed variables、context assembly/retrieval snapshot、input manifest、output schema、data scope、政策/价格/预算、deadline与preview。`BUSINESS`另冻结activation revision与当时最新eligible assessment；`EVALUATION`另冻结typed immutable authorization receipt且不得伪造activation/eligible assessment：provider TARGET只匹配实际PromptConfig；JUDGE匹配冻结judge配置，并在binding中冻结basis对应的dependency selector，而不是尚不存在的artifact hash。canonical hash生成后不可回写。一次最多三业务模型的授权必须按lane分别创建binding/attempt/job；retry/fallback只在原lane以新preview/new binding/new attempt推进，不能在同一binding混模。调用后的Attempt/ModelCall/ExecutionOutput/CostLedger另存真实response、raw-output hash、validator、用量、费用和fallback outcome，并引用该binding；JUDGE的ModelCall只在其basis所需artifact/baseline receipts齐全后冻结实际`resolvedCallInputManifestRef/hash`。
  - `EVALUATION`调用解决未激活候选Prompt的评测：它与BUSINESS共用AI job、JIT、费用、provider幂等与DeliveryStore，但使用独立pool/quota/cost和typed authorization。`OFFLINE_EVALUATION`由管理员授权并冻结candidate/control、comparison/basis/arm、blind/order、binding/plan/dataset/license/policy/price/budget/expiry与`EVALUATION_ARTIFACT_ONLY`，不占用户slot；`SHADOW_EVALUATION_CONSENT`同时要求`prompt_activation`中的不可变rollout authority manifest与用户D01 consent，冻结task/business execution/input、额外数据、增量费用/slot/allowlist/expiry。撤销追加新receipt或activation revision，JIT锁原授权、rollout ref/hash/revision、最新事件与expiry。单个arm/role结果只能写评测artifact/cost/run progress，不能创建business candidate/formal；只有API finalizer证明完整plan/hard-fail/必要人审及basis对应证据闭合且无stale后才追加合格assessment，之后才可能晋升/activation。
  - 每次provider调用必须另经过**atomic JIT call-start authorization boundary**：Worker携带job/purpose/role/arm/lane/attempt/step/binding、当前lease/fencing、expected job revision、稳定`callIntentId`、`resolvedCallInputManifestRef/hash`、规范化`requestHash`及provider idempotency capability/version请求授权；API在单一PG事务中锁定归属并按purpose重验。BUSINESS锁定匹配modelProfile activation与当前eligibility assessment revision；EVALUATION重算typed authorization manifest/hash并检查expiry/revoke，OFFLINE检查管理员authority，SHADOW检查rollout+用户consent/task/execution/input/cost/slot/allowlist。provider TARGET输入由binding确定性产生；JUDGE在其basis所需artifact/baseline receipts未齐时不可claim/call-start，实际输入逐项匹配同一authorization/run的artifact或baseline ref/hash/receipt及冻结selector/schema/order。两者都重验policy/price/budget、input/object refs、cancel/deletion，再把实际调用输入、采用的assessment或evaluation-authorization ref/hash/kind/basis/arm/role、不可变ModelCall intent、幂等receipt及exact-key策略一起写入。只有事务提交后才返回短时授权与同一exact provider key。任何purpose/basis/role/arm/lane/input/权威依据漂移、校验失败或事务回滚均不得调用provider；这不声称与外部provider实现分布式exactly-once。
  - call-start提交即进入`CALL_START_COMMITTED`副作用可能发生边界。相同`callIntentId+requestHash`重复只返回同一ModelCall/receipt及同一exact key，不创建第二意图；不同hash冲突。授权响应丢失、Worker崩溃或lease过期时，只有provider明确支持且合同验证同一exact idempotency key，才可恢复同一外部call；provider不支持或key不可重建/解密时进入`OUTCOME_UNKNOWN/WAITING_DIAGNOSIS`并保留成本/partial。自动重试、换模或改Prompt必须新preview/new ExecutionBinding/new attempt。
  - 模型只收到完成任务所需业务变量；BUSINESS executor在模型输出之外写入唯一canonical `semantic-candidate-envelope/v1`：`schemaVersion,familyId,promptVersionId,promptConfigRef,promptConfigHash,evaluationBindingRef,evaluationBindingHash,executionBindingRef,executionBindingHash,inputManifestHash,activationRevision,validationStatus,rawOutputHash,validatorVersion,validatorResult,createdAt,modelPayload`。Ref必须可解析到对应不可变ID、canonical hash和版本；模型自报值不可信且不得覆盖envelope。该17字段envelope（或不可变对象ref）、schema/hash与validator version/result持久化在ExecutionOutput；SemanticFindingCandidate只FK该output并校验同一hash，不复制第二份可信事实。EVALUATION使用独立evaluation-artifact schema且不创建业务envelope/candidate。面向UI的脱敏投影必须使用不同名称/版本，不能复用该可信envelope名称。
  - registry权威状态位于PostgreSQL候选实现。PromptConfig定义不可变，approve/config-deprecate只推进专用config lifecycle metadata并留command receipt/audit；pilot/shadow/canary/active/revoke/rollback只追加PromptActivation revision，不与通用config activation混用。`Unverified`只属于最新EligibilityAssessment revision的独立证据状态。激活唯一键为`environment + promptFamilyId + activationScope + modelProfileId`。Prompt变更默认必须引用与当前verified LKG匹配的`PAIRED/PROMPT_ONLY` assessment，获批多因子变更用FACTORIAL，首版无LKG用BASELINE_GATE；V1的DIRECT只能补充，不能单独晋升，也不提供comparison门例外。PILOT/SHADOW/CANARY activation revision必须引用不可变rollout manifest，冻结mode、完整key/config、task/execution allowlist、费用/容量、stop conditions、effective/expiry/revoke；JIT按ref/hash/revision验证。已被active引用的config不得直接deprecate，必须先在同事务或可对账outbox路径revoke/rollback相关activation。A05不提供在线自由Prompt编辑或任意模型接线。
  - Prompt 激活只有上述专用 authority。通用场景/Agent/Review/合规/平台规则的 config activation 必须以数据库 closed type/FK 排除 Prompt、decision family、provider/model 与 price bundle；A05 不得通过通用配置命令旁路 EvaluationBinding、EligibilityAssessment 或职责分离。
  - 评测数据分为 G0 Critical、G1 Representative、G2 Hard/Incident、G3 Hidden Holdout；激活门在这些数据上依次执行确定性 hard gate、离线逐维质量、human/judge 校准、受控 pilot/shadow/canary 与漂移观察。直接评分和 paired comparison 分开；judge 盲化、顺序随机/交换、长度/风格偏差检查并与人工标注校准。
  - author、evaluator、activator 是可审计的职责，不允许自评结果无独立收据地直接 Active。精确人员/RBAC 和 MVP 是否具备分离条件由用户批准；条件不足时保持 Candidate 或无 AI，不虚构新角色。
  - 首版无 last-known-good 时，必须预声明并验证人工/确定性 no-AI baseline；撤销或重大漂移时新执行回到 last-known-good，若不存在则关闭该 AI capability 并走 no-AI/manual path。
  - revoke/rollback对尚未越过call-start提交边界的新调用立即fail closed；已经提交的call intent保持原ExecutionBinding并按真实outcome收口，不能静默切LKG。排队/在途若需改用LKG，必须回到repreview并形成新binding/attempt。
- Explicit non-goals:
  - 不提供小说正文、改文、标题或简介写作 Prompt；不批准 family 正文、精确 JSON Schema、阈值、Golden Set 内容或 provider/model。
  - 不声称同一模型自评、单次演示、平均总分或离线提升能保证线上效果；不允许 Prompt 自动自改、自激活或按业务结果无审阅学习。
  - 不把执行 hash 放入 metric label；不在日志/指标中记录 Prompt、正文、评论或模型原始输出。
  - 不批准外部 Prompt 平台、向量库、模型 SDK、预算或线上真实数据二次使用。

## Rationale and Trade-Offs

- Requirement-linked rationale: 三层不可变对象分别回答“测的是什么配置”“凭什么激活”“这次实际跑了什么”，既能复现也避免输入变化污染配置评测。
- Trade-offs accepted: 接受 registry、hash、评测运行、审批和灰度的运维开销，以获得可审计激活、可比较改进和安全回退。
- Negative consequences: Prompt迭代速度低于自由编辑；评测集和人评成本持续存在；模型/provider漂移可能使旧证据过期；JIT事务增加一次锁/校验/提交延迟并产生call-intent/receipt存储；外部provider不支持幂等时，崩溃窗口仍只能保守判为outcome unknown；小样本下统计结论有限。
- Mitigations: 分层 Golden/Regression/Challenge/Shadow Set；版本化 rubric；保留原始逐样例证据和 Wilson/置信区间候选；按风险等级决定门；漂移触发降级/重评而非自动放宽阈值。

## Impact

- Modules, ownership, and dependency direction: governance owner 管 Prompt 定义/激活，execution runtime 只解析 Active binding 并写可信 envelope，领域模块只通过 family/typed input/output 窄合同消费候选；provider adapter 不反向进入领域。
- Public contracts, data, compatibility, and migration: 需版本化 config/evaluation/execution/envelope 和 activation receipt。旧执行永久绑定旧 hash；新 config 不追溯改写历史。Schema/枚举变化需兼容分类和 repreview 策略。
- Reliability, failure, recovery, and operations: registry不可用、最新EligibilityAssessment不可解析/不eligible或active ref/hash不一致时禁止新AI调用；已有正式事实不受影响；Worker不得绕过JIT endpoint直接调用。call-start提交前可安全放弃/重领；提交后API/Worker/provider任一响应不明均按副作用可能发生收口，DeliveryStore保存未获result-or-discard receipt的结果。在途attempt按原ExecutionBinding记录真实outcome，不能静默换模重试。
- Performance and capacity: 增加配置解析、hash、证据存储、双轨评测和每次call-start锁/事务开销；在线路径只查稳定active revision/缓存候选，但缓存不能成为权威。必须分别测precheck/context、call-start事务、provider、validation和candidate-ready延迟，并只使用有界family/model/provider/workload标签；精确阈值仍Unknown/Unverified。
- Security, privacy, and compliance: Prompt 最小化输入；截图/密钥/凭证/跨任务内容不入模；trusted metadata 与模型 payload 分离；评测集、原始输出和激活权限需访问控制与审计。
- Deployment, rollout, rollback/forward recovery: 先扩展兼容的call-intent/receipt字段与internal contract，再部署能理解但不强制JIT的API/Worker，验证后原子启用“required JIT”capability，最后移除旧调用路径。先注册Candidate与EvaluationBinding；通过门后以新activation revision小范围启用；撤销时原子切换到last-known-good/no-AI，尚未call-start的新调用不再使用被撤销版本；已提交/历史仍保留原binding并真实收口，不覆盖正式业务事实。旧Worker不能在required JIT环境claim对应job。
- Technical debt introduced or retired: 退休单一 Effect Bundle、自由 Prompt 编辑和不可重建执行风险；引入评测资产维护、职责分离和证据保留成本，必须有 owner。

## Implementation and Verification

- File-level plan: 接受后先冻结 family/Schema/状态与 owner，再审批 persistence/API/UIUX/安全合同，最后实现 registry、runner、activation、envelope、telemetry 和回退。当前 ADR 不授权代码或模型调用。
- Architecture/contract/failure/performance checks:
  - canonical serialization/hash、不可变binding、append-only assessment revision/current projection、并发 invalidation+activate/revoke、唯一 Active、stale activation 和 envelope 防伪合同测试。
  - Golden/Regression/Challenge/Shadow 数据隔离、泄漏检查、逐维 rubric、零容忍项、paired order swap、judge-human 校准和失败样例复审。
  - registry/provider/judge 不可用、hash mismatch、Schema invalid、预算/政策过期、canary 严重事故、last-known-good 缺失和 no-AI 回退演练。
  - JIT合同测试覆盖并发call-start、相同intent同/异hash、stale lease/fencing/job revision、attempt/step/binding错配、activation在锁前/锁后撤销、预算耗尽、删除/取消竞态、事务提交/响应丢失、Worker崩溃、provider有/无幂等、DeliveryStore满载和result receipt丢失；任何重复外部副作用或绕过JIT调用为Failed。
  - 记录质量、安全、成本、延迟和漂移原始结果；没有批准样例/阈值/人工标注时 `evaluationEvidenceStatus/eligibilityStatus=Unverified`，配置生命周期最多为 Draft/Candidate，不能 Active。
- Mixed-version or migration sequence: 先支持读取旧/新config schema与call-intent字段，再生成新binding和shadow结果；API capability只向支持同一JIT schema的Worker发job，混合版本期间旧Worker不得claim required-JIT workload；观察窗口后才移除旧路径/归档旧版本。撤销不删除历史。
- Success and failure evidence: 需要数据集清单/hash、rubric/阈值版本、原始逐样例输出、盲评/校准结果、审批/activation receipt、call-start/ModelCall/lease/fencing/result receipt关联、故障注入、canary轨道、漂移和rollback/no-AI演练。文档完整、一次模型演示或仅有call-intent记录都不是效果/可靠性证据；当前全部Unverified。

## Revisit Triggers

- Confirmed scale or load threshold: family/模型组合、评测样本、上下文体量、成本或延迟达到已确认扩容/分层阈值。
- New consumer or implementation: 新 provider/model、外部 Prompt 平台、自动工具调用、金融 family、线上学习或第二个真实领域消费者。
- Reliability/performance budget change: 质量/安全零容忍、成本、延迟、数据驻留、评测保留或回退目标变化。
- Due phase/date: 首个真实 AI 调用前必须接受且完成首版 baseline；每次 Active/重大模型或政策变化重新核验。未接受时 Prompt 仅可 Draft/Candidate。
