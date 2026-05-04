"""NOTE: This project contains AI-generated code."""

import argparse
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import quote, urlparse, parse_qs

import requests
from pypinyin import Style, pinyin


def to_pinyin(text: str) -> str:
    result: List[str] = []
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff":
            py = pinyin(ch, style=Style.NORMAL, errors="ignore")
            if py and py[0]:
                result.append(py[0][0])
            else:
                result.append("_")
        else:
            result.append(ch)
    return "".join(result)


def slugify_filename(name: str) -> str:
    text = to_pinyin(name)
    out = []
    for ch in text:
        if ch.isalnum():
            out.append(ch)
        elif ch in {" ", "\t"}:
            out.append("_")
        else:
            out.append("_")
    slug = "".join(out)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "untitled"


def strip_css_from_first_line(lines: List[str]) -> List[str]:
    if not lines:
        return lines
    match = re.search(r"\s\\?\*\s*\{", lines[0])
    if match:
        lines[0] = lines[0][: match.start()].rstrip()
    return lines


def remove_garbage_lines(lines: List[str]) -> List[str]:
    cleaned: List[str] = []
    for line in lines:
        if "data:image/svg+xml" in line:
            continue
        if "阅读" in line and ("赞" in line or "分享" in line or "推荐" in line or "留言" in line):
            continue
        cleaned.append(line)
    return cleaned


def normalize_title_line(lines: List[str]) -> List[str]:
    first_idx = None
    first_text = ""
    second_text = ""
    for idx, line in enumerate(lines):
        if line.strip():
            if first_idx is None:
                first_idx = idx
                first_text = line.strip()
                lines[idx] = first_text
            else:
                second_text = line.strip()
                break
    if first_idx == 0 and first_text and first_text == second_text:
        lines[first_idx] = ""
    return lines


