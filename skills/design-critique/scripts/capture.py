#!/usr/bin/env python3
"""Resolution-capped screenshot capture for the design-critique skill.

Two modes, both keep image tokens low by capping width (~1000px by default):
  - URL capture (default): screenshot one or more localhost/live URLs via Playwright.
  - Downscale (--downscale): resize image files the user already has.

Usage:
  python capture.py https://localhost:3000 https://localhost:3000/next
  python capture.py --mobile https://localhost:3000
  python capture.py --auth auth.json https://localhost:3000/app
  python capture.py --downscale shot1.png shot2.png

Saved PNG paths are printed one per line so the skill can Read them.
"""
import argparse
import os
import sys

SCRATCH = os.environ.get(
    "CLAUDE_SCRATCHPAD",
    "/private/tmp/claude-501/-Users-designer-teloslabs/scratchpad",
)


def downscale(path, width, out_dir):
    from PIL import Image

    img = Image.open(path)
    if img.width > width:
        height = round(img.height * width / img.width)
        img = img.resize((width, height), Image.LANCZOS)
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(out_dir, f"{base}_capped.png")
    img.convert("RGB").save(out, "PNG")
    return out


def capture_urls(urls, width, mobile, auth, out_dir):
    from playwright.sync_api import sync_playwright

    os.makedirs(out_dir, exist_ok=True)
    viewport = {"width": 390 if mobile else 1280, "height": 844 if mobile else 800}
    saved = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx_args = {"viewport": viewport, "device_scale_factor": 1}
        if auth:
            ctx_args["storage_state"] = auth
        context = browser.new_context(**ctx_args)
        page = context.new_page()
        for i, url in enumerate(urls):
            page.goto(url, wait_until="networkidle", timeout=30000)
            raw = os.path.join(out_dir, f"screen_{i + 1}.png")
            page.screenshot(path=raw)  # viewport only, never full_page
            saved.append(downscale(raw, width, out_dir) if viewport["width"] > width else raw)
        browser.close()
    return saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="URLs to capture, or image paths with --downscale")
    ap.add_argument("--width", type=int, default=1000, help="max width in px (token cap)")
    ap.add_argument("--mobile", action="store_true", help="mobile viewport")
    ap.add_argument("--auth", help="Playwright storage_state JSON for logged-in pages")
    ap.add_argument("--downscale", action="store_true", help="resize image files instead of capturing URLs")
    ap.add_argument("--out", default=os.path.join(SCRATCH, "design-critique"))
    args = ap.parse_args()

    if args.downscale:
        saved = [downscale(p, args.width, args.out) for p in args.targets]
    else:
        saved = capture_urls(args.targets, args.width, args.mobile, args.auth, args.out)

    for path in saved:
        print(path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"capture failed: {exc}", file=sys.stderr)
        sys.exit(1)
