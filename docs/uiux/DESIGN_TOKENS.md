# FlowVerse Design Tokens

## Status

- These are initial V1 design values supplied by the user's product specification and referenced by ../product/V1_PRODUCT_BRIEF.md.
- Reconcile future package tokens through ../intake/V1_PACKAGE_INTAKE.md; never resolve a conflict silently.
- No machine-readable token source exists yet.
- When implementation begins, map these values into one canonical token file before component use.

## Color

| Semantic role | Value |
|---|---|
| Main background | #F6F1E7 |
| Background gradient start | #F8F3EA |
| Background gradient end | #F1ECE2 |
| Surface / card | #FCFAF5 |
| Primary text | #243238 |
| Body text | #53605F |
| Muted text | #89918B |
| AI teal-green | #536F64 |
| Creative warm copper | #B9784D |

## Usage Rules

- Never use pure black for body text.
- Do not use large areas of high-saturation blue.
- Do not introduce black-purple neon or cyberpunk styling.
- Keep backgrounds low-saturation and comfortable for long reading.
- Use AI glow only as restrained ambience; it must not reduce readability.
- Preserve strong contrast for text, controls, focus rings, errors, and disabled states.
- Color must not be the only carrier of meaning.
- Normal-size text must reach 4.5:1 contrast; large text and essential control boundaries must reach 3:1.
- Muted #89918B and copper #B9784D are not approved for normal-size text on the listed light surfaces.
- Use primary or body text tokens for normal text.
- Copper #B9784D may be used for qualifying large text or non-text accents after contrast verification.
- Muted #89918B may be used for qualifying large text only on #FCFAF5; on other listed light surfaces, restrict it to non-essential decoration or non-text accents.
- If no listed token satisfies an essential role, stop for human design approval instead of inventing a color.

## Token Implementation

- Use semantic names based on purpose, not raw color names.
- Keep component code free of repeated arbitrary color literals.
- Reuse spacing, radius, shadow, typography, and motion tokens from the eventual canonical source.
- Any new token requires a documented semantic role and visual verification.
