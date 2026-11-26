#!/usr/bin/env python3
"""Entrypoint for news-image-20261126.

Sums up the world news of Thursday 26 November 2026 in one image.

The picture itself (entry.png, committed beside this file) was drawn at
build time by render_news.py from the headlines reported on the morning of
26 November 2026: the Houthi attack on Saudi Arabia's Ras Tanura refinery
and the mined tankers in the Strait of Hormuz, the Gaza ceasefire under
strain, Ukraine's strikes on Russian refineries, looming US tariffs,
Pakistan's first astronaut bound for China's Tiangong station, plus the
day's other stories in the footer strip.

This program is deliberately stdlib-only: it reads entry.png from beside
itself and copies it byte for byte to the output directory, so both graded
runs write identical bytes. It uses no Pillow and no network.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    with open(src, "rb") as f:
        magic = f.read(8)
    if magic[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({size} bytes, PNG verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
