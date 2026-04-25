// Render policy-brief.html to a real multi-page PDF using puppeteer.
// Run: node build-pdf.js

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();

  const htmlPath = path.resolve(__dirname, 'policy-brief.html');
  const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');

  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });

  // Inject print-friendly overrides
  await page.addStyleTag({
    content: `
      @page { size: Letter; margin: 0.85in 0.7in 0.95in 0.7in; }
      @media print {
        body { font-size: 11pt; line-height: 1.55; max-width: none !important; }
        main { max-width: none !important; padding: 0 !important; }
        h1 { page-break-before: always; padding-top: 0.5em; }
        h1:first-of-type { page-break-before: avoid; }
        h2, h3, h4 { page-break-after: avoid; }
        blockquote, table, pre { page-break-inside: avoid; }
        .site-header, .site-footer, .heading-anchor, .toc { display: none !important; }
        a { color: #1f4068; text-decoration: none; }
      }
    `,
  });

  await page.pdf({
    path: path.resolve(__dirname, 'policy-brief.pdf'),
    format: 'Letter',
    margin: { top: '0.85in', right: '0.7in', bottom: '0.95in', left: '0.7in' },
    printBackground: false,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      '<div style="font-size:9pt; color:#777; width:100%; text-align:center; padding-bottom:6px;">' +
      '<span class="pageNumber"></span> &middot; What Accountable Government Looks Like</div>',
  });

  await browser.close();
  const stats = fs.statSync(path.resolve(__dirname, 'policy-brief.pdf'));
  console.log(`PDF written: ${stats.size} bytes`);
})();
