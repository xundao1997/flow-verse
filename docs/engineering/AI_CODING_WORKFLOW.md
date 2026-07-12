# FlowVerse AI Coding Workflow

## Readiness Gates

### Bootstrap Preparation

- Package intake is APPROVED for the named bootstrap scope.
- Target technologies, target version/ranges, and exact bootstrap command evidence are Confirmed.
- The user has approved a minimal bootstrap plan and its allowed files.
- Preparation may create only explicitly listed prerequisite files needed to verify command availability; it adds no product behavior.

### Bootstrap Command Execution

- Immediately before execution, the exact command evidence is Confirmed and execution state is Available.
- Bootstrap output is limited to manifests, config, lockfile, quality gates, and measurement entry points approved by the plan.

### Business Implementation

- Package intake is APPROVED for the active implementation slice.
- Task-relevant target and resolved runtime entries in TECH_STACK.md are Confirmed or N/A.
- Required commands have Confirmed evidence and Available execution state.
- The task has approved acceptance criteria, a file-level scope, and applicable performance gates.
- Cross-boundary work has Confirmed target baseline rows; existing dependencies have Confirmed conformance, while rows created by this task may remain NotYetImplemented until verification.

Unknown facts outside the active slice do not block it. Unknown, Conflict, or TBD facts that the slice actually depends on stop only the affected work.

## 1. Preflight

- Read ../../AGENTS.md, any nearer directory-scoped instructions, the V1 brief, intake, evidence policy, stack registry, acceptance, performance budget, and change policy.
- Inspect Git status, relevant source, tests, config, manifests, lockfiles, and CI.
- Read ARCHITECTURE_STANDARD.md, ARCHITECTURE_BASELINE.md, RELIABILITY_BUDGET.md, TECH_DEBT_REGISTER.md, and applicable Accepted ADRs.
- Separate confirmed facts, assumptions, conflicts, and missing evidence.
- Reproduce an existing defect before proposing its fix when diagnosis is requested.

## 2. File-Level Plan

Before editing, record:

- Goal and user-visible outcome
- Acceptance IDs and exact evidence
- Files to change and files explicitly excluded
- Change class, affected modules/owners, public/private surface, dependency edges, and data ownership
- Public API, data, auth, security, accessibility, compatibility, release-order, and recovery impact
- ADR trigger and evidence for every new abstraction or extension point
- Failure modes, deadline/retry/idempotency/degradation/capacity/observability impact
- Loading, interaction, rendering, network, memory, AI, and bundle performance risks
- Technical debt introduced, touched, repaid, or explicitly N/A
- Exact focused and full verification commands
- Recovery or rollback approach

Do not begin when the plan depends on an unconfirmed path, API, version, tool, command, asset, or budget.

## 3. Implementation

- Make the smallest complete change that satisfies the approved outcome.
- Follow confirmed nearby patterns and reuse existing components, tokens, and abstractions.
- Preserve public contracts unless a breaking change is explicitly approved.
- Do not introduce dependency cycles, private cross-module imports, cross-owner writes, second sources of truth, shared/utils dumping grounds, or god modules.
- Keep domain rules independent of UI, transport, persistence, and provider SDKs.
- Add abstractions only with evidence allowed by ARCHITECTURE_STANDARD.md.
- Do not perform opportunistic refactors, broad reformatting, speculative optimization, or dependency upgrades.
- Do not use empty handlers, fake success, final-state placeholders, unauthorized mocks, swallowed errors, or hard-coded business results.
- Add focused tests for changed behavior and applicable loading, empty, error, recovery, and cancellation states.

## 4. Verification

- Run the narrowest relevant checks first, then required repository-wide checks.
- Use exact commands from TECH_STACK.md and record command, working directory, exit result, and output summary.
- Run applicable dependency-boundary, contract-compatibility, failure/recovery, and debt-reference checks.
- Update affected target/conformance rows with source/config/test evidence; an Accepted ADR is not implementation proof.
- Verify acceptance, accessibility, security, and data safety; measure performance under baseline conditions when an approved performance scenario is affected, otherwise record N/A with reason.
- Review the final diff for unrelated changes, generated files, secrets, stale code, duplication, and contract drift.
- Unavailable or failed checks are Unverified or Failed, never Passed.

## 5. Handoff

Report:

- Changed files and behavior
- Acceptance mapping and supporting evidence
- Commands, results, manual checks, and visual evidence
- Module/dependency/data-owner changes, contract evolution, ADR IDs, reliability evidence, and debt IDs
- Applicable performance environment, baseline, after-result, and delta; otherwise N/A with reason
- Assumptions, Unverified items, remaining risks, and follow-up decisions

## Multi-Agent Work

- Parallelize only independent, bounded tasks; the primary agent owns the global plan and final integration.
- Each subtask declares evidence, allowed files, forbidden scope, acceptance, and time or retry limit.
- Do not let two agents edit the same file concurrently.
- Subagents return conclusion, evidence paths, changed files, verification results, risks, and Unknowns.
- The primary agent revalidates results; a subagent assumption never becomes project fact.
- Stop repeated no-progress attempts instead of retrying blindly.

## Stop Report

Stop the affected work for missing/conflicting required evidence, unapproved scope, a production dependency cycle, unapproved boundary/data-owner/contract change, destructive/security-sensitive action, failed required checks, expired debt, or exceeded/unverifiable reliability/performance gates.

    Status: BLOCKED
    Stop point:
    Evidence checked:
    Missing or conflicting fact:
    Files changed:
    Impact:
    Decision required:
    Safe options:
