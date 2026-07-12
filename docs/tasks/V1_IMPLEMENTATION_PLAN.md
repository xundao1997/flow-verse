# FlowVerse V1 Implementation Plan

## Status

- Rules baseline is complete only when all required files exist, relative references resolve, AGENTS files stay under 60 lines, and no invented tooling, replacement characters, trailing whitespace, or unresolved high-priority review findings remain.
- V1 is the first implementation; no predecessor, v0.x behavior, migration source, or redesign baseline exists.
- Read current package state and approved scope only from ../intake/V1_PACKAGE_INTAKE.md.
- Business implementation follows the task readiness gate; an approved non-business bootstrap may precede resolved runtime evidence.
- This plan must become file-level after package intake; do not invent paths, frameworks, versions, or commands.

## Prerequisite Gate: V1 Package Intake

- Follow ../intake/V1_PACKAGE_INTAKE.md; preserve and inventory the supplied package before implementation.
- Read ../../AGENTS.md and any applicable nested instructions.
- Classify each artifact and map every conclusion to a specific evidence path.
- Populate ../engineering/TECH_STACK.md from manifests, lockfiles, configuration, CI, or explicit user decisions.
- Populate ../engineering/ARCHITECTURE_BASELINE.md from approved package/source evidence without inventing modules.
- Classify applicable targets in ../engineering/RELIABILITY_BUDGET.md and record baseline debt/decisions.
- Confirm test environments, data scales, commands, and project-specific budgets in ../engineering/PERFORMANCE_BUDGET.md.
- Map the approved V1 package to ../uiux/ACCEPTANCE_CRITERIA.md.
- Set the affected intake scope row to APPROVED only after missing and conflicting facts for that scope are resolved by the user.
- Do not write business code unless intake is APPROVED for the active slice; every other state blocks that slice.

## Phase 0: Conditional Engineering Bootstrap

- If the approved package contains a runnable implementation baseline, verify and inventory it; do not regenerate it.
- Preparation: under an approved bootstrap plan, create only the explicitly listed prerequisite files needed to make the exact bootstrap command verifiable.
- Command execution: verify Confirmed command evidence and Available execution state immediately before running it.
- Bootstrap output is limited to minimum manifests, config, lockfile, quality gates, and measurement entry points.
- Do not add product pages, business behavior, inferred APIs, sample domain data, or optional dependencies during bootstrap.
- Run the generated install/build/check commands, then update resolved versions and command states in ../engineering/TECH_STACK.md.
- Confirm Python/TypeScript dependency-boundary, contract-compatibility, reliability/failure, and technical-debt-reference commands or mark them Unverified.
- Establish the approved lab environment, test data, measurement noise, and initial baseline needed to confirm pre-release budgets.
- Obtain user confirmation for baseline-dependent warning/failure thresholds before feature work that depends on them.

## Phase 1: Architecture and Reliability Baseline

- Confirm scale, data, traffic, team, roadmap, domain, real-time, compliance, budget, deployment, and consistency context needed by architecture choices.
- Register Confirmed target modules, owners, non-goals, data/invariants, public contracts, dependency direction, and adapters; leave pre-code conformance NotYetImplemented.
- Define critical flows, failure domains, deadlines, retry owner/idempotency, degradation, capacity, observability, SLO applicability, and recovery gates.
- Draft ADRs for structural choices; do not implement them until Accepted.
- Map domain unit, contract, adapter integration, failure/recovery, architecture, performance, and E2E test responsibilities.
- Audit the imported baseline into ../engineering/TECH_DEBT_REGISTER.md; do not assume an empty register means zero debt.
- Do not begin cross-module business implementation until affected baseline rows and gates are Confirmed.

## Phase 2: Semantic Tokens

- Implement ../uiux/DESIGN_TOKENS.md in the confirmed canonical token mechanism from the outset.
- Do not introduce arbitrary colors, duplicated tokens, or pure-black body text.
- Confirm the applicable production-build lab budget and baseline before performance-sensitive feature implementation.
- Verify text contrast, focus, disabled states, and 1440 × 900 / 390 × 844 CSS-pixel viewports.

## Phase 3: AI-First Homepage and Navigation

- Make AI intent input the first-screen primary action and show the FlowVerse 流界 brand Logo.
- Add only the required lightweight shortcuts, recent work, and world insight.
- Implement the approved V1 navigation order around AI, current creation, worlds, knowledge, and history.
- Verify AC-01 through AC-05 and AC-10 through AC-13, including the fixed labels in ../uiux/COPY_RULES.md.

## Phase 4: Creative Workspace

- Make manuscript editing the dominant surface.
- Keep AI assistance contextual, supportive, collapsible where space is constrained, and non-technical.
- Complex-task fixtures must generate a workspace; simple-task fixtures must remain in conversation.
- Preserve context, unsaved work, recovery states, and responsive behavior.
- Verify AC-06, AC-10, AC-11, and AC-12.

## Phase 5: World Insight and Health Check

- Implement world state as narrative insight; do not introduce scores, KPIs, charts, or Dashboard presentations.
- Return risk, reason, suggestion, and blocking status.
- Apply conditional primary CTA behavior from ../uiux/INTERACTION_RULES.md.
- Verify AC-07 through AC-10.

## Phase 6: Verification and Review

- Run focused checks after each phase and full repository-defined checks at the end.
- Complete every item in ../uiux/ACCEPTANCE_CRITERIA.md and ../engineering/REVIEW_CHECKLIST.md.
- Execute the AI workflow in ../engineering/AI_CODING_WORKFLOW.md and performance workflow in ../engineering/PERFORMANCE_BUDGET.md.
- Run applicable architecture/contract checks and complete ../engineering/RELIABILITY_BUDGET.md gates.
- Confirm affected architecture target rows, implementation conformance evidence, Accepted ADRs, decision log, and technical-debt register match the implementation.
- Capture visual evidence for required page states at 1440 × 900 and 390 × 844.
- Report unavailable tooling or performance evidence as unverified; never claim a check passed when it could not run.

## Stop Conditions

- V1 package intake is not APPROVED for the affected bootstrap or implementation slice.
- A required target/runtime technology, command, API, asset, source path, or applicable performance gate remains Unknown or TBD, except evidence intentionally produced by an approved bootstrap.
- Specifications conflict or require product judgment.
- Work requires an unapproved dependency, backend contract, schema, auth, runtime, destructive, or security-sensitive change.
- A production dependency cycle, private cross-boundary access, second data owner, or unapproved module/contract/deployment change is introduced.
- At the active Gate stage, an affected reliability row is missing/Applicability Unknown, or a Required target is not Confirmed or its verification is NotYetTested, Failed, or Unverified.
- A confirmed performance budget is exceeded or a critical performance scenario cannot be verified.
