#!/usr/bin/env bash
# Capture audit evidence for one or more URLs.
# usage: capture.sh <evidence_dir> <url> [url ...]
set -euo pipefail

DIR="$1"; shift
SESSION="uxaudit"
mkdir -p "$DIR"

pw() { playwright-cli -s="$SESSION" "$@" >/dev/null 2>&1 || true; }

playwright-cli -s="$SESSION" open >/dev/null 2>&1 || true

n=0
for url in "$@"; do
  n=$((n+1))
  echo "capturing $n: $url"
  pw resize 1440 900
  playwright-cli -s="$SESSION" goto "$url" >/dev/null
  sleep 3
  pw screenshot --filename "$DIR/screen-$n-desktop-fold.png"
  pw screenshot --full-page --filename "$DIR/screen-$n-desktop-full.png"
  playwright-cli -s="$SESSION" snapshot > "$DIR/screen-$n-snapshot.txt" 2>&1 || true
  playwright-cli -s="$SESSION" console > "$DIR/screen-$n-console.txt" 2>&1 || true
  pw resize 390 844
  sleep 1
  pw screenshot --filename "$DIR/screen-$n-mobile-fold.png"
  pw screenshot --full-page --filename "$DIR/screen-$n-mobile-full.png"
  echo "$n	$url" >> "$DIR/urls.tsv"
done

playwright-cli -s="$SESSION" close >/dev/null 2>&1 || true
echo "captured $n screen(s) to $DIR"
ls -1 "$DIR"
