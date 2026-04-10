#!/usr/bin/env node
/**
 * html-to-pdf.js — Render MathJax HTML to PDF using Chromium headless
 * 
 * Usage: node html-to-pdf.js <input.html> <output.pdf>
 * 
 * Waits for MathJax to finish rendering all math before printing.
 */

const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

function resolveChromiumPath() {
  // Honor explicit env var overrides first (set by CI or build-pdf.sh)
  const envVars = ['PUPPETEER_EXECUTABLE_PATH', 'CHROME_PATH', 'CHROMIUM_PATH'];
  for (const v of envVars) {
    if (process.env[v]) return process.env[v];
  }
  // Fall back to common names on PATH
  const { execFileSync } = require('child_process');
  for (const name of ['chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable']) {
    try {
      const p = execFileSync('which', [name], { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
      if (p) return p;
    } catch (_) { /* not found */ }
  }
  throw new Error(
    'Chromium/Chrome executable not found. Install Chromium or set PUPPETEER_EXECUTABLE_PATH, ' +
    'CHROME_PATH, or CHROMIUM_PATH to the browser binary.'
  );
}

async function htmlToPdf(inputHtml, outputPdf) {
  const absoluteInput = path.resolve(inputHtml);
  
  if (!fs.existsSync(absoluteInput)) {
    console.error(`Error: Input file not found: ${absoluteInput}`);
    process.exit(1);
  }

  console.log(`Input:  ${absoluteInput}`);
  console.log(`Output: ${outputPdf}`);
  
  const chromiumPath = resolveChromiumPath();
  console.log(`Chromium: ${chromiumPath}`);
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--font-render-hinting=none',
    ],
    executablePath: chromiumPath
  });

  const page = await browser.newPage();
  
  // Set a large viewport for proper rendering
  await page.setViewport({ width: 1200, height: 800 });

  // Navigate to the HTML file
  const fileUrl = `file://${absoluteInput}`;
  console.log('Loading HTML...');
  await page.goto(fileUrl, { 
    waitUntil: 'networkidle0',
    timeout: 120000  // 2 minutes for large files
  });

  // Wait for MathJax to finish rendering
  console.log('Waiting for MathJax to render all equations...');
  try {
    await page.waitForFunction(
      () => document.body.getAttribute('data-mathjax-done') === 'true',
      { timeout: 300000 }  // 5 minutes for MathJax on a large document
    );
    console.log('MathJax rendering complete.');
  } catch (e) {
    console.warn('MathJax timeout - proceeding with current state. Some equations may not be rendered.');
  }

  // Additional wait for SVG rendering to settle
  await new Promise(resolve => setTimeout(resolve, 5000));

  // Generate PDF
  console.log('Generating PDF...');
  await page.pdf({
    path: outputPdf,
    format: 'Letter',
    margin: {
      top: '0.75in',
      right: '0.75in',
      bottom: '0.75in',
      left: '0.75in'
    },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size: 9px; color: #999; text-align: center; width: 100%;"><span class="pageNumber"></span></div>',
    preferCSSPageSize: false,
    timeout: 300000  // 5 minutes for PDF generation
  });

  console.log(`PDF generated successfully: ${outputPdf}`);
  
  await browser.close();
}

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 2) {
  console.log('Usage: node html-to-pdf.js <input.html> <output.pdf>');
  process.exit(1);
}

htmlToPdf(args[0], args[1]).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
