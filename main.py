"""Entrypoint for make.fun news-image-20261126 (round 2, full-day image).

Copies the pre-rendered front page (entry.png, committed next to this
file) into the output directory. Standard library only: the grader runs
Python 3.13 with no third-party packages installed, so nothing here
imports Pillow or any other non-stdlib module. The picture itself was
produced at build time by render_news.py; this script just delivers the
finished file, byte for byte, on every run.
"""

import os
import shutil
import sys


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)

    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    dest = os.path.join(out_dir, "entry.png")

    # Best-effort sanity read of the PNG header (signature, dimensions,
    # bit depth), plain bytes only, so no missing third-party module can
    # ever break the run.
    try:
        with open(source, "rb") as fh:
            header = fh.read(33)
        if header[:8] != b"\x89PNG\r\n\x1a\n":
            print("warning: entry.png does not start with a PNG signature",
                  file=sys.stderr)
        else:
            width = int.from_bytes(header[16:20], "big")
            height = int.from_bytes(header[20:24], "big")
            print(f"entry.png is {width}x{height} px")
    except (OSError, ValueError) as exc:
        print(f"warning: could not inspect entry.png: {exc}",
              file=sys.stderr)

    shutil.copyfile(source, dest)
    size = os.path.getsize(dest)
    print(f"copied entry.png -> {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
