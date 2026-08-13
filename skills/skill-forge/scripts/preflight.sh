#!/usr/bin/env bash
# preflight.sh — 评测/打包前的体检:
#   1) claude -p 认证(过期会让触发评测静默读成 0、改写描述步崩)
#   2) description 字数 <= 1024(打包成 .skill 会校验)
#
# 用法: bash preflight.sh <path/to/skill>
set -euo pipefail

SKILL_DIR="${1:-}"
if [[ -z "$SKILL_DIR" || ! -f "$SKILL_DIR/SKILL.md" ]]; then
  echo "❌ 用法: bash preflight.sh <path/to/skill>（该目录需含 SKILL.md）" >&2
  exit 1
fi

FAIL=0

# --- 1) 认证 ---
echo "== 认证检查 (claude -p) =="
if command -v claude >/dev/null 2>&1; then
  if OUT="$(claude -p "OK" 2>&1)"; then
    echo "✅ claude -p 可用"
  else
    echo "❌ claude -p 失败——CLI 登录令牌可能过期。评测会把所有触发静默读成 0,先重新登录。" >&2
    echo "   ($OUT)" >&2
    FAIL=1
  fi
else
  echo "⚠ 未找到 claude CLI,跳过认证检查(触发评测将不可用)。" >&2
fi

# --- 2) description 字数 ---
echo "== description 字数 (<=1024) =="
LEN="$(python3 - "$SKILL_DIR/SKILL.md" <<'PY'
import sys, re
text = open(sys.argv[1], encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---", text, re.S)
fm = m.group(1) if m else ""
# 抓 description: 后面的内容(支持 >- 折叠块)
dm = re.search(r"(?ms)^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", fm)
raw = dm.group(1) if dm else ""
raw = re.sub(r"^\s*[>|][+-]?\s*$", "", raw, flags=re.M)  # 去掉 >- 标记行
desc = " ".join(line.strip() for line in raw.splitlines() if line.strip())
print(len(desc))
PY
)"
if [[ "$LEN" -le 1024 ]]; then
  echo "✅ description = $LEN 字符"
else
  echo "❌ description = $LEN 字符,超过 1024,打包会失败。" >&2
  FAIL=1
fi

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ preflight 通过。"
else
  echo "❌ preflight 未通过,先修上面的问题再评测/打包。" >&2
  exit 1
fi
