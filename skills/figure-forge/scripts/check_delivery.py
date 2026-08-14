#!/usr/bin/env python3
"""
check_delivery.py — 能力测试的「交付真实文件」硬检查(确定性,不靠 LLM)。

figure-forge 的产出是文件,而 LLM 裁判读的是文本、无法可靠核验"文件是否真存在"。
本脚本把这条判据独立出来:解析每个 evals/capability/outputs/<id>.txt 末尾的
    [files] a.svg + b.png
行,核对所列文件(与 txt 同目录)真实存在、非空、且格式正确:
    .svg → 文本里含 <svg 根标签
    .png → 以 PNG 魔数开头 (89 50 4E 47 0D 0A 1A 0A)
    其它 → 仅查存在且非空

用法:
    python check_delivery.py [<path/to/skill>]   # 缺省 skills/figure-forge(相对 CWD)
退出码非 0 表示有用例未通过(可接进 CI / 评测流水线)。
"""
import re
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_file(p: Path):
    if not p.exists():
        return False, "缺失"
    if p.stat().st_size == 0:
        return False, "空文件"
    suf = p.suffix.lower()
    if suf == ".svg":
        head = p.read_text(encoding="utf-8", errors="replace")[:2000]
        return ("<svg" in head), ("含<svg根" if "<svg" in head else "不含<svg根标签")
    if suf == ".png":
        with open(p, "rb") as f:
            ok = f.read(8) == PNG_MAGIC
        return ok, ("PNG魔数正确" if ok else "PNG魔数不符")
    return True, "存在非空"


def parse_files_line(txt: Path):
    """取末尾 [files] 行,返回文件名列表(去掉尾部的 (…) 注记)。"""
    for line in reversed(txt.read_text(encoding="utf-8", errors="replace").splitlines()):
        s = line.strip()
        if s.startswith("[files]"):
            body = s[len("[files]"):].strip()
            body = re.sub(r"\s*\([^)]*\)\s*$", "", body)  # 去掉结尾 (rsvg-convert, 3x) 之类
            return [t.strip() for t in body.split("+") if t.strip()]
    return None


def main():
    root = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else Path("skills/figure-forge").resolve()
    out_dir = root / "evals" / "capability" / "outputs"
    txts = sorted(out_dir.glob("*.txt")) if out_dir.exists() else []
    if not txts:
        print(f"⚠ 没有产出可查:{out_dir}(先生成 outputs/<id>.txt 再跑)")
        sys.exit(0)

    all_ok = True
    print(f"── 交付硬检查 (check_delivery) @ {out_dir} ──")
    for txt in txts:
        cid = txt.stem
        files = parse_files_line(txt)
        if files is None:
            print(f"  ❌ {cid}: 缺 [files] 行,无法核验交付")
            all_ok = False
            continue
        case_ok = True
        parts = []
        for name in files:
            ok, why = check_file(out_dir / name)
            case_ok &= ok
            parts.append(f"{name}[{'✅' if ok else '❌'} {why}]")
        all_ok &= case_ok
        print(f"  {'✅' if case_ok else '❌'} {cid}: " + "  ".join(parts))

    print(f"\n→ 交付硬检查:{'全部通过' if all_ok else '有未通过项'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
