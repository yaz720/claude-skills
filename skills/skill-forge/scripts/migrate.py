#!/usr/bin/env python3
"""
migrate.py — 把一个**已存在的旧技能**收编进当前 skill-forge 标准布局(双兼容 monorepo)。

和 scaffold.py 互补:scaffold 从零新建,migrate 移植现有。适用于:
  - 一个 `.skill` 打包文件(zip)
  - 一个散装技能文件夹(内含 SKILL.md,可能还带 references/ scripts/)
  - 一个孤零零的 SKILL.md 文件

用法:
    # 全局技能 → 收进技能总库 skills/<name>/
    python migrate.py <源(.skill / 文件夹 / SKILL.md)> [--name <kebab-name>] [--repo ~/Desktop/claude-skills]

    # 项目专属技能 → 收进 <project>/.claude/skills/<name>/
    python migrate.py <源> --project /path/to/project [--name <kebab-name>]

行为要点(可安全重复跑):
  - **非破坏**:不动你的原件;目标已存在则拒绝(除非 --force 覆盖)。
  - **保留**源里已有的正文 / references/ / scripts/ / 任何附带资产。
  - **补齐**缺失的标准骨架:references/、scripts/、evals/{triggering,capability}/、evals/bar.yaml
    (用与 scaffold 完全相同的模板,让移植来的技能和新建的长一个样)。
  - name 优先取 SKILL.md frontmatter 的 name:;没有再退到 --name 或源文件名(kebab 校验)。
  - 打印激活软链 + 预检 / 评测的下一步命令(与 scaffold 一致)。
  - 移植后照常走 preflight → eval → package → publish。
"""
import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

# 复用 scaffold 的 evals 模板,保证"移植来的"和"新建的"骨架一模一样
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from scaffold import TRIGGERING_YAML, CAPABILITY_YAML, BAR_YAML
except Exception:  # 万一 scaffold 不可导入,内联兜底(与 scaffold 保持同义)
    TRIGGERING_YAML = ("# 触发测试:正例该触发(fire)、负例不该触发(no-fire)\n"
                       "- {{ id: trig-001, input: \"TODO 一条该触发的话\", expect: fire }}\n"
                       "- {{ id: trig-neg-001, input: \"TODO 一条不该触发的话\", expect: no-fire }}\n")
    CAPABILITY_YAML = ("# 能力测试:触发后活干得好不好。check 由 LLM 裁判逐条判。\n"
                       "- id: cap-001\n  input: \"TODO 一个真实任务\"\n  check:\n    - \"TODO 期望产出的一条硬标准\"\n")
    BAR_YAML = ("triggering: {{ pass_rate: 0.9, negatives_must_pass: all }}\n"
                "capability: {{ judge_pass_rate: 0.8, runs: 3 }}\njudge_model: claude-sonnet-5\n")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
IGNORE = shutil.ignore_patterns(".git", ".DS_Store", "__pycache__", "*.pyc", "node_modules")


def die(msg: str) -> None:
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def slugify(raw: str) -> str:
    s = re.sub(r"\.skill$|\.md$", "", raw.strip(), flags=re.I)
    s = s.strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def find_skill_md(root: Path):
    """在 root 里找 SKILL.md:先看根,再看直接子目录一层。返回含 SKILL.md 的目录,找不到返回 None。"""
    if (root / "SKILL.md").is_file():
        return root
    subs = [d for d in sorted(root.iterdir()) if d.is_dir()] if root.is_dir() else []
    for d in subs:
        if (d / "SKILL.md").is_file():
            return d
    return None


def parse_frontmatter(skill_md: Path):
    """轻量解析 frontmatter,返回 (name, description_text)。不依赖 PyYAML。
    description 可能是折叠标量(>- / |),这里粗取其后所有缩进行拼成一段,仅供字数近似核对。"""
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not m:
        return None, None
    fm = m.group(1)
    name = None
    nm = re.search(r"^name:\s*(.+?)\s*$", fm, re.M)
    if nm:
        name = nm.group(1).strip().strip("'\"")
    # description:从该行到下一个顶层 key(^\S:)或块末
    desc = None
    dm = re.search(r"^description:\s*(.*)$", fm, re.M)
    if dm:
        after = fm[dm.end():]
        lines = [dm.group(1)]
        for ln in after.splitlines():
            if re.match(r"^\S.*:", ln):  # 下一个顶层 key
                break
            lines.append(ln)
        joined = " ".join(x.strip() for x in lines)
        joined = re.sub(r"^[>|][-+]?\s*", "", joined).strip()  # 去掉折叠标量记号
        desc = re.sub(r"\s+", " ", joined).strip()
    return name, desc


