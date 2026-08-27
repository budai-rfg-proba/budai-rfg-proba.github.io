"""Készít egy relatív útvonalakkal ellátott másolatot a dist/ mappából, kizárólag
a deploy_website előnézeti eszközhöz (amely nem a domain gyökerén szolgálja ki a
fájlokat). A GitHub Pages build (dist/) változatlanul abszolút '/'-gyökerű
útvonalakat használ a BASE_PATH környezeti változó miatt -- ez a script csak egy
másolaton dolgozik.
"""
import re
import shutil
from pathlib import Path

SRC = Path("/home/user/workspace/rfg-honlap/dist")
DST = Path("/home/user/workspace/rfg-honlap/dist-preview")

ATTR_RE = re.compile(r'(href|src|action)="(/[^"]*)"')


def prefix_for(html_path: Path) -> str:
    depth = len(html_path.relative_to(DST).parent.parts)
    return "../" * depth if depth > 0 else "./"


def rewrite_path(prefix: str, value: str) -> str:
    if value.startswith("//") or "://" in value:
        return value
    if value == "/":
        return prefix
    return prefix + value[1:]


def fix_html(html_path: Path) -> None:
    prefix = prefix_for(html_path)
    text = html_path.read_text(encoding="utf-8")

    def attr_sub(m: re.Match) -> str:
        attr, value = m.group(1), m.group(2)
        return f'{attr}="{rewrite_path(prefix, value)}"'

    text = ATTR_RE.sub(attr_sub, text)
    # A /kereses/ oldal kliensoldali szkriptjében lévő base konstans javítása.
    text = text.replace('const base = "/";', f'const base = "{prefix}";')
    html_path.write_text(text, encoding="utf-8")


def main() -> None:
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
    for html_path in DST.rglob("*.html"):
        fix_html(html_path)
    print(f"Kész: {sum(1 for _ in DST.rglob('*.html'))} HTML fájl javítva.")


if __name__ == "__main__":
    main()
