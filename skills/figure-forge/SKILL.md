---
name: figure-forge
description: >-
  Turn an idea, a dataset, or a sketch into a polished diagram or chart and DELIVER it as real,
  downloadable SVG + PNG files — the part a plain answer skips, since by default Claude only draws
  an inline diagram and stops instead of saving/converting it to a file. Reach for it
  whenever the user wants a figure to keep, download, drop into a doc, or edit: flowcharts,
  architecture/system diagrams, block/wiring schematics, org/relationship charts, timelines and
  roadmaps, side-by-side comparisons, and data charts (bar/line/pie/scatter). Trigger whether the
  user (1) describes what to draw, (2) hands over numbers or a table and wants a fitting chart, or
  (3) gives a sketch to clean up — and ALWAYS when they ask to export, download, save, or convert
  an earlier figure to PNG or SVG. Same intents in Chinese: 画/做 流程图、架构图、示意图、对比图、
  时序图、时间线、柱状图/折线图/饼图, 或 "转成 PNG / 存成图片 / 给我源文件 / 要能下载的图". Do NOT
  use for AI-generated or imagined artwork (logos, illustrations, photorealistic art, "画一只猫")
  — use the image tool instead.
---

# diagram — figures delivered as files

The reason to reach for this skill is not "draw something" (Claude can already emit an inline
SVG). It is **delivery**: turn an intent, a dataset, or a sketch into a figure and hand it back as
**real, downloadable files (SVG + PNG)** the user can keep, open, edit, or paste into a doc. That
last mile — save an actual file, convert it to PNG, place it, return it — is what a plain reply
skips, and it's the whole point here. Inline-preview download buttons are unreliable, so this
skill always writes real files and delivers them explicitly.

It draws with **code** (hand-authored SVG, or a plotting approach for data). It does **not** do
generative/AI image creation — if the user wants imagined art, say that needs the chat image tool
and stop.

## Three input modes → one engine

The front door differs; everything after "design" is identical.

| Mode | User gives | Extra first step |
|------|-----------|------------------|
| 1. Instruction | "draw a flowchart of X" | none |
| 2. Data | a table / numbers | **decide the fitting chart type** |
| 3. Sketch | a hand-drawn image | **read the sketch, infer its structure** |

For mode 2, pick the chart that fits the question: comparison across categories → bar; trend over
time → line; parts of a whole (≤5 slices) → pie/donut; correlation → scatter. When the choice is
genuinely ambiguous, state your pick in one line and proceed — don't stall.

For mode 3, reproduce the sketch's *structure and intent*, not its wobble: clean boxes, aligned
rows, consistent spacing. Keep the user's labels and layout; upgrade only the execution.

## Workflow

1. **Design + author a self-contained SVG.** Follow the design conventions below. Critically, the
   SVG must be *self-contained* — explicit `font-family`, explicit hex colors, and (by default) a
   white background rect — because it will be rendered outside the chat by `rsvg-convert`, which
   has none of the chat widget's CSS. See "Self-contained SVG" below.
2. **Preview it inline** by passing the same SVG to `show_widget` (visualize) so the user sees it
   immediately in the conversation. (If that tool isn't available, skip straight to files.)
3. **Write the SVG to a file** in the output directory (see "Where files go").
4. **Convert to PNG.** The engine is `rsvg-convert` (from `librsvg`) — best quality, handles CJK:
   ```bash
   rsvg-convert -z 3 -o <name>.png <name>.svg     # -z 3 = 3× for a crisp raster
   ```
   A bundled convenience wrapper with a QuickLook fallback lives beside this skill at
   `scripts/svg2png.sh <file.svg> [scale] [out.png]`; use it if you can resolve its path,
   otherwise call `rsvg-convert` directly.
5. **Deliver both files** with `SendUserFile` (SVG + PNG). This is the step that makes download
   reliable — do not skip it, and do not rely on any inline widget's download button.
6. **Leave a reproducible command** in your reply so the user can re-convert themselves.

## Where files go

- Save into a `diagrams/` subfolder of the **current project** (the working directory), e.g.
  `./diagrams/<name>.svg` and `.png`. Keeping them in a subfolder avoids cluttering the repo root.
- If the working directory is the user's home directory (`~`) or otherwise not a real project,
  save to `~/Downloads/` instead — don't scatter files across `$HOME`.
- Name files after their content in kebab-case (`auth-flow.svg`, `q4-revenue-by-region.png`).

## Defaults (so you don't re-ask every time)

- **Both formats**: SVG (vector, editable) + PNG (raster, easy to paste into docs/chat).
- **PNG background: white.** Our figures use dark text; a transparent PNG dropped onto a dark
  surface makes the text vanish. White travels safely everywhere. If the user asks for
  transparent, remove the background `<rect>` and pass through — `rsvg-convert` preserves alpha.
- **PNG scale: 3×** for a sharp result. Go higher only if the user wants a very large image.
- For a **chart built from data** where you use a plotting library that renders to canvas rather
  than SVG, the "both formats" default relaxes to PNG-only — canvas has no clean SVG export. Say
  so in one line. Prefer an SVG-based approach when the chart is simple enough to keep both.

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

## Dependencies

- PNG conversion needs `rsvg-convert` (from `librsvg`): `brew install librsvg` (macOS). It handles
  CJK via fontconfig. `scripts/svg2png.sh` falls back to macOS `qlmanage` (QuickLook) if
  `rsvg-convert` is absent — usable but lower quality (square-padded).

## Example

**Input** (mode 1): "画个流程图,说明我 Git 自动推送的判断:改动是否收尾 → 是就 push,否则只本地 commit。"

**What to do**: author a 3–4 node horizontal flowchart with an arrow-labeled branch, preview it
inline, write `./diagrams/git-push-decision.svg`, convert to PNG at 3×, and deliver both with a
one-line note plus the re-convert command.
