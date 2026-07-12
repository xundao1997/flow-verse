# FlowVerse V1 Product Brief

## Status

- Defines FlowVerse's first product release and initial implementation.
- V1 is not a redesign, migration, upgrade, or continuation of any v0.x product.
- Implementation readiness and package state are recorded only in ../intake/V1_PACKAGE_INTAKE.md and ../engineering/TECH_STACK.md.
- This brief never authorizes an inferred framework, source layout, dependency, version, command, or architecture.
- Default user-interface language is Simplified Chinese (zh-CN); preserve the brand name “FlowVerse 流界”.
- Use the initial V1 design-token baseline in ../uiux/DESIGN_TOKENS.md.
- When the future V1 package conflicts with this brief, stop and request a user decision.

## Goal

Build the first FlowVerse release around:

**AI Assistant First + Dynamic Creative Workspace**

## Primary Journey

    AI assistant
      → express creative intent
      → AI assesses task complexity
      → simple: complete in conversation
      → complex: generate a creative workspace
      → write and refine a chapter
      → run story health check
      → confirm world-history changes
      → continue creating

## V1 Capability Requirements

### Homepage

- Make the AI assistant and large intent input the first-screen focus.
- Show the FlowVerse 流界 brand Logo on the first screen.
- Use the greeting “你好，今天想创造什么？”.
- Support lightweight creation shortcuts, recent creations, and concise world insight.
- Do not present a module chooser, marketing page, Dashboard, or traditional SaaS workbench.

### Navigation

- Use these primary labels and order: “FlowVerse AI”, “当前创作”, “我的世界”, “知识库”, “历史”.
- AI is the primary entry; spaces are not first-level choices.

### Dynamic Workspace

- AI must generate a creative workspace after it identifies a complex task.
- Do not make users select “world / creation / knowledge space” before expressing intent.

### Creative History

- Present AI Flow as creative history or world evolution.
- Do not imply nodes can be dragged, connected, configured, or executed as a workflow builder.

### Chapter Creation

- Make the long-form editor the main stage.
- Keep AI assistance supportive and contextual; it must not crowd out the manuscript.
- On desktop, use collapsible left context, dominant center manuscript, and collapsible right AI assistance.

### World State and Health Check

- Present world state as narrative insight, not charts, percentages, scores, or KPIs.
- Health checks return: risk, reason, suggestion, and whether the issue blocks progress.

## Out of Scope

- Workflow editor, Agent configuration, Prompt editor, model configuration, or node graph
- Unapproved backend, API, database, authentication, or runtime changes
- Frameworks, production dependencies, or architecture not confirmed by the approved V1 package or the user

## Completion

- All items in ../uiux/ACCEPTANCE_CRITERIA.md pass.
- The review in ../engineering/REVIEW_CHECKLIST.md is recorded with evidence.
