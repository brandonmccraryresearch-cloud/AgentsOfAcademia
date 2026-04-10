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
PREPROCESSED="/tmp/${BASENAME}_preprocessed.md"

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

if [ ! -f "$SCRIPT_DIR/node_modules/puppeteer-core/package.json" ] 2>/dev/null; then
  echo "[Step 0] Installing puppeteer..."
  cd "$SCRIPT_DIR"
  npm init -y --silent 2>/dev/null || true
  npm install puppeteer-core 2>&1 | tail -3
  cd "$REPO_DIR"
fi

echo "[Step 0] Dependencies OK."

# --- Step 1: Preprocess markdown ---
echo ""
echo "[Step 1] Preprocessing markdown..."

# The manuscript uses standard markdown with $...$ for inline math and $$...$$ 
# for display math. We need to handle a few edge cases:
# 1. Pipe characters inside table cells that contain math
# 2. Emoji characters (✅, ⚠️, 🔶) that may not render in all fonts
# 3. Ensure blank lines around display math blocks

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

# Cleanup
rm -f "$PREPROCESSED"

echo ""
echo "Done."
