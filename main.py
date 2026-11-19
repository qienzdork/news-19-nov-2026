#!/usr/bin/env python3
"""Entry point for the 19 November 2026 front page.

The front page is drawn by draw_frontpage.py (Pillow, run at build time)
and shipped as entry.png beside this file. This program is stdlib-only:
it copies that image, byte for byte, to the output directory the grader
provides, so the two grader runs write identical bytes. No network,
no randomness, no dependencies beyond the standard library.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SRC.is_file():
        print("entry.png missing beside main.py", file=sys.stderr)
        raise SystemExit(1)
    size = SRC.stat().st_size
    if size > 1048576:
        print(f"entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        raise SystemExit(1)
    shutil.copyfile(SRC, out_dir / "entry.png")
    print("wrote", out_dir / "entry.png", SRC.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
