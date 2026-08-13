#!/usr/bin/env python3
"""
eval_run.py — 跑触发测试 + 能力测试,出分栏报告。

用法:
    python eval_run.py <path/to/skill>

依赖: pyyaml (pip install pyyaml)、claude CLI(用于触发判定与 LLM 裁判)。
先跑 preflight.sh 确认认证——否则触发会被静默读成 0(见 references/eval-and-tuning.md)。

设计要点:
- 触发测试:对每条 input 问裁判"带此 description 的技能是不是该被选用",与 expect 比对。
- 能力测试:需要先"运行技能拿到产出"再判;运行环节是接入点(RUN_SKILL_HINT),
  v1 默认从 evals/capability/outputs/<id>.txt 读取已保存的产出,没有则跳过并提示。
- 基准盲区判别:若触发判定"对正负例给出完全相同的结论"(常见于重叠型技能或认证过期),
  报「基准盲区,请人工判」,而不是给出一个会误导的分数。
"""
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ 需要 pyyaml:  pip install pyyaml", file=sys.stderr)
    sys.exit(1)

RUN_SKILL_HINT = (
    "能力测试需要该技能对 input 的实际产出。把产出保存到 "
    "evals/capability/outputs/<case-id>.txt 后重跑,或在 Claude 会话里人工评。"
)


def claude(prompt: str, model: str | None = None) -> str:
    cmd = ["claude", "-p", prompt]
    if model:
        cmd += ["--model", model]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"__ERROR__ {e}"


def load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None


def read_description(skill_dir: Path) -> str:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    import re
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    fm = fm.group(1) if fm else ""
    dm = re.search(r"(?ms)^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", fm)
    raw = dm.group(1) if dm else ""
    raw = re.sub(r"^\s*[>|][+-]?\s*$", "", raw, flags=re.M)
    return " ".join(l.strip() for l in raw.splitlines() if l.strip())


# ---------- 触发测试 ----------
def run_triggering(skill_dir: Path, name: str, desc: str, model: str | None):
    cases = load(skill_dir / "evals" / "triggering" / "cases.yaml") or []
    results = []
    for c in cases:
        q = (
            f"A Claude Code skill named '{name}' has this description:\n\"\"\"\n{desc}\n\"\"\"\n"
            f"For the user request below, is THIS skill the right tool to trigger? "
            f"Answer strictly YES or NO.\nRequest: {c['input']}"
        )
        ans = claude(q, model).upper()
        fired = ans.startswith("YES") if "__ERROR__" not in ans else None
        expect_fire = c["expect"] == "fire"
        ok = (fired == expect_fire) if fired is not None else None
        results.append({"id": c["id"], "expect": c["expect"], "fired": fired, "ok": ok})
    return results


def triggering_blind(results) -> bool:
    fireds = [r["fired"] for r in results]
    if any(f is None for f in fireds):   # 有 ERROR(常是认证过期)
        return True
    return len(set(fireds)) == 1 and len(results) > 1   # 对所有例给出同一结论


# ---------- 能力测试 ----------
def run_capability(skill_dir: Path, model: str | None):
    cases = load(skill_dir / "evals" / "capability" / "cases.yaml") or []
    out_dir = skill_dir / "evals" / "capability" / "outputs"
    results = []
    for c in cases:
        out_file = out_dir / f"{c['id']}.txt"
        if not out_file.exists():
            results.append({"id": c["id"], "skipped": True})
            continue
        output = out_file.read_text(encoding="utf-8")
        checks = c.get("check", [])
        q = (
            "You are a strict evaluator. Given a task, a produced output, and a rubric, "
            "judge each rubric item PASS or FAIL with a one-line reason. Return JSON: "
            '[{"item":..,"pass":true/false,"reason":..}].\n'
            f"TASK: {c['input']}\nOUTPUT:\n{output}\nRUBRIC: {json.dumps(checks, ensure_ascii=False)}"
        )
        verdict = claude(q, model)
        results.append({"id": c["id"], "verdict": verdict})
    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python eval_run.py <path/to/skill>", file=sys.stderr)
        sys.exit(1)
    skill_dir = Path(sys.argv[1]).expanduser().resolve()
    name = skill_dir.name
    bar = load(skill_dir / "evals" / "bar.yaml") or {}
    model = bar.get("judge_model")
    desc = read_description(skill_dir)

    print(f"=== eval: {name} (judge={model or 'default'}) ===\n")

    print("── 触发测试 (triggering) ──")
    trig = run_triggering(skill_dir, name, desc, model)
    if triggering_blind(trig):
        print("⚠ 基准盲区:对正/负例结论无区分度(重叠型技能或认证过期?)——请人工判,勿信分数。")
    total = len(trig)
    passed = sum(1 for r in trig if r["ok"])
    negs = [r for r in trig if r["expect"] == "no-fire"]
    negs_ok = all(r["ok"] for r in negs) if negs else True
    for r in trig:
        mark = "✅" if r["ok"] else ("⚠" if r["ok"] is None else "❌")
        print(f"  {mark} {r['id']}: expect={r['expect']} fired={r['fired']}")
    print(f"  → {passed}/{total} 通过; 负例全过: {negs_ok}\n")

    print("── 能力测试 (capability) ──")
    cap = run_capability(skill_dir, model)
    if not cap:
        print("  (无用例)")
    for r in cap:
        if r.get("skipped"):
            print(f"  ⚠ {r['id']}: 缺产出,跳过。{RUN_SKILL_HINT}")
        else:
            print(f"  {r['id']} 裁判结论:\n    {r['verdict']}")

    print("\n达标线:", bar)
    print("提示:调优请在 tune/<name> 分支上跑,只收总分严格变高的改动(见 eval-and-tuning.md)。")


if __name__ == "__main__":
    main()
