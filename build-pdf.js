// Render policy-brief.html to a real multi-page PDF using puppeteer.
// Run: node build-pdf.js

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  });
  const page = await browser.newPage();

  const htmlPath = path.resolve(__dirname, 'policy-brief.html');
  const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');

  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 90000 });

  // Wait for web fonts to load before rendering
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) {
      await document.fonts.ready;
    }
  });

  // Tag each Part section so puppeteer's running header can pick up the current Part
  await page.evaluate(() => {
    const headings = document.querySelectorAll('main h1, main h2');
    let currentPart = '';
    headings.forEach((h) => {
      const text = h.textContent.replace(/¶$/, '').trim();
      if (/^Part [IVX]+/.test(text) || /^Appendix [A-G]/.test(text) || /^At a glance/i.test(text) || /^A note from/i.test(text)) {
        currentPart = text;
      }
      h.setAttribute('data-running-head', currentPart);
    });
  });

  await page.pdf({
    path: path.resolve(__dirname, 'policy-brief.pdf'),
    format: 'Letter',
    margin: { top: '0.85in', right: '0.7in', bottom: '0.95in', left: '0.7in' },
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="font-family: 'Inter', sans-serif; font-size: 8pt; color: #6b1f1f; width: 100%; padding: 0 0.7in; margin-top: 0.35in; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 500; display: flex; justify-content: space-between;">
        <span>What Accountable Government Looks Like</span>
        <span></span>
      </div>`,
    footerTemplate: `
      <div style="font-family: 'Inter', sans-serif; font-size: 8pt; color: #4a4a4a; width: 100%; padding: 0 0.7in; margin-bottom: 0.35in; display: flex; justify-content: space-between; align-items: center;">
        <span style="letter-spacing: 0.06em;">Drafted &middot; Alberta &middot; CC BY-SA 4.0</span>
        <span style="font-feature-settings: 'tnum';"><span class="pageNumber"></span></span>
      </div>`,
  });

  await browser.close();
  const stats = fs.statSync(path.resolve(__dirname, 'policy-brief.pdf'));
  console.log(`PDF written: ${stats.size} bytes`);
})();
