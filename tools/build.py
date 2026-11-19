#!/usr/bin/env python3
"""Build the two pages people open from the one source file.

    src/page.html  ->  index.html  (English)
                   ->  ja.html     (Japanese, using i18n/ja.json)

Run from the repo root:  python3 tools/build.py
Edit src/page.html only. index.html and ja.html are rebuilt every time.

i18n/ja.json is a list of [English, Japanese] pairs, applied top to bottom as exact
text replacements. When you change English text in src/page.html, change the English
side of its pair too (or add a new pair), or the Japanese page keeps showing English.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "page.html"
PAIRS = ROOT / "i18n" / "ja.json"

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
"""


def wrap(body: str, lang: str) -> str:
    """Put the page source inside a full HTML document (head ends after the first </style>)."""
    i = body.index("</style>") + len("</style>")
    return HEAD.format(lang=lang) + body[:i] + "\n</head>\n<body>" + body[i:] + "\n</body>\n</html>\n"


def translate(text: str):
    pairs = json.loads(PAIRS.read_text(encoding="utf-8"))
    missing = []
    for en, ja in pairs:
        if en in text:
            text = text.replace(en, ja)
        else:
            missing.append(en)
    return text, len(pairs), missing


def check_js(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    try:
        out = subprocess.run(
            ["node", "-e", "new Function(require('fs').readFileSync(0,'utf8'))"],
            input="\n".join(scripts), text=True, capture_output=True, timeout=30,
        )
    except FileNotFoundError:
        return "skipped (node not installed)"
    return "ok" if out.returncode == 0 else "ERROR\n" + out.stderr.strip()


def main():
    src = SRC.read_text(encoding="utf-8")
    ja, n, missing = translate(src)
    (ROOT / "index.html").write_text(wrap(src, "en"), encoding="utf-8")
    (ROOT / "ja.html").write_text(wrap(ja, "ja"), encoding="utf-8")

    imgs = sorted(set(re.findall(r"img/([\w.-]+?\.jpg)", src)) |
                  {m + ".jpg" for m in re.findall(r"'(gen-[\w-]+|[a-z][\w-]+)'", src)
                   if (ROOT / "img" / (m + ".jpg")).exists()})
    absent = [f for f in imgs if not (ROOT / "img" / f).exists()]

    print(f"Built index.html and ja.html. Japanese pairs: {n}, not matched: {len(missing)}")
    for en in missing:
        print("  not matched:", en[:90].replace("\n", " "))
    if absent:
        print("Missing images in img/:", ", ".join(absent))
    ok = True
    for f in ("index.html", "ja.html"):
        res = check_js(ROOT / f)
        print(f"Script check {f}: {res}")
        ok = ok and not res.startswith("ERROR")
    sys.exit(0 if ok and not absent else 1)


if __name__ == "__main__":
    main()
