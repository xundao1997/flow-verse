# Frontend Agent Instructions

## Scope
- Applies only under services/web/ and extends ../../AGENTS.md.
- Presence of this file does not prove a framework, package manager, source layout, or current implementation state.

## Required Reading
- ../../docs/product/V1_PRODUCT_BRIEF.md
- ../../docs/intake/V1_PACKAGE_INTAKE.md
- ../../docs/engineering/TECH_STACK.md
- ../../docs/engineering/ARCHITECTURE_STANDARD.md
- ../../docs/engineering/ARCHITECTURE_BASELINE.md
- ../../docs/engineering/RELIABILITY_BUDGET.md
- ../../docs/engineering/TECH_DEBT_REGISTER.md
- ../../docs/engineering/AI_CODING_WORKFLOW.md
- ../../docs/engineering/PERFORMANCE_BUDGET.md
- ../../docs/uiux/UIUX_PRINCIPLES.md
- ../../docs/uiux/DESIGN_TOKENS.md
- ../../docs/uiux/INTERACTION_RULES.md
- ../../docs/uiux/COPY_RULES.md
- ../../docs/uiux/ACCEPTANCE_CRITERIA.md

## Stack Gate
- Business code uses only a Confirmed target stack with Confirmed resolved runtime entries and commands whose evidence is Confirmed and execution is Available.
- Lockfile evidence controls resolved versions; do not use “latest” or infer React, Vite, Tailwind, shadcn, or any alternative.
- Create manifests, configs, routes, or directories only in an approved bootstrap or file-level implementation plan backed by evidence.

## Product and UI Rules
- Make AI the primary entry and the writing surface the primary workspace.
- Generate spaces for complex tasks; never make users choose a space first.
- Do not create Dashboard-first, admin-console, Dify-like, or draggable workflow interfaces.
- Do not expose Agent, Workflow, Prompt, RAG, Node, Vector, Token, or model configuration in user copy.
- Show world state as creative insight; use one visually primary CTA per page state.
- Keep layouts calm, warm, readable, responsive, keyboard accessible, and manuscript dominant.

## Implementation and Performance
- Reuse confirmed components and semantic tokens; keep page orchestration out of primitives and business state out of presentation-only components.
- Follow Confirmed module boundaries and dependency directions; cross-feature use goes through public entries with no private deep imports or cycles.
- React pages/components render or orchestrate; they do not own core rules, persistence, database access, or provider SDK integration.
- Server data, editable drafts, and derived view state each have one authoritative owner; do not copy them into competing stores.
- Shared code is stable and domain-neutral with real consumers; do not create global barrel, utils, helpers, manager, or base-service dumping grounds.
- Cover applicable default, loading, empty, error, disabled, success, recovery, and unsaved states.
- Bound lists, history, chat, DOM growth, cache, AI context, concurrency, retries, and polling.
- Cancel and clean up asynchronous work that can outlive its owner or be superseded by a newer user action.
- If an underlying operation cannot be cancelled, document why and provide timeout, stale-response protection, and lifecycle cleanup.
- If approved AI output is streamed, batch UI updates; do not rerender the full conversation or manuscript for every token.
- Preserve Chinese IME, cursor, selection, undo/redo, and draft safety during any approved background persistence.
- Local reversible optimization requires measured need; new dependencies, workers, global/persistent cache semantics, or architecture changes also require approval.

## Validation
- Run only commands with Confirmed evidence and Available execution state in ../../docs/engineering/TECH_STACK.md; prefer file-scoped checks.
- Use a production build and the workflow in ../../docs/engineering/PERFORMANCE_BUDGET.md for performance conclusions.
- Verify required viewports, keyboard behavior, accessibility, and visual evidence.
- If tooling, baseline, data scale, or budget is missing, report Unverified and stop the affected delivery.
