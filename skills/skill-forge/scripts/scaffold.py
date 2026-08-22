#!/usr/bin/env python3
"""
scaffold.py — 为一个新技能生成双兼容目录 + SKILL.md 模板 + evals 模板。

用法:
    # 全局技能(源进技能总库,软链到 ~/.claude/skills/)
    python scaffold.py <new-skill-name> [--repo ~/Desktop/claude-skills]

    # 项目专属技能(源直接放进项目的 .claude/skills/)
    python scaffold.py <new-skill-name> --project /path/to/project

生成后会打印"软链激活"命令;不自动建软链(留给你确认落位)。
"""
import argparse
import os
import sys
from pathlib import Path

NAME_RE = __import__("re").compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

SKILL_MD = """---
name: {name}
description: >-
  TODO —— 以【差异化价值】开头(模型默认不会做的那部分),不要写泛泛的"帮你做 X"。
  精确点名触发场景;中英文触发词并列;必须包含否定例(不要在什么情况触发,尤其相邻易误触的场景)。
  若要打包成 .skill,本段必须 <= 1024 字符(preflight 会核对)。
---

# {name}

TODO —— 一句话说清这个技能是干什么的、它的差异化价值在哪。

## 什么时候用我 / 什么时候别用我

**用我**:TODO

**别用我**:TODO(尤其写清相邻、容易误触的场景)

## 工作流

TODO —— 核心步骤;细节拆进 references/*.md,这里指路(渐进披露)。
"""

TRIGGERING_YAML = """# 触发测试:正例该触发(fire)、负例不该触发(no-fire)
# 负例里务必放几条"本该由别的技能处理"的护栏例。
- {{ id: trig-001, input: "TODO 一条该触发的话", expect: fire }}
- {{ id: trig-neg-001, input: "TODO 一条不该触发的话", expect: no-fire }}
"""

CAPABILITY_YAML = """# 能力测试:触发后活干得好不好。check 由 LLM 裁判逐条判(可含硬检查)。
- id: cap-001
  input: "TODO 一个真实任务"
  check:
    - "TODO 期望产出的一条硬标准"
"""

BAR_YAML = """# 本技能自己的达标线(不搞全局统一线)
triggering: {{ pass_rate: 0.9, negatives_must_pass: all }}
capability: {{ judge_pass_rate: 0.8, runs: 3 }}
judge_model: claude-sonnet-5   # 缺省 Sonnet;判错才升 claude-opus-5;别用 Haiku 当裁判
"""


README_MD = """# {name}

> **状态:🚧 开发中**(尚未跑过基线;跑通并留档后再转 ✅)

一个 Claude Code **技能**:TODO —— 一句话说清它把什么变成什么。

TODO —— 差异化价值:模型不装这个技能也能做点什么,但它**不会自己做**的是哪几件事?
(README 面向"要不要装它"的读者,SKILL.md 面向"已经装了、正要干活"的模型——别把 SKILL.md 抄一遍。)

## 这个技能做什么

- TODO
- TODO

## 边界

TODO —— 不做什么;相邻技能各管什么。

## 仓库结构

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能主文件:frontmatter(触发描述)+ 工作流 |
| `evals/` | 触发用例 + 能力用例 + 分数历史 |

---

> **安装与分发**:本技能随总库一起分发,不是独立仓库。
> 装法(软链激活 / 下载 `dist/{name}.skill` 一键装)见[总库根 README](../../README.md)。
"""


def die(msg: str) -> None:
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold a new Claude Code skill (dual-compatible).")
    ap.add_argument("name", help="new skill name, kebab-case (e.g. md-weekly)")
    ap.add_argument("--repo", default="~/Desktop/claude-skills",
                    help="总库根:公开或私有 monorepo(缺省=公开总库);私密跨项目技能指向你的 private 总库。仅在无 --project 时用")
    ap.add_argument("--project", default=None,
                    help="project path for a PROJECT-scoped skill (source goes to <project>/.claude/skills/)")
    args = ap.parse_args()

    name = args.name.strip()
    if not NAME_RE.match(name):
        die(f"name must be kebab-case lowercase: got '{name}'")

    if args.project:
        base = Path(os.path.expanduser(args.project)) / ".claude" / "skills"
        scope = "project"
    else:
        base = Path(os.path.expanduser(args.repo)) / "skills"
        scope = "global"

    skill_dir = base / name
    if skill_dir.exists():
        die(f"already exists: {skill_dir}")

    # 双兼容目录
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "scripts").mkdir()
    (skill_dir / "evals" / "triggering").mkdir(parents=True)
    (skill_dir / "evals" / "capability").mkdir(parents=True)

    (skill_dir / "SKILL.md").write_text(SKILL_MD.format(name=name), encoding="utf-8")
    (skill_dir / "README.md").write_text(README_MD.format(name=name), encoding="utf-8")
    (skill_dir / "evals" / "triggering" / "cases.yaml").write_text(TRIGGERING_YAML.format(), encoding="utf-8")
    (skill_dir / "evals" / "capability" / "cases.yaml").write_text(CAPABILITY_YAML, encoding="utf-8")
    (skill_dir / "evals" / "bar.yaml").write_text(BAR_YAML.format(), encoding="utf-8")

    # dist/ (仅全局总库需要;项目级技能一般不单独打 .skill)
    if scope == "global":
        (Path(os.path.expanduser(args.repo)) / "dist").mkdir(exist_ok=True)

    print(f"✅ scaffolded [{scope}] skill: {skill_dir}")
    print("\n下一步:")
    print("  1) 撰写:把正文交给官方 skill-creator;起草 description 记得围绕差异化价值 + 否定例 + <=1024。")
    print("     同时把 README.md 的 TODO 填掉(面向读者的门面:装不装它、它替你做什么),")
    print("     并让首行【状态徽标】如实反映评测进度——没跑基线就写 🚧,别默认写成成品。")
    if scope == "global":
        link = f"~/.claude/skills/{name}"
        print(f"  2) 激活(全局):")
        print(f"       ln -s {skill_dir} {link}")
    else:
        print("  2) 项目级技能已在项目的 .claude/skills/ 下,无需软链。")
    print("  3) 预检:  bash <skill-forge>/scripts/preflight.sh " + str(skill_dir))
    print("  4) 测试:  python <skill-forge>/scripts/eval_run.py " + str(skill_dir))
    print("  ★ 别停在 evals 的 TODO 占位:据技能用途起草候选用例(触发正负例 + 能力 rubric),")
    print("     用户过目同意后落地;并立即跑一次【触发基线】(便宜、早抓描述缺陷)。")
    print("     能力基线待技能能真产出时再跑。基线是后续调优判好坏的锚(见 eval-and-tuning.md)。")


if __name__ == "__main__":
    main()
