"""NOTE: This project contains AI-generated code."""

import re
from pathlib import Path
from typing import Tuple
from urllib.parse import unquote

BASE_URL = "https://cdn.jsdelivr.net/gh/gky0329/tong-image-repo@main/"
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def is_within_comment(line: str, start: int, end: int) -> bool:
    open_idx = line.rfind("<!--", 0, start)
    close_idx = line.find("-->", end)
    return open_idx != -1 and close_idx != -1


def split_rel_path(url: str) -> Tuple[str, str] | None:
    if not url.startswith(BASE_URL):
        return None
    rel = unquote(url[len(BASE_URL):]).lstrip("/")
    if "/" not in rel:
        return None
    slug, filename = rel.split("/", 1)
    return slug, filename


def process_line(line: str, assets_dir: Path) -> str:
    def replacer(match: re.Match) -> str:
        if is_within_comment(line, match.start(), match.end()):
            return match.group(0)
        url = match.group(1)
        rel = split_rel_path(url)
        if not rel:
            return match.group(0)
        slug, filename = rel
        sure_path = assets_dir / slug / "sure" / filename
        if not sure_path.exists():
            return match.group(0)
        return f"<!-- {match.group(0)} -->"

    return IMAGE_PATTERN.sub(replacer, line)


def process_file(md_path: Path, assets_dir: Path) -> bool:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    updated_lines = [process_line(line, assets_dir) for line in lines]
    updated = "\n".join(updated_lines) + ("\n" if text.endswith("\n") else "")
    if updated != text:
        md_path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    assets_dir = Path("news images")
    md_dir = Path("newmd")
    changed = 0
    for md_path in md_dir.glob("*.md"):
        if process_file(md_path, assets_dir):
            changed += 1
    print(f"Updated {changed} files.")


if __name__ == "__main__":
    main()