def trim_edge_blank_lines(lines: List[str]) -> List[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def find_title(lines: List[str]) -> str:
    for line in lines:
        if line.strip():
            return line.strip()
    return "untitled"


def extract_extension(url: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if "wx_fmt" in qs and qs["wx_fmt"]:
        return qs["wx_fmt"][0].lower()
    path = parsed.path.lower()
    for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        if path.endswith(ext):
            return ext.lstrip(".")
    return "png"


def download_image(
    url: str,
    output_path: Path,
    proxies: Dict[str, str],
    sleep_ms: int,
    max_retries: int,
    timeout_sec: int,
) -> bool:
    if output_path.exists():
        return True
    last_error: Exception | None = None
    for _ in range(max_retries):
        try:
            resp = requests.get(url, timeout=timeout_sec, proxies=proxies)
            resp.raise_for_status()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(resp.content)
            time.sleep(sleep_ms / 1000.0)
            return True
        except Exception as exc:
            last_error = exc
            time.sleep(1.0)
    print(f"WARN: failed to download {url}: {last_error}", file=sys.stderr)
    return False


def build_cdn_url(repo: str, asset_path: Path) -> str:
    # jsdelivr uses URL paths with spaces encoded
    encoded_path = "/".join(quote(part) for part in asset_path.parts)
    return f"https://cdn.jsdelivr.net/gh/{repo}@main/{encoded_path}"


def process_markdown(
    text: str,
    file_slug: str,
    assets_dir: Path,
    repo: str,
    proxies: Dict[str, str],
    filename_mode: str,
    image_sleep_ms: int,
    max_retries: int,
    timeout_sec: int,
    image_proxies: Dict[str, str],
) -> Tuple[str, List[Path]]:
    image_index = 1
    downloaded: List[Path] = []

    def replace_image(match: re.Match) -> str:
        nonlocal image_index
        url = match.group(1)
        if "mmbiz.qpic.cn" not in url:
            return match.group(0)

        ext = extract_extension(url)

        if filename_mode == "title-index":
            filename = f"{image_index:03d}.{ext}"
        else:
            filename = f"{image_index:03d}.{ext}"

        image_index += 1

        output_path = assets_dir / file_slug / filename
        if not download_image(url, output_path, image_proxies, image_sleep_ms, max_retries, timeout_sec):
            return match.group(0)
        downloaded.append(output_path)

        cdn_url = build_cdn_url(repo, output_path.relative_to(assets_dir))
        return f"![]({cdn_url})"

    lines = text.splitlines()
    lines = strip_css_from_first_line(lines)
    lines = remove_garbage_lines(lines)
    lines = normalize_title_line(lines)

    updated_lines: List[str] = []
    image_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    for line in lines:
        line_stripped = line.strip()
        images = list(image_pattern.finditer(line))
        if not images:
            updated_lines.append(line)
            continue

        if line_stripped and all(
            line_stripped == m.group(0) for m in images
        ):
            updated_lines.append(image_pattern.sub(replace_image, line))
        else:
            # Keep inline text, drop inline images
            new_line = image_pattern.sub("", line).strip()
            if new_line:
                while len(updated_lines) >= 2 and (not updated_lines[-1].strip()) and (not updated_lines[-2].strip()):
                    updated_lines.pop()
                updated_lines.append(new_line)

    updated_lines = trim_edge_blank_lines(updated_lines)
    return "\n".join(updated_lines) + "\n", downloaded


def process_file(
    input_path: Path,
    output_path: Path,
    assets_dir: Path,
    repo: str,
    proxies: Dict[str, str],
    filename_mode: str,
    image_sleep_ms: int,
    max_retries: int,
    timeout_sec: int,
    image_proxies: Dict[str, str],
) -> None:
    text = input_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    lines = strip_css_from_first_line(lines)
    lines = remove_garbage_lines(lines)
    lines = normalize_title_line(lines)
    file_slug = slugify_filename(input_path.stem)

    processed_text, _ = process_markdown(
        text=text,
        file_slug=file_slug,
        assets_dir=assets_dir,
        repo=repo,
        proxies=proxies,
        filename_mode=filename_mode,
        image_sleep_ms=image_sleep_ms,
        max_retries=max_retries,
        timeout_sec=timeout_sec,
        image_proxies=image_proxies,
    )
    output_path.write_text(processed_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Process markdown files and rewrite image links.")
    parser.add_argument("--input", help="Input markdown file")
    parser.add_argument("--input-dir", help="Process all markdown files in a directory")
    parser.add_argument("--assets-dir", default="news images", help="Assets output directory")
    parser.add_argument("--cdn-repo", default="gky0329/tong-image-repo", help="GitHub repo for jsdelivr")
    parser.add_argument("--filename-mode", default="title-index", choices=["title-index"], help="Image filename mode")
    parser.add_argument("--proxy", default="http://127.0.0.1:7890", help="HTTP proxy URL")
    parser.add_argument("--no-proxy", action="store_true", help="Disable proxy for downloads")
    parser.add_argument("--image-sleep-ms", type=int, default=1000, help="Sleep after each image download")
    parser.add_argument("--file-sleep-ms", type=int, default=5000, help="Sleep between files")
    parser.add_argument("--download-retries", type=int, default=3, help="Max retries per image")
    parser.add_argument("--download-timeout-sec", type=int, default=30, help="Timeout per image download")
    args = parser.parse_args()

    if not args.input and not args.input_dir:
        parser.error("--input or --input-dir is required")

    if args.no_proxy:
        proxies = {}
    else:
        proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else {}
    image_proxies: Dict[str, str] = {}
    assets_dir = Path(args.assets_dir)

    if args.input:
        input_path = Path(args.input)
        output_dir = Path("newmd")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{input_path.stem}_after{input_path.suffix}"
        if output_path.exists():
            print(f"SKIP: {output_path} already exists")
            return 0
        process_file(
            input_path,
            output_path,
            assets_dir,
            args.cdn_repo,
            proxies,
            args.filename_mode,
            args.image_sleep_ms,
            args.download_retries,
            args.download_timeout_sec,
            image_proxies,
        )
        return 0

    input_dir = Path(args.input_dir)
    for md_file in input_dir.glob("*.md"):
        output_dir = Path("newmd")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{md_file.stem}_after{md_file.suffix}"
        if output_path.exists():
            print(f"SKIP: {output_path} already exists")
            continue
        process_file(
            md_file,
            output_path,
            assets_dir,
            args.cdn_repo,
            proxies,
            args.filename_mode,
            args.image_sleep_ms,
            args.download_retries,
            args.download_timeout_sec,
            image_proxies,
        )
        time.sleep(args.file_sleep_ms / 1000.0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
