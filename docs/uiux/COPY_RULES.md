# FlowVerse Copy Rules

## Status and Authority

- External-package copy and retained product semantics remain the approved evidence baseline identified by `../intake/V1_PACKAGE_INTAKE.md`.
- DecisionCandidate, Prompt-governance, phased-release capability, compact-workspace, D10 conflict-resolution, and system-degradation/recovery additions are `IN_REVIEW / Proposed`. They do not authorize implementation or replace package copy until the synchronized change set receives explicit final human approval.
- Degradation and recovery wording implements the proposed semantics in [System Degradation and Recovery UIUX](SYSTEM_DEGRADATION_AND_RECOVERY_UIUX.md); this file owns user-facing phrasing, not transport field values or retry policy.

## Tone

- A calm, precise editorial workbench
- An attentive collaborator that distinguishes candidates, evidence, formal facts, and human decisions
- Transparent about context, model/provider, data scope, cost, uncertainty, and recovery
- Specific without technical posturing or growth promises

## Locale and Fixed Labels

- Default user-interface locale is Simplified Chinese (zh-CN).
- Brand: “流界 FlowVerse”.
- User page labels: “工作主页”, “任务驾驶舱”, “创作工作台”, “投放与观察”, “复盘与决策”.
- Product terms such as Stage 0, Cycle, Agent, Review, Bot, AI and proper model/provider names may appear where the approved package uses them; explain their business meaning and do not expose implementation jargon.

## Prefer

- “候选，尚未正式确认。”
- “确认并生成正式内容快照。”
- “内容已确认，作品记忆仍待确认，暂不可投放。”
- “确认外部已生效并开始 Cycle {nextCycleNumber}。”（界面显示服务端分配的实际编号；正常路径示例可为 Cycle 2。）
- “输入已变化，请查看差异后重新预览。”
- “AI 决策候选，尚未形成正式事实或人类决定。”
- “证据不足，本次不提供确定建议。”
- “需要人工复核；复核完成后仍需在业务页面正式确认。”
- “此功能未在当前版本启用。”
- “此评测版本不可晋升：缺少有效的人评或回归证据。”
- “部分功能暂不可用；你的输入已保留。”
- “当前显示截至 {asOf} 的数据，可能不是最新状态。”
- “已保存在此设备，尚未同步。”
- “系统尚未确认本次操作结果，请先查看处理结果。”
- “请求较多，请在 {retryTime} 后重试。”（仅在服务器允许重试并提供时间时。）
- State preservation, next action, impact, and recovery in plain language.

## Avoid in User-Facing UI

- Workflow
- Pipeline
- RAG
- Prompt Template
- Node
- Vector
- Model Config
- Token
- “系统繁忙，请稍后重试”（没有明确影响范围、保留状态或可重试证据时）
- “已保存”（只存在本地副本或服务器结果未知时）
- “数据已恢复／当前最新”（没有权威 freshness 与时间证据时）
- “正在自动重试”（没有单一 retry owner、有界策略或服务器许可时）

“Agent” may identify approved novel business roles and actual participation. It must not expose free role creation, topology editing, Prompt tuning, or implementation configuration.

These terms may appear in engineering documentation when technically necessary.

After the roadmap overlay is approved, administrator-only A05 may use the controlled governance terms `PromptConfigBundle`, `EvaluationBinding`, `ExecutionBinding`, “Prompt 版本”, “评测”, “晋升”, “受控试用”, “影子评测”, “激活”, “撤销” and “回退” because they identify governed production assets and actions. It must not invite free-form Prompt tuning, expose hidden holdout/protected input content or secrets, or use “编辑 Prompt” for an action that production A05 does not provide.

## Rules

- Name tasks, story objects, evidence, formal records, and outcomes instead of implementation concepts.
- Do not use vague AI magic claims or imply certainty the system cannot provide.
- Error copy states what happened, whether work was preserved, and the recovery action.
- Degradation copy follows one order: affected capability/scope, freshness and `asOf`, preserved work, then the one safe recovery action. Internal names such as `degradationMode`, raw capability codes, storage/provider locators, and stack details are mapped to approved user language rather than exposed directly.
- Stale or verified last-known-good data always says “截至 {asOf}” and never uses “当前”, “最新”, or “已恢复”. If freshness is unknown, say “无法确认最新状态” and disable actions that require current authority.
- Local-only draft copy is “已保存在此设备，尚未同步”; “已保存到服务器” is reserved for an authoritative server receipt/revision. A failed or unknown formal command says “尚未确认结果” and makes “查看处理结果” the sole primary recovery, not “再次提交”.
- For 429/503, say retry is available only when the authoritative response sets it as retryable. Show `retryAfter` as a localized time/duration when supplied; otherwise do not promise a countdown, automatic retry, or that waiting alone will repair the condition.
- If no verified `lastKnownGoodRef` exists, say “没有可用的已验证版本/快照” and route to the deterministic/manual or safe read-only path. Never call the newest local cache a fallback.
- Confirmation copy explains scope and impact before destructive or persistent changes.
- Observation, AI analysis candidate, recommendation, and human decision use distinct labels.
- A `SemanticFindingCandidate` is rendered by `DecisionCandidatePanel` and user-facing as “AI 决策候选” or the more specific approved business label. Its recommendation is “行动建议”, never “系统决定”, “已批准”, “最佳选择”, or “下一步已确定”.
- Model states use only: `abstain` → “证据不足，本次不提供确定建议” and `needs_human_review` → “需要人工复核”. A deterministic validation block uses “系统校验阻断，当前不能采用”; an authoritative compliance-policy block names that policy owner and reason. Never say the AI candidate itself decided `BLOCK`. Stale/invalid evidence names the invalid source and asks for refresh or correction.
- Do not show model-self-reported confidence by default. If a future approved, human-calibrated coarse hint is introduced, describe it only as a review aid—not a probability, quality guarantee, or permission to proceed—and never show invented precision such as “93%可信”.
- Evidence copy distinguishes “支持证据”, “反证”, “背景依据”, “证据冲突”, and “缺失证据”, and exposes source/version/location in understandable language.
- A capability absent from the current release uses “此功能未在当前版本启用” plus a safe available route. Do not promise a date, call it a permission error, or imply that retrying will unlock it.
- Prompt governance actions use precise verbs: “提交人工审批”, “开始受控试用”, “激活已批准版本”, “紧急撤销”, and—only when a verified target exists—“回退至已验证版本”. The first version instead says “无可回退的已验证版本；停用此 AI 能力并改用人工流程”. Automated evaluation says “离线检查已完成”, never “已自动批准上线”.
- Do not promise platform approval, exposure, growth, signing, income, causality, or market validation.
- Mobile-disabled actions use “请使用桌面端继续此操作”.
- When mobile width and system degradation both apply, state them separately: desktop is required for the prohibited action, while the service/freshness message explains the current system condition. Never imply that changing devices fixes an outage or stale data.
- D10 mobile copy applies to pause, resume, terminate, archive, restore, and delete alike; never describe resume as a mobile-safe exception.
