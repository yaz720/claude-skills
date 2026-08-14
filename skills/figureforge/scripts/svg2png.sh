#!/usr/bin/env bash
# svg2png.sh — convert an SVG to a PNG.
#
# Usage:  svg2png.sh <input.svg> [scale] [output.png]
#   scale     raster zoom factor (default: 3)
#   output    output path (default: input with .png extension)
#
# Prefers rsvg-convert (librsvg) for quality + correct CJK rendering.
# Falls back to macOS qlmanage (QuickLook) if rsvg-convert is missing.

set -euo pipefail

IN="${1:?usage: svg2png.sh <input.svg> [scale] [output.png]}"
SCALE="${2:-3}"
OUT="${3:-${IN%.svg}.png}"

if [ ! -f "$IN" ]; then
  echo "svg2png: input not found: $IN" >&2
  exit 1
fi

if command -v rsvg-convert >/dev/null 2>&1; then
  rsvg-convert -z "$SCALE" -o "$OUT" "$IN"
  echo "$OUT"
elif command -v qlmanage >/dev/null 2>&1; then
  # QuickLook fits the image into a square of side N and pads the rest.
  # Size the square off the canonical 680px width so scale still applies.
  SIDE=$(( 680 * SCALE ))
  DIR="$(cd "$(dirname "$OUT")" && pwd)"
  qlmanage -t -s "$SIDE" -o "$DIR" "$IN" >/dev/null 2>&1
  mv -f "$DIR/$(basename "$IN").png" "$OUT"
  echo "$OUT (via qlmanage fallback — square-padded; install librsvg for a tight crop)" >&2
  echo "$OUT"
else
  echo "svg2png: no converter found. Install one with:  brew install librsvg" >&2
  exit 1
fi
