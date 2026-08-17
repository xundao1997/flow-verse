# ADR-0014: 认证、会话、CSRF 与调试访问

## Metadata

| Field | Value |
|---|---|
| Status | Proposed |
| Decision owner | User / TBD |
| Date | 2026-08-16 |
| Scope IDs | FV1-PRODUCT-DESIGN / FV1-ROADMAP-REVIEW |
| Evidence | `../product/V1_PRODUCT_BRIEF.md`；`../uiux/ACCEPTANCE_CRITERIA.md`；`../engineering/V1_DATA_AND_INTERFACE_CONTRACT_DESIGN.md`；`../engineering/V1_TECHNICAL_SOLUTION_PROPOSAL.md` |
| Supersedes | N/A |

## Context

- V1 有默认用户与管理员两类角色；管理员不能冒充用户或确认用户业务事实。
- 当前 Bootstrap 没有认证、会话、CSRF、密码或 debug access 实现。
- 正式命令、对象 grant、Prompt 管理和 internal Worker 必须使用不同安全边界。

## Options

| Option | Benefits | Costs / risks | Complexity | When valid |
|---|---|---|---|---|
| A. 服务端 opaque session + 角色/能力校验 | 可撤销、浏览器边界清楚、适合当前单产品 | 需要 session 存储和 CSRF | Medium | 当前候选 |
| B. 浏览器长期 JWT | 无状态 | 撤销/轮换/敏感存储更复杂 | Medium | 多独立客户端需求成立后 |
| C. 外部 IdP/SSO | 成熟身份能力 | 厂商/部署/成本尚未选择 | Medium-high | 企业/多用户需求批准后 |
| D. 无认证内部使用 | 开发简单 | 无法满足角色、隐私和正式命令 | Low | 仅本地诊断 |

## Decision

- Proposed option A：浏览器使用 Secure、HttpOnly、SameSite 的 opaque session cookie；服务端保存 hash/expiry/revocation/actor，登录后轮换，敏感动作重验当前 session。
- 所有 state-changing browser request 使用 CSRF token 与 origin/host 检查；CORS 默认同源最小集合。
- 用户与管理员 capability 独立；管理员可配置、监控、审计和运维终止，但不能建立用户业务 session、编辑/确认用户正式事实或绕过 compliance block。
- Worker 使用独立 workload identity/private endpoint，不复用用户 session。
- debug access 是短时、理由、scope、审批和明显 banner 的 grant；默认不读取正文/Prompt/secret，结束后撤销并审计。
- 密码 hash 算法、secret manager、外部 IdP 和精确 TTL 需在依赖/部署批准时冻结，不在本文发明。

## Rationale and Trade-Offs

- 服务端撤销和 capability D2 更符合单产品、敏感正式命令与当前规模。
- 接受 session store/CSRF 的实现成本，换取比长期浏览器 token 更清晰的泄露半径。
- 身份数据最小化；audit 不保存密码、cookie、CSRF、provider secret 或正文。

## Impact

- PostgreSQL 是会话和授权元数据的候选 authority；Redis 不是必需 session authority。
- API/OpenAPI 需要统一 401/403/密码变更/capability 错误；Web 在登出/过期时保留未提交本地草稿但禁止正式提交。
- 发布前需要暴力尝试、枚举、固定 session、CSRF、角色越权、debug grant expiry/revoke 测试。

## Implementation and Verification

- 先批准密码库/版本、cookie/TTL、secret 来源和生产 TLS，再实现 auth slice。
- 单元/集成/E2E 覆盖登录失败统一响应、session rotation/revoke、CSRF、用户/管理员互斥和 internal identity。
- 任何缺失的安全依赖、命令或威胁测试保持 Unverified 并阻断业务发布。

## Revisit Triggers

- 多用户注册、企业 SSO、第三方客户端/API、跨域部署或会话负载测量改变。

