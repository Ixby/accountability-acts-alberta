// Render policy-brief.html to a real multi-page PDF using puppeteer.
// Two-pass render: page 1 (cover) gets no running header/footer; pages 2+ do.
// Run: node build-pdf.js

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');

const HEADER_BODY = `
  <div style="font-family: 'Inter', sans-serif; font-size: 8pt; color: #6b1f1f; width: 100%; padding: 0 0.7in; margin-top: 0.35in; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 500; display: flex; justify-content: space-between;">
    <span>What Accountable Government Looks Like</span>
    <span></span>
  </div>`;
const FOOTER_BODY = `
  <div style="font-family: 'Inter', sans-serif; font-size: 8pt; color: #4a4a4a; width: 100%; padding: 0 0.7in; margin-bottom: 0.35in; display: flex; justify-content: space-between; align-items: center;">
    <span style="letter-spacing: 0.06em;">Drafted &middot; Alberta &middot; CC BY-SA 4.0</span>
    <span style="font-feature-settings: 'tnum';"><span class="pageNumber"></span></span>
  </div>`;
const EMPTY = `<span style="display:none"></span>`;

async function renderPdf({ pageRanges, headerTemplate, footerTemplate }) {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  });
  const page = await browser.newPage();

  const htmlPath = path.resolve(__dirname, 'policy-brief.html');
  const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');

  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 90000 });
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) {
      await document.fonts.ready;
    }
  });

  const buf = await page.pdf({
    format: 'Letter',
    margin: { top: '0.85in', right: '0.7in', bottom: '0.95in', left: '0.7in' },
    printBackground: true,
    preferCSSPageSize: true,
    pageRanges,
    displayHeaderFooter: true,
    headerTemplate,
    footerTemplate,
  });

  await browser.close();
  return buf;
}

(async () => {
  // Pass 1: cover only, no chrome
  const coverBuf = await renderPdf({
    pageRanges: '1',
    headerTemplate: EMPTY,
    footerTemplate: EMPTY,
  });
  // Pass 2: pages 2 onward, with running header & footer
  const bodyBuf = await renderPdf({
    pageRanges: '2-',
    headerTemplate: HEADER_BODY,
    footerTemplate: FOOTER_BODY,
  });

  // Merge with pdf-lib
  const cover = await PDFDocument.load(coverBuf);
  const body = await PDFDocument.load(bodyBuf);
  const out = await PDFDocument.create();
  const coverPages = await out.copyPages(cover, cover.getPageIndices());
  coverPages.forEach((p) => out.addPage(p));
  const bodyPages = await out.copyPages(body, body.getPageIndices());
  bodyPages.forEach((p) => out.addPage(p));

  const merged = await out.save();
  const outPath = path.resolve(__dirname, 'policy-brief.pdf');
  fs.writeFileSync(outPath, merged);
  const stats = fs.statSync(outPath);
  console.log(`PDF written: ${stats.size} bytes (${out.getPageCount()} pages)`);
})();
