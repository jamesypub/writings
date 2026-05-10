#!/usr/bin/env python3
"""
publish.py -- copy the latest version of an allowlisted internal blog into
this public writings repo. Nothing outside the allowlist is ever touched.

Usage:
  python scripts/publish.py            # dry-run
  python scripts/publish.py --apply    # copy files + stage changes

Guarantees:
  - Only source folders listed in ALLOWLIST are read.
  - Only the latest blog-source--V{N}.md is published (older drafts ignored).
  - Only images the markdown actually references are copied.
  - Only .md + .png/.jpg/.jpeg/.svg are permitted. Anything else aborts.
  - Image paths must resolve inside the allowlisted source folder.
"""

import re
import shutil
import sys
from pathlib import Path

HOME = Path.home()
REPO_ROOT = Path(__file__).resolve().parent.parent

# THE ALLOWLIST -- single source of truth for what may be published.
ALLOWLIST = [
    {
        "source_dir": HOME / "jycode/blog-agent-orchestration-architecture",
        "post_dir":   REPO_ROOT / "posts/agent-orchestration-patterns",
        "title":      "Building multi-agent applications: orchestration patterns",
    },
]

ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".svg"}
VERSION_RE = re.compile(r"blog-source--V(\d+)\.md$")
IMAGE_REF_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def find_latest_source(output_dir: Path) -> Path:
    if not output_dir.is_dir():
        die(f"Missing Output/ folder: {output_dir}")
    candidates = []
    for p in output_dir.glob("blog-source--V*.md"):
        m = VERSION_RE.search(p.name)
        if m:
            candidates.append((int(m.group(1)), p))
    if not candidates:
        die(f"No blog-source--V*.md found in {output_dir}")
    candidates.sort()
    return candidates[-1][1]


def resolve_images(md_text: str, md_path: Path, source_root: Path):
    resolved = []
    for m in IMAGE_REF_RE.finditer(md_text):
        ref = m.group(1).split(" ", 1)[0]  # strip optional "title"
        if ref.startswith(("http://", "https://")):
            continue
        img_path = (md_path.parent / ref).resolve()
        try:
            img_path.relative_to(source_root.resolve())
        except ValueError:
            die(f"Image escapes allowlisted folder: {ref} -> {img_path}")
        if img_path.suffix.lower() not in ALLOWED_IMAGE_EXTS:
            die(f"Disallowed file type: {img_path}")
        if not img_path.is_file():
            die(f"Missing image: {img_path}")
        resolved.append((ref, img_path))
    return resolved


def publish_one(entry: dict, apply: bool) -> None:
    source_dir = entry["source_dir"]
    post_dir = entry["post_dir"]
    if not source_dir.is_dir():
        die(f"Allowlisted source folder missing: {source_dir}")

    latest_md = find_latest_source(source_dir / "Output")
    print(f"[{source_dir.name}] publishing {latest_md.name}")

    md_text = latest_md.read_text(encoding="utf-8")
    images = resolve_images(md_text, latest_md, source_dir)

    new_text = md_text
    for ref, img_path in images:
        new_text = new_text.replace(f"]({ref})", f"](images/{img_path.name})")

    images_dir = post_dir / "images"
    post_readme = post_dir / "README.md"

    print(f"  -> {post_readme.relative_to(REPO_ROOT)}")
    for _, img in images:
        print(f"  -> posts/{post_dir.name}/images/{img.name}")

    if not apply:
        print("\n(dry-run -- nothing copied; rerun with --apply)")
        return

    post_dir.mkdir(parents=True, exist_ok=True)
    if images_dir.exists():
        for old in images_dir.iterdir():
            if old.is_file():
                old.unlink()
    images_dir.mkdir(exist_ok=True)

    post_readme.write_text(new_text, encoding="utf-8")
    for _, img in images:
        shutil.copy2(img, images_dir / img.name)

    print("Done. Review `git status`, then commit + push.")


def main() -> None:
    apply = "--apply" in sys.argv
    for entry in ALLOWLIST:
        publish_one(entry, apply=apply)


if __name__ == "__main__":
    main()
