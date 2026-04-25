// Build the policy-brief PDF in three stages, then merge.
//
// Stage 1: render the COVER page from the HTML/CSS cover section
//          (no header/footer chrome, full-bleed background colour).
// Stage 2: measure heading positions in the body so the TOC has accurate
//          page numbers, then render a standalone TOC page.
// Stage 3: render the BODY of the brief (Parts I–VII + Appendices), with
//          running header/footer and page numbers starting at 1.
// Stage 4: merge cover + TOC + body via pdf-lib.
//
// Run: node build-pdf.js

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');

const HEADER_BODY = `
  <div style="font-family: 'Inter', sans-serif; font-size: 8pt; color: #003f87; width: 100%; padding: 0 0.7in; margin-top: 0.35in; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 500; display: flex; justify-content: space-between;">
    <span>Honest Alberta</span>
    <span></span>
  </div>`;
const FOOTER_BODY = `
  <div style="font-family: 'Inter', sans-serif; font-size: 8pt; color: #4a4a4a; width: 100%; padding: 0 0.7in; margin-bottom: 0.35in; display: flex; justify-content: space-between; align-items: center;">
    <span style="letter-spacing: 0.06em;">Drafted by Will Conner &middot; CC BY-SA 4.0</span>
    <span style="font-feature-settings: 'tnum';"><span class="pageNumber"></span></span>
  </div>`;

const HTML_PATH = path.resolve(__dirname, 'policy-brief.html');
const FILE_URL = 'file:///' + HTML_PATH.replace(/\\/g, '/');

async function withPage(fn) {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  });
  const page = await browser.newPage();
  await page.goto(FILE_URL, { waitUntil: 'networkidle0', timeout: 90000 });
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
  });
  try {
    return await fn(page);
  } finally {
    await browser.close();
  }
}

// Stage 1 — render the cover.
async function renderCover() {
  return await withPage(async (page) => {
    // Show only the cover; hide everything else
    await page.addStyleTag({
      content: `
        .site-header, .site-footer { display: none !important; }
        .toc, main { display: none !important; }
        .html-cover-shim { display: block !important; }
        .cover { display: flex !important; page-break-after: avoid; }
        @page { size: Letter; margin: 0; }
      `,
    });
    return await page.pdf({
      format: 'Letter',
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: false,
      pageRanges: '1',
    });
  });
}

// Stage 2a — measure where each h1/h2 lands in the body, when rendered alone.
async function measureBodyPositions() {
  return await withPage(async (page) => {
    await page.addStyleTag({
      content: `
        @media screen, print {
          .toc, .html-cover-shim, .cover, .site-header, .site-footer { display: none !important; }
        }
      `,
    });

    // Print page content height: Letter 11in - 0.85in - 0.95in = 9.2in × 96dpi = 883.2 px
    const PAGE_CONTENT_PX = 9.2 * 96;
    return await page.evaluate((PAGE_CONTENT_PX) => {
      const out = [];
      const all = document.querySelectorAll('main h1, main h2');
      all.forEach((el) => {
        const id = el.id;
        if (!id) return;
        const text = el.textContent.replace(/¶$/, '').trim();
        const rect = el.getBoundingClientRect();
        const top = rect.top + window.scrollY;
        const pageNum = Math.floor(top / PAGE_CONTENT_PX) + 1;
        const tag = el.tagName.toLowerCase();
        out.push({ id, tag, text, top, pageNum });
      });
      return out;
    }, PAGE_CONTENT_PX);
  });
}

