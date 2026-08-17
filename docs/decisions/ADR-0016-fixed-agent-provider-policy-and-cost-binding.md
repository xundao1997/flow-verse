# ADR-0016: 固定 Agent、模型供应商、政策与费用绑定

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../ai/SYSTEM_DECISION_PROMPTS.md`；`../engineering/V1_DETAILED_TECHNICAL_DESIGN.md`；`../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`；`ADR-0029-prompt-configuration-evaluation-and-activation.md` |
| Supersedes | N/A |

## Context

- FlowVerse 是多模型、多 Agent 工作台，但 topology 只读；用户不能自由创建 Agent、Prompt、任意 wiring 或 DAG。
- 模型版本、允许数据、政策、价格和 Prompt 效果会变化，正式结果必须可追溯到当时精确配置。
- 当前没有 provider SDK、model、Agent、价格、调用或费用实现。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. 固定 Agent template + provider adapter + immutable bindings | 可治理、可复现、可替换 | 需要版本/评测/费用治理 | Medium | 当前候选 |
| B. 直接散布 provider SDK 调用 | 初期快 | 政策、重试、费用和输出不可统一 | Low initially | 不满足审计要求 |
| C. 通用 Agent/Workflow Builder | 灵活 | 权限、Prompt注入、成本和UI复杂度极高 | High | 明确第二产品与治理能力后 |
| D. 单一固定模型无 adapter | 最简单 | 静默版本变化与退出风险 | Low | 供应商/模型永不变化时；当前不成立 |

## Decision

- Proposed option A：Agent 是管理员批准的不可变 template version，声明职责、允许 Prompt family、模型 profile、输入数据类别、工具权限、Review rubric 和费用范围；前端只读展示 topology。
- Provider adapter 只暴露冻结的 completion/structured-output/cancel/status 能力，不把供应商原始对象泄漏到领域。
- 每次执行绑定 AgentTemplate、PromptConfig、EvaluationBinding、model/provider exact version、sampling/tool schema、policy/license、price version、input manifest、budget preview 和 human authorization。
- provider policy 使用 green/yellow/red 与允许数据范围；每次 call-start 重验，禁止静默换模、减候选或自动重试收费调用。
- CostLedger 保存估算/实际、币种/单位、provider receipt 与未知状态；费用不由模型 payload 决定。
- 具体 provider、SDK、模型、价格和版本只有在 TECH_STACK/配置审批后才能启用。

## Rationale and Trade-Offs

- 固定 template 提供足够多模型能力，同时守住人类确认、数据范围和成本。
- 接受配置/评测管理成本；换取可回退、可审计和供应商替换能力。
- 不追求供应商所有特性的最低公分母；adapter 可按能力声明，不支持时 fail closed。

## Impact

- Worker 只能执行已授权 binding，模型输出始终是 candidate。
- 管理员可配置/激活/撤销，但不能确认用户内容或业务决策。
- 供应商故障只影响对应 AI capability；确定性/人工路径按 UIUX 降级合同继续。

## Implementation and Verification

- provider contract tests 覆盖 timeout、429/5xx、partial/invalid schema、unknown outcome、cancel、费用和静默 alias 变化。
- 每个 active Prompt family 必须有 Golden/hidden set、人评/judge校准、成本/时延与 Pilot/Canary 证据。
- 无 verified LKG 时 revoke 后关闭 AI，不凭点击率、单次收益或 judge 自动晋升。

## Revisit Triggers

- 第二供应商真实接入、工具调用/流式需求、数据区域变化、成本/SLO变化或第二领域证明共享 Agent 语义。

