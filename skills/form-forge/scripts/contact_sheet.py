#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把一个目录里的图拼成一张总览图，用于**下载后目视验收**。

这一步不是可选的。按词搜维基极易撞车，作者黑名单也拦不干净所有货色：
实测第一轮 40 张里有 3 张是错的（一张视频截图、一张尸体照、一张下颌骨）。
不看一眼就往笔记里塞，错的图会一直躺在那儿。

用法
  python contact_sheet.py <图片目录> [-o 输出.png] [--cols 8] [--cell 170]
"""
import argparse, glob, os, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--cell", type=int, default=170)
    a = ap.parse_args()
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("需要 Pillow：pip install pillow"); return 1

    files = sorted(f for f in glob.glob(os.path.join(a.dir, "*"))
                   if os.path.splitext(f)[1].lower() in (".png", ".jpg", ".jpeg", ".gif"))
    if not files:
        print("目录里没有图"); return 1
    C, S = a.cols, a.cell
    rows = (len(files) + C - 1) // C
    sheet = Image.new("RGB", (C * S, rows * (S + 14)), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f); im.seek(0); im = im.convert("RGB")
        im.thumbnail((S - 10, S - 10))
        x, y = (i % C) * S, (i // C) * (S + 14)
        sheet.paste(im, (x + (S - im.width) // 2, y + (S - im.height) // 2))
        # 标签用文件名去掉前缀，中文字形靠系统默认位图字体可能画不出，
        # 画不出也无妨：核对时按位置对照下面打印的清单即可。
        d.text((x + 5, y + S + 1), os.path.splitext(os.path.basename(f))[0][-14:], fill="black")
    out = a.out or os.path.join(a.dir, "_contact-sheet.png")
    sheet.save(out)
    print("拼图：%s  (%dx%d, %d 张)" % (out, sheet.width, sheet.height, len(files)))
    for i, f in enumerate(files):
        print("%3d %s" % (i + 1, os.path.basename(f)))
    print("\n逐格看一遍。发现视频截图、尸体照、明显对不上的部位，就用")
    print("fetch_muscle_images.py --search 换个拼法重取，并回 assets/muscles.tsv 更正。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