// Stage 2b — render the TOC page with measured page numbers.
async function renderToc(headings) {
  // Filter to TOC items: top-level Parts (h2 outside appendices) + Appendix h1s.
  const items = [];
  let inAppendix = false;
  for (const h of headings) {
    const lc = h.text.toLowerCase();
    if (lc.startsWith('a note from')) continue;
    if (lc.startsWith('at a glance')) continue;
    if (h.tag === 'h1') {
      if (lc.startsWith('appendix')) {
        items.push({ kind: 'appendix', text: h.text, pageNum: h.pageNum });
        inAppendix = true;
      } else {
        // Document title — skip
        inAppendix = false;
      }
    } else if (h.tag === 'h2' && !inAppendix) {
      items.push({ kind: 'part', text: h.text, pageNum: h.pageNum });
    }
  }

  return await withPage(async (page) => {
    await page.evaluate((items) => {
      // Hide everything
      document.querySelectorAll('.html-cover-shim, .site-header, .site-footer, main').forEach((el) => {
        el.style.display = 'none';
      });
      // Inject TOC page
      const tocPage = document.createElement('div');
      tocPage.className = 'print-toc-page';
      tocPage.innerHTML = `
        <div class="print-toc-eyebrow">Contents</div>
        <ol class="print-toc-list">
          ${items.map((it) => `
            <li class="${it.kind === 'appendix' ? 'toc-appendix-line' : 'toc-part-line'}">
              <span class="toc-text">${it.text}</span>
              <span class="toc-leader"></span>
              <span class="toc-page">${it.pageNum}</span>
            </li>
          `).join('')}
        </ol>
      `;
      document.body.appendChild(tocPage);
    }, items);

    await page.addStyleTag({
      content: `
        .print-toc-page {
          padding: 1.5in 0.85in 1in;
          font-family: "Source Serif 4", Georgia, serif;
          color: #0a0a0a;
          background: #faf6ec;
          min-height: 9.6in;
        }
        .print-toc-eyebrow {
          font-family: "Inter", system-ui, sans-serif;
          font-size: 9pt;
          letter-spacing: 0.22em;
          text-transform: uppercase;
          color: #003f87;
          font-weight: 600;
          margin-bottom: 1.6em;
        }
        .print-toc-list {
          list-style: none;
          padding: 0;
          margin: 0;
        }
        .print-toc-list li {
          display: flex;
          align-items: baseline;
          gap: 0.6em;
          margin: 0.55em 0;
          font-feature-settings: "tnum", "lnum";
        }
        .toc-part-line {
          font-size: 12pt;
          font-weight: 600;
          color: #003f87;
        }
        .toc-appendix-line {
          font-size: 11pt;
          font-style: italic;
          color: #003f87;
        }
        .toc-appendix-line:first-of-type {
          margin-top: 1.4em;
          padding-top: 0.9em;
          border-top: 1px solid #c9bfa6;
        }
        .toc-text { flex: 0 0 auto; }
        .toc-leader {
          flex: 1 1 auto;
          border-bottom: 1px dotted #c9bfa6;
          height: 0.7em;
          margin: 0 0.2em;
        }
        .toc-page {
          flex: 0 0 auto;
          color: #003f87;
          font-weight: 600;
        }
      `,
    });

    return await page.pdf({
      format: 'Letter',
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: false,
    });
  });
}

// Stage 3 — render the body with running header/footer.
async function renderBody() {
  return await withPage(async (page) => {
    await page.addStyleTag({
      content: `@media print { .toc, .html-cover-shim, .cover { display: none !important; } }`,
    });
    return await page.pdf({
      format: 'Letter',
      margin: { top: '0.85in', right: '0.7in', bottom: '0.95in', left: '0.7in' },
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: true,
      headerTemplate: HEADER_BODY,
      footerTemplate: FOOTER_BODY,
    });
  });
}

(async () => {
  console.log('Stage 1: rendering HTML cover…');
  const coverBuf = await renderCover();

  console.log('Stage 2a: measuring heading positions…');
  const headings = await measureBodyPositions();
  console.log(`  found ${headings.length} headings`);

  console.log('Stage 2b: rendering TOC page…');
  const tocBuf = await renderToc(headings);

  console.log('Stage 3: rendering body…');
  const bodyBuf = await renderBody();

  console.log('Merge…');
  const cover = await PDFDocument.load(coverBuf);
  const toc = await PDFDocument.load(tocBuf);
  const body = await PDFDocument.load(bodyBuf);
  const out = await PDFDocument.create();

  for (const src of [cover, toc, body]) {
    const pages = await out.copyPages(src, src.getPageIndices());
    pages.forEach((p) => out.addPage(p));
  }

  const merged = await out.save();
  const outPath = path.resolve(__dirname, 'policy-brief.pdf');
  fs.writeFileSync(outPath, merged);
  const stats = fs.statSync(outPath);
  console.log(`PDF written: ${stats.size} bytes (${out.getPageCount()} pages)`);
  console.log(`  cover: ${cover.getPageCount()}, TOC: ${toc.getPageCount()}, body: ${body.getPageCount()}`);
})();
