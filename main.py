#!/usr/bin/env python3
"""The World Today — 26 November 2026 in one image.

Entry for make.fun news-image-20261126: "Sum up 26 November's world news
in one image" (program/v1).

The image itself is pre-rendered at build time by render.py (Pillow) from
the real headlines of 26 November 2026 and committed as entry.png, because
this grader runs bare python3.13 with no network, a read-only repo, no
Pillow, and only /output writable. This script is stdlib-only: it verifies
entry.png is a well-formed PNG of the expected size and copies it, byte
for byte, into the output folder. It never touches the network, never
writes outside the output folder, and never removes the output folder
itself (the grader mounts it).

Run:  python3 main.py   (writes /output/entry.png, or ./output/entry.png
if /output is not mounted, or $OUTPUT_DIR when set)
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
EXPECTED_WIDTH = 1200
EXPECTED_HEIGHT = 1600
EXPECTED_MIN_BYTES = 50_000

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def read_png_header(path):
    """Return (width, height) after checking the PNG signature and IHDR."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file (bad signature)")
    length, chunk = struct.unpack(">I4s", head[8:16])
    if chunk != b"IHDR" or length != 13:
        raise ValueError("not a PNG file (missing IHDR)")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def output_dir():
    """The grader mounts /output; fall back to ./output, then $OUTPUT_DIR."""
    override = os.environ.get("OUTPUT_DIR")
    if override:
        return override
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(HERE, "output")


def clean_output_contents(path):
    """Remove only the *contents* of the output folder, never the folder."""
    os.makedirs(path, exist_ok=True)
    for name in os.listdir(path):
        target = os.path.join(path, name)
        if os.path.isdir(target) and not os.path.islink(target):
            shutil.rmtree(target)
        else:
            os.remove(target)


def main():
    if not os.path.isfile(SOURCE):
        return fail("entry.png missing next to main.py")
    try:
        width, height = read_png_header(SOURCE)
    except (OSError, ValueError) as exc:
        return fail("entry.png failed validation: %s" % exc)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return fail("entry.png is %dx%d, expected %dx%d"
                    % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT))
    size = os.path.getsize(SOURCE)
    if size < EXPECTED_MIN_BYTES:
        return fail("entry.png is only %d bytes, expected a full render"
                    % size)

    out = output_dir()
    clean_output_contents(out)
    dest = os.path.join(out, "entry.png")
    shutil.copyfile(SOURCE, dest)

    with open(dest, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("entry.png: %dx%d, %d bytes, sha256 %s"
          % (width, height, size, digest))
    print("wrote %s" % dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
