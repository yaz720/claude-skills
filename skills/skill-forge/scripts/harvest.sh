#!/usr/bin/env bash
# harvest.sh — 把一个真实翻车案例回灌进技能的 evals/,成为防回归的新测试。
# 这是"真闭环":测试集是用出来的,不是一次性造的。
#
# 用法:
#   bash harvest.sh <path/to/skill> "<失败输入>" <fire|no-fire|capability> ["能力测试的一条 check"]
#
# fire/no-fire   → 追加进 evals/triggering/cases.yaml
# capability     → 追加进 evals/capability/cases.yaml(需再给一条 check)
set -euo pipefail

SKILL_DIR="${1:-}"; INPUT="${2:-}"; KIND="${3:-}"; CHECK="${4:-}"
if [[ -z "$SKILL_DIR" || -z "$INPUT" || -z "$KIND" ]]; then
  echo "❌ 用法: bash harvest.sh <path/to/skill> \"<失败输入>\" <fire|no-fire|capability> [\"check\"]" >&2
  exit 1
fi

STAMP="$(date +%Y%m%d-%H%M%S)"

case "$KIND" in
  fire|no-fire)
    F="$SKILL_DIR/evals/triggering/cases.yaml"
    ID="harvest-$STAMP"
    printf '\n- { id: %s, input: %s, expect: %s }  # harvested\n' \
      "$ID" "$(printf '%q' "$INPUT")" "$KIND" >> "$F"
    echo "✅ 已追加触发用例 $ID → $F (expect=$KIND)"
    ;;
  capability)
    [[ -z "$CHECK" ]] && { echo "❌ capability 需再给一条 check" >&2; exit 1; }
    F="$SKILL_DIR/evals/capability/cases.yaml"
    ID="harvest-$STAMP"
    {
      printf '\n- id: %s   # harvested\n' "$ID"
      printf '  input: %s\n' "$(printf '%q' "$INPUT")"
      printf '  check:\n    - %s\n' "$(printf '%q' "$CHECK")"
    } >> "$F"
    echo "✅ 已追加能力用例 $ID → $F"
    ;;
  *)
    echo "❌ kind 必须是 fire | no-fire | capability" >&2; exit 1 ;;
esac

echo "下次改动前跑 eval_run.py,这条就成了防回归护栏。"
