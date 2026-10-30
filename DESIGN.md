# Design — Ticket del surtidor

World: the thermal receipt of a fuel pump. Each module is one long cream receipt sheet (torn zig-zag bottom edge, mask-based) laid on a warm laminate counter. The world owns the frame — masthead, tab strip, ticket header line, dotted rules, receipts for the manual trace, LED pump display — while the reading column stays calm.

## Scene
Projected in a classroom → light theme only, high-contrast ink on cream paper.

## Tokens
- Ground `--counter #E6E0D2` (dot texture), paper `--paper #FBF8F1`, insets `--paper-2/3`.
- Ink `#1B1D22`, secondary `#45474D`, muted `#66676C`, ghost `#C9C3B6` (decorative only).
- Signal `#C2410C` (text variant `#A3360A`): alerts, ρ > 1, observed series, current selection, "ocupado".
- Blue `#2B5BD7`: expected/theoretical series, grouped χ² categories, proposal figures.
- Go `#1E7A46`: "libre", accepted H₀, met precision.
- Chart pair orange/blue validated with dataviz `validate_palette.js` (light): all checks pass.

## Type
- Display: Archivo, condensed (font-stretch 70–90 %), 800–900, uppercase for view titles.
- Body: Atkinson Hyperlegible 18px (projector legibility).
- Figures, formulas, tables, code: JetBrains Mono, tabular numerals.

## Signature moves
- Big condensed step numerals (1-2-3-4) for worked formulas and question numbers.
- Ghost alternatives: inactive values shown faint, the selected one struck in signal (inverse-transform verifier, clock ghost 888.00).
- The simulation clock snaps between event times; state is a mark (dashed outline = waiting, filled = in service), not only a hue.

## Motion
Custom curves `--ease-out cubic-bezier(.23,1,.32,1)`, `--ease-in-out cubic-bezier(.77,0,.175,1)`. Press feedback scale(.97); car movement 520ms ease-in-out transitions (interruptible); hover gated behind `(hover:hover)`; reduced-motion keeps opacity only.
