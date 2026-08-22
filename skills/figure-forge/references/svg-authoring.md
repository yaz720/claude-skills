# SVG authoring spec

Read this when you are **about to author the SVG** (workflow step 1). SKILL.md keeps only the
non-negotiables; the exact numbers, the palette, and the skeleton live here.

Two things are covered:

- [Design conventions](#design-conventions) — canvas, type scale, color, spacing
- [Self-contained SVG](#self-contained-svg-required-for-the-saved-file) — what the saved file must
  carry on its own, plus a minimal correct skeleton to copy

Why it matters: the saved `.svg` is rendered by `rsvg-convert` **outside** the chat, with none of
the chat widget's CSS. Anything you leave implicit — font, size, fill, background — renders wrong
or not at all.

---

## Design conventions

Keep figures calm and legible — the visual language matches the chat's own design system.

- **Canvas**: `viewBox="0 0 680 H"`, width 680 (matches typical container width; do not change the
  680). Set `H` to the bottom-most element + ~20px. No negative coordinates.
- **Flat only**: solid fills, no gradients / shadows / glow / blur.
- **Sentence case** everywhere — never Title Case, never ALL CAPS, including labels.
- **Two font sizes**: 14px for box/region labels, 12px for subtitles and arrow labels. Nothing
  below 11px.
- **Two weights**: 400 regular, 500 for labels/headings. Never 600/700 (reads heavy).
- **Color**: at most two color families per figure; use a neutral gray as the baseline and color
  only to carry meaning. Mid-tone hexes read fine in both light and dark. A small starter set that
  works well: blue `#4a90d9`, teal `#14b8a6`, gray `#6b6f76`, amber `#d9902a`, red `#d64545`,
  green `#3fa96a`, purple `#8b5cf6`. White text `#ffffff` on these mid-tones; body text `#333333`.
- **No overlaps**: check that no two unrelated boxes/labels/arrows collide. In a row, keep a ≥20px
  gap between boxes. A figure with crossed labels reads as broken no matter how good the content.
- **Rounded corners** (`rx="8"`) on boxes; **1.5px** strokes for light container outlines.

### Self-contained SVG (required for the saved file)

The saved `.svg` is rendered by `rsvg-convert`, which does **not** inherit any chat CSS. So the SVG
must stand on its own:

- Put a font stack on the root: `font-family="-apple-system, 'PingFang SC', 'Helvetica Neue', Arial, sans-serif"`
  so CJK text renders (PingFang SC covers Chinese on macOS).
- Give every `<text>` an explicit `font-size` and `fill` (no reliance on classes).
- Set explicit `width` and `height` on the root `<svg>` in addition to `viewBox`.
- Include a white background rect as the first child by default:
  `<rect x="0" y="0" width="680" height="H" fill="#ffffff"/>` (omit for transparent output).
- Add `role="img"` with `<title>` and `<desc>` as the first children for accessibility.

A minimal, correct skeleton:

```svg
<svg width="680" height="200" viewBox="0 0 680 200" role="img"
     xmlns="http://www.w3.org/2000/svg"
     font-family="-apple-system, 'PingFang SC', 'Helvetica Neue', Arial, sans-serif">
  <title>…</title>
  <desc>…</desc>
  <rect x="0" y="0" width="680" height="200" fill="#ffffff"/>
  <rect x="40" y="40" width="200" height="44" rx="8" fill="#4a90d9"/>
  <text x="140" y="67" text-anchor="middle" font-size="14" fill="#ffffff">label</text>
</svg>
```
