#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从维基共享资源 (Wikimedia Commons) 抓版权干净的肌肉解剖图。

用法
  # 从已验证索引批量取（推荐，最快最稳）
  python fetch_muscle_images.py --out <图片目录> --from-index

  # 只取几块
  python fetch_muscle_images.py --out <目录> --muscles 前锯肌 臀中肌

  # 索引里没有的肌肉，现搜（会打印候选供人工挑）
  python fetch_muscle_images.py --out <目录> --search "Popliteus" --cn 腘肌

  # 只列候选不下载
  python fetch_muscle_images.py --search "Pectineus" --cn 耻骨肌 --dry-run

设计要点见 references/image-pipeline.md。核心避坑规则都编在下面的常量里。
"""
import argparse, html, io, json, os, re, sys, time, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "form-forge/1.0 (personal training-notes vault; Wikimedia Commons API client)"
INDEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "muscles.tsv")

# 作者黑名单：图本身合法，但不适合放进健身笔记
BAD_AUTHORS = (
    "anatomist90",      # 全是尸体解剖照片
    "drjanaofficial",   # 不少是视频截图，糊
)
# 标题黑名单：搜索按词匹配极易撞车（external oblique → 下颌骨的 external oblique line）
BAD_TITLE = (
    "mandible", "skull", "capitis", "cervicis", "oculi", "oris", "nasi", "labii",
    "tongue", "pharyn", "larynx", "cadaver", "dissection", "histolog", "micrograph",
    "stain", "ultrasound", "mri", "x-ray", "short head", "long head", "logo", "icon",
)
# 拉丁拼法变体：维基收录的拼法常与教科书不同。一次搜空绝不等于没有。
SPELLING_HINTS = {
    "vastus intermedius": ["Vastus intermedialis"],
    "sternocleidomastoid": ["Sternocleidomastoideus", "Musculus sternocleidomastoideus"],
    "external oblique": ["Abdominal external oblique", "Obliquus externus abdominis"],
    "internal oblique": ["Abdominal internal oblique", "Obliquus internus abdominis"],
    "erector spinae": ["Iliocostalis", "Longissimus", "Spinalis"],
}


def api(params, tries=3):
    params = dict(params); params["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(params)
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return json.load(urllib.request.urlopen(req, timeout=45))
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(1.5 * (k + 1))


def strip_html(s):
    return re.sub("<[^>]+>", "", html.unescape(s or "")).strip()


def meta_for(titles):
    """批量取 imageinfo，返回 [(title, url, mime, width, size, author, license)]"""
    out = []
    for i in range(0, len(titles), 25):
        try:
            pages = api({"action": "query", "prop": "imageinfo",
                         "iiprop": "url|extmetadata|mime|size|dimensions",
                         "titles": "|".join(titles[i:i + 25])})["query"]["pages"]
        except Exception:
            continue
        for _, v in pages.items():
            ii = (v.get("imageinfo") or [None])[0]
            if not ii or ii.get("mime") not in ("image/png", "image/jpeg", "image/gif"):
                continue
            m = ii.get("extmetadata", {})
            out.append((v["title"].replace("File:", ""), ii["url"].split("?")[0],
                        ii.get("mime"), ii.get("width"), ii.get("size"),
                        strip_html(m.get("Artist", {}).get("value")),
                        strip_html(m.get("LicenseShortName", {}).get("value"))))
    return out


def search_candidates(en):
    """多轮查询 + 严格校验。返回按评分排序的候选。"""
    queries = ['intitle:"%s"' % en, "%s muscle Anatomography" % en, "%s muscle anatomy" % en]
    for alt in SPELLING_HINTS.get(en.lower(), []):
        queries.insert(1, 'intitle:"%s"' % alt)
    seen = {}
    for q in queries:
        try:
            res = api({"action": "query", "list": "search", "srsearch": q,
                       "srnamespace": 6, "srlimit": 40})["query"]["search"]
        except Exception:
            continue
        for c in meta_for([r["title"] for r in res]):
            seen[c[0]] = c
        time.sleep(0.2)
        if len(seen) >= 8:
            break

    words = [w.lower() for w in en.split()]
    alts = [a.lower() for a in SPELLING_HINTS.get(en.lower(), [])]
    scored = []
    for title, url, mime, w, size, author, lic in seen.values():
        t = title.lower()
        if not lic:                                    # 授权读不出来的一律不要
            continue
        if any(b in (author or "").lower() for b in BAD_AUTHORS):
            continue
        if any(b in t for b in BAD_TITLE):
            continue
        # 严格校验：标题必须含完整目标词组（或某个已知拼法变体）
        if not (all(x in t for x in words) or any(a.split()[0] in t for a in alts)):
            continue
        s = 0
        s += 60 if mime == "image/png" else (10 if mime == "image/gif" else 0)
        if "anatomography" in (author or "").lower():
            s += 45
        if re.search(r"(lateral|anterior|posterior|top|front|superior)", t):
            s += 12
        if w and 600 <= w <= 2600:
            s += 15
        if "small" in t:
            s -= 15
        scored.append((s, title, url, mime, w, size, author, lic))
    scored.sort(reverse=True)
    return scored


def download(src_title, dest, mime, thumb_width=700):
    """PNG/JPG 取 thumbnail 省体积；GIF 取原图保住动画，之后再降采样。"""
    url = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
           + urllib.parse.quote(src_title)
           + ("" if mime == "image/gif" else "?width=%d" % thumb_width))
    data = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120).read()
    if data[:6] not in (b"GIF87a", b"GIF89a") and data[:4] != b"\x89PNG" and data[:2] != b"\xff\xd8":
        raise RuntimeError("拿到的不是图片，多半是重定向或错误页")
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def shrink_gif(path, size=320):
    """动图降采样，体积一般能降七成。没装 Pillow 就跳过。"""
    try:
        from PIL import Image, ImageSequence
    except ImportError:
        return None
    im = Image.open(path)
    if im.width <= size:
        return os.path.getsize(path)
    frames = [f.convert("RGBA").resize((size, size), Image.LANCZOS)
               .convert("P", palette=Image.ADAPTIVE, colors=128)
              for f in ImageSequence.Iterator(im)]
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=im.info.get("duration", 80), loop=0,
                   optimize=True, disposal=2)
    return os.path.getsize(path)


def read_index():
    rows = []
    with io.open(INDEX, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            p = line.split("\t")
            if len(p) >= 7:
                rows.append(dict(zip(["cn", "en", "region", "bucket", "src", "author", "lic"], p)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="图片输出目录")
    ap.add_argument("--from-index", action="store_true", help="按已验证索引批量下载")
    ap.add_argument("--muscles", nargs="*", help="只取索引里的这几块（中文名）")
    ap.add_argument("--search", help="索引里没有时，用英文名现搜")
    ap.add_argument("--cn", help="配合 --search，指定中文名用于命名")
    ap.add_argument("--dry-run", action="store_true", help="只列候选不下载")
    ap.add_argument("--prefix", default="肌肉-", help="文件名前缀，默认 肌肉-")
    a = ap.parse_args()

    if a.search:
        cands = search_candidates(a.search)
        if not cands:
            print("没有候选。换个拼法再试一次，别急着断定维基上没有。")
            print("已知会变形的拼法见脚本里的 SPELLING_HINTS。")
            return 1
        print("候选（评分高的在前，下载前请目视确认）：")
        for s, t, u, mime, w, size, au, lic in cands[:8]:
            print("  %3d  %-52s %-4s %5sx %6.0fKB  %-26s %s"
                  % (s, t[:52], (mime or "").split("/")[-1], w, (size or 0) / 1024, (au or "?")[:26], lic))
        if a.dry_run or not a.out:
            return 0
        s, t, u, mime, w, size, au, lic = cands[0]
        cn = a.cn or a.search
        ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif"}[mime]
        os.makedirs(a.out, exist_ok=True)
        dest = os.path.join(a.out, a.prefix + cn + ext)
        n = download(t, dest, mime)
        if ext == ".gif":
            n = shrink_gif(dest) or n
        print("\n下载 %s  <- %s  %dKB" % (os.path.basename(dest), t, n // 1024))
        print("署名请登记：%s | %s | %s" % (t, au or "?", lic))
        return 0

    if not a.out:
        ap.error("--out 是必须的")
    rows = read_index()
    if a.muscles:
        want = set(a.muscles)
        rows = [r for r in rows if r["cn"] in want]
        missing = want - {r["cn"] for r in rows}
        if missing:
            print("索引里没有：%s（用 --search 现搜）" % "、".join(sorted(missing)))
    elif not a.from_index:
        ap.error("要么 --from-index，要么 --muscles，要么 --search")

    os.makedirs(a.out, exist_ok=True)
    ok = fail = 0
    for r in rows:
        ext = os.path.splitext(r["src"])[1].lower()
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif"}.get(ext, "image/png")
        dest = os.path.join(a.out, a.prefix + r["cn"] + (".gif" if mime == "image/gif" else ext))
        if os.path.exists(dest):
            print("跳过 %-14s 已存在" % r["cn"]); ok += 1; continue
        try:
            n = download(r["src"], dest, mime)
            if mime == "image/gif":
                n = shrink_gif(dest) or n
            print("OK   %-14s %-46s %5dKB" % (r["cn"], r["src"][:46], n // 1024)); ok += 1
        except Exception as e:
            print("失败 %-14s %s" % (r["cn"], e)); fail += 1
        time.sleep(0.15)
    print("\n成功 %d，失败 %d。下一步务必跑 contact_sheet.py 目视验收。" % (ok, fail))
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
