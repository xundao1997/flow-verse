# FlowVerse Agent Instructions

## Version Identity
- FlowVerse V1 is the first product release and an initial implementation.
- No v0.x product, predecessor app, legacy behavior, migration source, upgrade path, or redesign baseline exists.
- Read package state and approved scope only from docs/intake/V1_PACKAGE_INTAKE.md; do not copy dynamic status or infer missing facts.

## Sources of Truth
- Product: docs/product/PRODUCT_POSITIONING.md and docs/product/V1_PRODUCT_BRIEF.md
- Evidence and package gate: docs/governance/EVIDENCE_POLICY.md and docs/intake/V1_PACKAGE_INTAKE.md
- Stack, architecture, reliability, coding, performance, debt, and change control: docs/engineering/
- UIUX and acceptance: docs/uiux/
- Delivery plan: docs/tasks/V1_IMPLEMENTATION_PLAN.md
- Resolve conflicts by docs/governance/EVIDENCE_POLICY.md; stop the affected work instead of choosing silently.

## Key Conventions
- FlowVerse is AI Assistant First; users express intent before learning system structure.
- Simple tasks finish in conversation; complex tasks generate a creative workspace.
- Do not expose Workflow, Agent, Prompt, RAG, or node-graph concepts in user-facing UI.
- The homepage is not a Dashboard; chapter writing is the main stage.
- World state is narrative insight, not KPI analytics.
- Use one primary CTA per page and a low-saturation, warm, readable visual system.
- Modules are cohesive, data ownership is singular, public contracts are explicit, and production dependencies are directed and acyclic.
- Extensibility requires a confirmed variation; prefer the simplest local design over speculative abstraction.

## Required AI Workflow
- Follow docs/engineering/AI_CODING_WORKFLOW.md for every code task.
- Do not write business code until the task's intake scope, target stack, resolved runtime, commands, acceptance, and applicable budgets satisfy the workflow gate.
- A user-approved, non-business bootstrap may run under docs/tasks/V1_IMPLEMENTATION_PLAN.md to create the first evidenced manifest, lockfile, tooling, and baseline.
- Before editing, state evidence, goal, acceptance IDs, module/data owner, affected and excluded files, contracts/dependencies, ADR/debt impact, reliability/performance risks, verification, and recovery.
- Make the smallest complete change; preserve user work, public contracts, nearby patterns, and task scope.
- Never invent files, APIs, schemas, assets, copy, dependencies, versions, commands, environment values, results, screenshots, or performance claims.
- Human approval is required for product, UIUX, acceptance, dependency, API, schema, auth, runtime, architecture, destructive, security, sensitive-data, or budget changes.

## Package Manager
- Read target choice, resolved version, and command state only from docs/engineering/TECH_STACK.md.
- Execute only commands with Confirmed evidence and Available execution state; .gitignore is not technology evidence.

## File-Scoped Commands
| Task | Command |
|---|---|
| Lint / format / typecheck | See docs/engineering/TECH_STACK.md command registry |
| Unit / integration / E2E test | See docs/engineering/TECH_STACK.md command registry |
| Build / performance | See docs/engineering/TECH_STACK.md command registry |
| Architecture / contract / reliability | See docs/engineering/TECH_STACK.md command registry |

## Done Means
- Applicable product, architecture, reliability, UIUX, accessibility, test, and performance acceptance passes with recorded evidence.
- Run exact repository-defined checks; mark missing checks Unverified, never Passed.
- Report changed files, behavior, commands and results, applicable performance before/after, assumptions, unverified items, and remaining risks; use N/A with reason when performance is unaffected.

## Commit Attribution
- AI-authored commits MUST include a valid runtime-provided co-author trailer.
- If no canonical model name and email are available, do not create the commit; report the blocker.

    Co-Authored-By: model name <runtime-provided-email>
