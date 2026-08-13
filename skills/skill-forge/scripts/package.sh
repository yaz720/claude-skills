#!/usr/bin/env bash
# package.sh — 调官方 package_skill.py 把技能打成 dist/<name>.skill(会校验 <=1024)。
#
# 用法: bash package.sh <path/to/skill> <output-dir>
#   例: bash package.sh skills/skill-forge ~/Desktop/claude-skills/dist
#
# package_skill.py 的机器路径不硬编码在技能里(见"两层分离"):
#   优先用环境变量 PACKAGE_SKILL_PY;没有则在官方 marketplace 目录里自动找。
set -euo pipefail

SKILL_DIR="${1:-}"
OUT_DIR="${2:-}"
if [[ -z "$SKILL_DIR" || -z "$OUT_DIR" ]]; then
  echo "❌ 用法: bash package.sh <path/to/skill> <output-dir>" >&2
  exit 1
fi

PKG="${PACKAGE_SKILL_PY:-}"
if [[ -z "$PKG" ]]; then
  PKG="$(find "$HOME/.claude/plugins/marketplaces" -name package_skill.py 2>/dev/null | head -1 || true)"
fi
if [[ -z "$PKG" || ! -f "$PKG" ]]; then
  echo "❌ 找不到 package_skill.py。请装官方 skill-creator,或设 PACKAGE_SKILL_PY 指向它。" >&2
  exit 1
fi

echo "== 重新打包(改过 SKILL.md 必重打) =="
mkdir -p "$OUT_DIR"
# package_skill.py 内部 `from scripts.quick_validate import ...`,需把其 skill 根目录放进 PYTHONPATH。
PKG_ROOT="$(cd "$(dirname "$PKG")/.." && pwd)"
# 传绝对路径,避免 cwd 影响
ABS_SKILL="$(cd "$SKILL_DIR" && pwd)"
ABS_OUT="$(cd "$OUT_DIR" && pwd)"
PYTHONPATH="$PKG_ROOT${PYTHONPATH:+:$PYTHONPATH}" python3 "$PKG" "$ABS_SKILL" "$ABS_OUT"
echo "✅ 已生成 .skill 于: $OUT_DIR"
echo "   记得把它一起 git commit(供下载一键装),并 push。"
