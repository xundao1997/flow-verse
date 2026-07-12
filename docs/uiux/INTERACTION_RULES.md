# FlowVerse Interaction Rules

## Primary Flow

    enter through AI assistant
      → express creative intent
      → AI assesses complexity
      → simple task: finish in conversation
      → complex task: generate workspace
      → create chapter
      → run story health check
      → confirm world-history impact
      → continue to the next chapter

## Page Contract

Every page must make these answers clear:

1. Where am I?
2. What is AI helping me do?
3. What should I do next?

## Primary CTA

- Exactly one action receives primary visual emphasis per page state.
- Secondary actions use a link, quiet button, menu, or contextual control.
- A page may offer multiple actions only when one is clearly primary.
- Health check:
  - Blocking risk: primary action is “回到正文修改”; hide or disable forward confirmation so the block cannot be bypassed.
  - Non-blocking risk: primary action is “进入世界历史确认”; “回到正文修改” may remain a quiet secondary action.
  - Never show both actions as peer primary buttons.

## Workspace Rules

- A workspace is a result of AI understanding a complex task.
- Preserve conversation context when entering or leaving a workspace.
- Keep manuscript editing central; panels must not shrink it below a comfortable reading width.
- Explain what will be saved before confirming world-history changes.
- Provide clear loading, empty, error, recovery, and unsaved-change states.

## Forbidden Interaction

- Draggable or connectable workflow nodes
- Agent configuration or Prompt tuning panels
- Multiple peer primary CTAs
- Dense metrics, scoreboards, or chart-first world state
- Hidden destructive actions or irreversible changes without confirmation
