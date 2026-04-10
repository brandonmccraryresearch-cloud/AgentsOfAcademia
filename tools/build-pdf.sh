#!/usr/bin/env bash
#
# build-pdf.sh — Convert the IRH manuscript markdown to a professional PDF
#
# Pipeline:
#   1. Preprocess: fix markdown quirks for pandoc compatibility
#   2. Pandoc: markdown → HTML with MathJax
#   3. Puppeteer + Chromium: HTML → PDF with rendered MathJax
#
# Usage: ./tools/build-pdf.sh [input.md] [output.pdf]
#
# Defaults:
#   input:  86.0IRH.md
#   output: 86.0IRH.pdf

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

INPUT="${1:-$REPO_DIR/86.0IRH.md}"
OUTPUT="${2:-$REPO_DIR/86.0IRH.pdf}"
BASENAME="$(basename "$INPUT" .md)"

HTML_OUT="$REPO_DIR/${BASENAME}.html"
TEMPLATE="$SCRIPT_DIR/template.html"
PREPROCESSED="$(mktemp "/tmp/${BASENAME}_preprocessed.XXXXXX.md")"

cleanup_preprocessed() {
  rm -f "$PREPROCESSED"
}
trap cleanup_preprocessed EXIT

echo "================================================================"
echo "  IRH Manuscript PDF Builder"
echo "================================================================"
echo "  Input:    $INPUT"
echo "  Output:   $OUTPUT"
echo "  HTML:     $HTML_OUT"
echo "  Template: $TEMPLATE"
echo "================================================================"

# --- Step 0: Check dependencies ---
echo ""
echo "[Step 0] Checking dependencies..."
for cmd in pandoc node; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ERROR: '$cmd' is not installed."
    exit 1
  fi
done

# Detect Chromium executable — check env vars first, then common names on PATH
CHROMIUM_BIN=""
for browser_var in PUPPETEER_EXECUTABLE_PATH CHROME_PATH CHROMIUM_PATH; do
  browser_path="${!browser_var:-}"
  if [ -n "$browser_path" ]; then
    if [ -x "$browser_path" ]; then
      CHROMIUM_BIN="$browser_path"
      break
    else
      echo "ERROR: '$browser_var' is set to '$browser_path', but that file is not executable."
      exit 1
    fi
  fi
done

if [ -z "$CHROMIUM_BIN" ]; then
  for browser_cmd in chromium chromium-browser google-chrome google-chrome-stable; do
    if command -v "$browser_cmd" &>/dev/null; then
      CHROMIUM_BIN="$(command -v "$browser_cmd")"
      break
    fi
  done
fi

if [ -z "$CHROMIUM_BIN" ]; then
  echo "ERROR: Chromium/Chrome is required for PDF generation but was not found."
  echo "Install Chromium/Google Chrome, or set PUPPETEER_EXECUTABLE_PATH, CHROME_PATH, or CHROMIUM_PATH."
  exit 1
fi
export PUPPETEER_EXECUTABLE_PATH="$CHROMIUM_BIN"
echo "[Step 0] Chromium: $CHROMIUM_BIN"

if [ ! -f "$SCRIPT_DIR/node_modules/puppeteer-core/package.json" ]; then
  echo "[Step 0] Installing puppeteer-core..."
  cd "$SCRIPT_DIR"
  if [ -f "$SCRIPT_DIR/package-lock.json" ]; then
    npm ci
  elif [ -f "$SCRIPT_DIR/package.json" ]; then
    npm install
  else
    npm init -y --silent
    npm install puppeteer-core
  fi
  cd "$REPO_DIR"
fi

echo "[Step 0] Dependencies OK."

# --- Step 1: Preprocess markdown ---
echo ""
echo "[Step 1] Preprocessing markdown..."

# Current preprocessing is intentionally minimal:
# 1. Copy the manuscript to a temporary working file
# 2. Ensure the file ends with a trailing newline for downstream tools
# More advanced markdown normalization should be implemented here only if needed.

cp "$INPUT" "$PREPROCESSED"

# Ensure the file ends with a newline
echo "" >> "$PREPROCESSED"

echo "[Step 1] Preprocessing complete."

# --- Step 2: Convert markdown to HTML ---
echo ""
echo "[Step 2] Converting markdown to HTML with pandoc..."

pandoc "$PREPROCESSED" \
  --from=markdown+tex_math_dollars+pipe_tables+yaml_metadata_block+smart+footnotes+strikeout+superscript+subscript \
  --to=html5 \
  --template="$TEMPLATE" \
  --mathjax \
  --standalone \
  --wrap=none \
  --columns=9999 \
  --metadata title="Intrinsic Resonance Holography" \
  --output="$HTML_OUT"

HTML_SIZE=$(wc -c < "$HTML_OUT")
HTML_LINES=$(wc -l < "$HTML_OUT")
echo "[Step 2] HTML generated: ${HTML_LINES} lines, $(( HTML_SIZE / 1024 )) KB"

# --- Step 3: Convert HTML to PDF ---
echo ""
echo "[Step 3] Rendering MathJax and generating PDF with Chromium..."

cd "$SCRIPT_DIR"
node html-to-pdf.js "$HTML_OUT" "$OUTPUT"

if [ -f "$OUTPUT" ]; then
  PDF_SIZE=$(wc -c < "$OUTPUT")
  PDF_PAGES=$(strings "$OUTPUT" | grep -c "/Type /Page" 2>/dev/null || echo "?")
  echo ""
  echo "================================================================"
  echo "  SUCCESS"
  echo "  PDF:   $OUTPUT"
  echo "  Size:  $(( PDF_SIZE / 1024 )) KB"
  echo "  Pages: ~${PDF_PAGES}"
  echo "================================================================"
else
  echo "ERROR: PDF generation failed."
  exit 1
fi

echo ""
echo "Done."