def main() -> None:
    ap = argparse.ArgumentParser(description="Migrate an existing skill into the skill-forge standard layout.")
    ap.add_argument("source", help="源:一个 .skill 文件、一个技能文件夹、或一个 SKILL.md")
    ap.add_argument("--name", default=None, help="覆盖技能名(kebab-case);缺省取 frontmatter 的 name:")
    ap.add_argument("--repo", default="~/Desktop/claude-skills", help="全局技能的 monorepo 根(缺省 ~/Desktop/claude-skills)")
    ap.add_argument("--project", default=None, help="项目专属:源放进 <project>/.claude/skills/")
    ap.add_argument("--force", action="store_true", help="目标已存在时覆盖(默认拒绝,保护已有技能)")
    args = ap.parse_args()

    src = Path(os.path.expanduser(args.source))
    if not src.exists():
        die(f"源不存在:{src}")

    tmpdir = None
    lone_md = None      # 若源是单个 SKILL.md
    src_root = None     # 含 SKILL.md 的目录(用于整目录拷贝)

    if src.is_file() and src.suffix.lower() == ".skill":
        tmpdir = Path(tempfile.mkdtemp(prefix="skforge-migrate-"))
        try:
            with zipfile.ZipFile(src) as z:
                z.extractall(tmpdir)
        except zipfile.BadZipFile:
            die(f"不是有效的 .skill(zip)文件:{src}")
        src_root = find_skill_md(tmpdir)
        if not src_root:
            die(f".skill 里找不到 SKILL.md:{src}")
    elif src.is_file() and src.name.lower().endswith(".md"):
        lone_md = src
    elif src.is_dir():
        src_root = find_skill_md(src)
        if not src_root:
            die(f"文件夹里(根或一层子目录)找不到 SKILL.md:{src}")
    else:
        die(f"不认识的源类型:{src}(需 .skill / 文件夹 / *.md)")

    skill_md = (src_root / "SKILL.md") if src_root else lone_md
    fm_name, fm_desc = parse_frontmatter(skill_md)

    # 定名:--name > frontmatter name > 源文件名
    name = args.name or fm_name or slugify(src.stem if src.is_file() else src.name)
    if not name or not NAME_RE.match(name):
        die(f"技能名非法或无法确定(需 kebab-case,如 doctor-finder):得到 '{name}'。用 --name 指定。")

    # 目标
    if args.project:
        base = Path(os.path.expanduser(args.project)) / ".claude" / "skills"
        scope = "project"
    else:
        base = Path(os.path.expanduser(args.repo)) / "skills"
        scope = "global"
    dest = base / name

    if dest.exists():
        if not args.force:
            die(f"目标已存在:{dest}(要覆盖加 --force;否则改名或先删)")
        shutil.rmtree(dest)

    actions = []

    # 1) 落主体
    if src_root:
        shutil.copytree(src_root, dest, ignore=IGNORE)
        actions.append(("(整个技能目录)", "从源拷入", "kept"))
    else:  # lone md
        dest.mkdir(parents=True)
        shutil.copy2(lone_md, dest / "SKILL.md")
        actions.append(("SKILL.md", "从源拷入", "kept"))

    if fm_name and args.name and fm_name != args.name:
        actions.append(("frontmatter name", f"'{fm_name}' 与 --name '{args.name}' 不一致(未自动改写 SKILL.md,请手动统一)", "warn"))

    # 2) 补齐标准骨架(只补缺的,不覆盖已有)
    for sub in ("references", "scripts", "evals/triggering", "evals/capability"):
        p = dest / sub
        if not p.exists():
            p.mkdir(parents=True)
            actions.append((sub + "/", "缺失 → 建空目录", "stub"))
        else:
            actions.append((sub + "/", "源已有 → 保留", "kept"))

    stubs = {
        "evals/triggering/cases.yaml": TRIGGERING_YAML.format(),
        "evals/capability/cases.yaml": CAPABILITY_YAML,
        "evals/bar.yaml": BAR_YAML.format(),
    }
    for rel, content in stubs.items():
        p = dest / rel
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            actions.append((rel, "缺失 → 写入模板(占位,待你填真实用例)", "stub"))
        else:
            actions.append((rel, "源已有 → 保留", "kept"))

    # dist/(仅全局)
    if scope == "global":
        (Path(os.path.expanduser(args.repo)) / "dist").mkdir(exist_ok=True)

    if tmpdir:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # 3) 报告
    print(f"✅ migrated [{scope}] skill → {dest}\n")
    print("动作明细:")
    for what, how, tag in actions:
        icon = {"kept": "•", "stub": "＋", "warn": "⚠"}.get(tag, "•")
        print(f"  {icon} {what:<32} {how}")

    # description 字数近似核对(权威校验仍在 preflight / package)
    if fm_desc is not None:
        n = len(fm_desc)
        flag = "✅" if n <= 1024 else "❌ 超限,打包会失败,需精简"
        print(f"\ndescription 近似字数:{n}  {flag}")
    else:
        print("\n⚠ 未能从 SKILL.md 解析到 description —— 确认 frontmatter 是否规范(name/description)。")

    print("\n下一步:")
    if scope == "global":
        link = f"~/.claude/skills/{name}"
        print(f"  1) 激活(全局软链):  ln -s {dest} {link}")
    else:
        print("  1) 项目级技能已在项目 .claude/skills/ 下,无需软链。")
    print(f"  2) 预检:  bash <skill-forge>/scripts/preflight.sh {dest}")
    print(f"  3) 测试:  python <skill-forge>/scripts/eval_run.py {dest}")
    print("  4) 填 evals/ 里的占位用例 → 调优 → package.sh 打包 → 提交并 push。")
    print("\n(原件未改动;这是一份收编进 monorepo 的副本。)")


if __name__ == "__main__":
    main()
