# FlowVerse Design Tokens

## Status and Source

- Approved design values from UIUX `DesignSpec/tokens.json` in the package identified by `../intake/V1_PACKAGE_INTAKE.md`.
- The JSON asset remains the exact authority. This file is a readable repository summary and must not be used to invent missing values.
- During an approved frontend bootstrap, import or map the package JSON into one canonical machine-readable token source before component implementation.

## Color

| Group | Token | Value | Use |
|---|---|---|---|
| Background | canvas / canvasWarm | `#F4F6F5` / `#F7F5F1` | Application and warm display backgrounds |
| Surface | surface / surfaceSoft / surfaceTint | `#FFFFFF` / `#F8FAF9` / `#F0F3F8` | Cards, editor, secondary containers, information sections |
| AI surface | surfaceAi | `#F1F0F8` | Candidate/collaboration state; never fill the manuscript area |
| Text | primary / secondary / muted / faint | `#26312E` / `#43504C` / `#6C7874` / `#929D99` | Body hierarchy; faint is non-essential only |
| Border/focus | default / strong / focus | `#DDE4E1` / `#CBD5D1` / `#596AA6` | Boundaries and focus |
| Brand | primary / primaryStrong / primarySoft | `#596AA6` / `#45588F` / `#EDF0FA` | Primary controls and branded emphasis |
| Brand support | teal / tealSoft / violet / violetSoft | `#4F7C72` / `#EAF3F0` / `#786F9F` / `#F0EDF7` | Formal/success and restrained AI semantics |
| Semantic | success / warning / danger / info / ai | `#477B68` / `#9A6B2F` / `#A45454` / `#5D7398` / `#786F9F` | Always combine with label and icon |

Overlay is `rgba(25, 33, 31, 0.42)`; focus ring is `0 0 0 3px rgba(89, 106, 166, 0.18)`.

## Typography

| Role | Approved value |
|---|---|
| UI | `Inter, Noto Sans SC, Microsoft YaHei, sans-serif` |
| Document | `Noto Serif SC, Songti SC, serif` |
| Chinese brand | `KaiTi, STKaiti, serif` |
| Monospace | `SFMono-Regular, Consolas, Liberation Mono, monospace` |
| Document body | `15px`, line-height `2.05`, ideal measure `680px`, maximum `720px` |
| UI sizes | `10, 12, 14, 18, 20, 24, 30px` with line-height from the canonical JSON |

## Geometry, Motion, and Layout

- Spacing scale: `0, 4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64px`.
- Radius: `6, 8, 12, 18px`, plus pill.
- Touch target minimum: `44px`; standard button `38px`; input minimum `40px`.
- Top bar `64px`; task navigation `220px` (`192px` at 1280); context panel `328px`; drawer `390px`; Agent trace detail `370px`.
- Motion durations: `120ms`, `180ms`, `280ms`; reduced motion removes drawer movement, shimmer, and progress pulse.
- Breakpoints: mobile read-only through `767px`; compact desktop through `1279px`; desktop from `1280px`; wide desktop from `1440px`.

## State Language

| State | Required label |
|---|---|
| Observation | 观察事实 |
| Analysis | AI 分析候选 |
| Recommendation | 行动建议 |
| Human decision | 人类决策 |
| Formal | 已正式确认 |
| Candidate | 候选，尚未正式确认 |
| Blocking | 存在阻断 |
| Stale | 输入已变化 |

## Usage and Accessibility Rules

- Low saturation, fine borders, light shadows, restrained radius, and long-session readability are mandatory.
- Do not use pure black body text, high-saturation enterprise blue, neon graphs, or AI surfaces across manuscript content.
- Minimum text contrast is `4.5:1`; large text and essential control boundaries are `3:1`.
- Focus has a visible equivalent of at least `2px` and is not clipped.
- Every status color includes readable text and an icon; danger copy names the object, impact, and irreversibility.
- Component code uses semantic tokens, not repeated literals. New tokens require design approval and visual/accessibility verification.
