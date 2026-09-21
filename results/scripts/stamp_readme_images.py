#!/usr/bin/env python3
"""Append ?v=<content hash> to every results/figures image link in the README.

GitHub serves README images from a fixed path, so a browser that has cached
an older render keeps showing it after the file changes. Tying the link to
the image's content makes the URL change exactly when the image does.
"""

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
LINK = re.compile(r"\]\((results/figures/[^)?\s]+\.png)(\?v=[0-9a-f]+)?\)")


def stamp(match):
    path = ROOT / match.group(1)
    if not path.exists():
        return match.group(0)
    digest = hashlib.sha1(path.read_bytes()).hexdigest()[:8]
    return f"]({match.group(1)}?v={digest})"


def main():
    text = README.read_text()
    stamped = LINK.sub(stamp, text)
    if stamped != text:
        README.write_text(stamped)
    print(f"Stamped {len(LINK.findall(stamped))} image links in {README}")


if __name__ == "__main__":
    main()
