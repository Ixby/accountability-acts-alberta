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
// Run: node build-pdf.js           → policy-brief.pdf        (Letter, print)
//      node build-pdf.js --eink    → policy-brief-eink.pdf   (A5, e-ink)
//
// E-ink mode targets the reMarkable 1 (6.2" × 8.3" screen ≈ A5).
// Changes vs print: A5 page, 12pt body, white background, dark monochrome
// accents, minimal chrome, 0.45/0.4/0.5/0.4in margins (top/r/bot/l).

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');

const HTML_PATH = path.resolve(__dirname, 'policy-brief.html');
const FILE_URL = 'file:///' + HTML_PATH.replace(/\\/g, '/');

const EINK = process.argv.includes('--eink');
const OUT_PATH = path.resolve(__dirname, EINK ? 'policy-brief-eink.pdf' : 'policy-brief.pdf');

// Page content height (inches) used to estimate TOC page numbers from DOM y.
// Letter: 11in − 0.85in top − 0.95in bottom = 9.2in
// A5 eink: 8.27in − 0.45in top − 0.50in bottom = 7.32in
const PAGE_CONTENT_IN = EINK ? 7.32 : 9.2;

// CSS injected into the body render for eink output.
const EINK_BODY_CSS = `
  @page {
    size: A5;
    margin: 0.45in 0.4in 0.5in 0.4in;
    @top-left   { content: ""; }
    @top-right  { content: ""; }
    @bottom-left { content: ""; }
    @bottom-right {
      content: counter(page);
      font-family: "Inter", sans-serif;
      font-size: 7pt;
      color: #333;
      vertical-align: top;
      padding-top: 0.2in;
    }
  }
  @page :first { margin: 0.45in 0.4in 0.5in 0.4in; }
  @media print {
    html, body { background: white !important; }
    body { font-size: 12pt !important; line-height: 1.55 !important; }
    h1, h2, h3, h4 { color: #111 !important; }
    h1 { border-bottom-color: #333 !important; }
    h2::before { background: #444 !important; }
    .part-opener::before { color: #111 !important; }
    .part-opener .part-prefix { color: #222 !important; }
    .part-opener .part-title  { color: #000 !important; }
    a { color: #000 !important; text-decoration: none !important; }
    blockquote { background: #f0f0f0 !important; border-left-color: #666 !important; }
    .display-cost { color: #111 !important; }
    .display-cost-label { color: #444 !important; }
    table th {
      color: #111 !important;
      border-top-color: #111 !important;
      border-bottom-color: #555 !important;
    }
    table tr:last-child td { border-bottom-color: #555 !important; }
    .bill-text h2, .bill-text h3 { color: #111 !important; }
    .at-a-glance-block h2 { color: #111 !important; }
  }
`;

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
    await page.addStyleTag({
      content: `
        .site-header, .site-footer { display: none !important; }
        .toc, main { display: none !important; }
        .html-cover-shim { display: block !important; }
        .cover { display: flex !important; page-break-after: avoid; }
        @page { size: ${EINK ? 'A5' : 'Letter'}; margin: 0; }
      `,
    });
    return await page.pdf({
      format: EINK ? 'A5' : 'Letter',
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

    const PAGE_CONTENT_PX = PAGE_CONTENT_IN * 96;
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
        inAppendix = false;
      }
    } else if (h.tag === 'h2' && !inAppendix) {
      items.push({ kind: 'part', text: h.text, pageNum: h.pageNum });
    }
  }

  // Geometry constants: eink = A5, default = Letter
  const tocPadding     = EINK ? '1.0in 0.4in 0.7in' : '1.5in 0.85in 1in';
  const tocMinHeight   = EINK ? '8.0in'              : '9.6in';
  const tocBackground  = EINK ? 'white'              : '#faf6ec';
  const colophonBottom = EINK ? '0.55in'             : '0.9in';
  const colophonSide   = EINK ? '0.4in'              : '0.85in';
  const partColor      = EINK ? '#111'               : '#003f87';
  const leaderColor    = EINK ? '#999'               : '#c9bfa6';
  const eyebrowColor   = EINK ? '#222'               : '#003f87';
  const colophonColor  = EINK ? '#444'               : '#4a4a4a';

  return await withPage(async (page) => {
    await page.evaluate((items) => {
      document.querySelectorAll('.html-cover-shim, .site-header, .site-footer, main').forEach((el) => {
        el.style.display = 'none';
      });
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
        <div class="print-toc-colophon">
          <span class="colophon-line">Drafted by Will Conner &middot; Released under Creative Commons Attribution-ShareAlike 4.0</span>
          <span class="colophon-line">github.com/Ixby/accountability-acts-alberta</span>
        </div>
      `;
      document.body.appendChild(tocPage);
    }, items);

    await page.addStyleTag({
      content: `
        @page { size: ${EINK ? 'A5' : 'Letter'}; margin: 0; }
        .print-toc-page {
          padding: ${tocPadding};
          font-family: "Source Serif 4", Georgia, serif;
          color: #0a0a0a;
          background: ${tocBackground};
          min-height: ${tocMinHeight};
        }
        .print-toc-eyebrow {
          font-family: "Inter", system-ui, sans-serif;
          font-size: 9pt;
          letter-spacing: 0.22em;
          text-transform: uppercase;
          color: ${eyebrowColor};
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
          color: ${partColor};
        }
        .toc-appendix-line {
          font-size: 11pt;
          font-style: italic;
          color: ${partColor};
        }
        .toc-appendix-line:first-of-type {
          margin-top: 1.4em;
          padding-top: 0.9em;
          border-top: 1px solid ${leaderColor};
        }
        .toc-text { flex: 0 0 auto; }
        .toc-leader {
          flex: 1 1 auto;
          border-bottom: 1px dotted ${leaderColor};
          height: 0.7em;
          margin: 0 0.2em;
        }
        .toc-page {
          flex: 0 0 auto;
          color: ${partColor};
          font-weight: 600;
        }
        .print-toc-colophon {
          position: absolute;
          bottom: ${colophonBottom};
          left: ${colophonSide};
          right: ${colophonSide};
          font-family: "Inter", system-ui, sans-serif;
          font-size: 7.5pt;
          color: ${colophonColor};
          letter-spacing: 0.06em;
          padding-top: 0.6em;
          border-top: 1px solid ${leaderColor};
          line-height: 1.6;
        }
        .print-toc-colophon .colophon-line { display: block; }
      `,
    });
    await page.evaluate(() => {
      const tocPage = document.querySelector('.print-toc-page');
      if (tocPage) tocPage.style.position = 'relative';
    });

    return await page.pdf({
      format: EINK ? 'A5' : 'Letter',
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: false,
    });
  });
}

// Stage 3 — render the body.
async function renderBody() {
  return await withPage(async (page) => {
    await page.addStyleTag({
      content: `
        @media print { .toc, .html-cover-shim, .cover { display: none !important; } }
        @page :first { margin: ${EINK ? '0.45in 0.4in 0.5in 0.4in' : '0.85in 0.7in 0.95in 0.7in'}; }
        ${EINK ? EINK_BODY_CSS : ''}
      `,
    });
    return await page.pdf({
      format: EINK ? 'A5' : 'Letter',
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: false,
    });
  });
}

(async () => {
  if (EINK) console.log('E-ink mode: A5, 12pt, white background → ' + OUT_PATH);

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
  const toc   = await PDFDocument.load(tocBuf);
  const body  = await PDFDocument.load(bodyBuf);
  const out   = await PDFDocument.create();

  for (const src of [cover, toc, body]) {
    const pages = await out.copyPages(src, src.getPageIndices());
    pages.forEach((p) => out.addPage(p));
  }

  const merged = await out.save();
  fs.writeFileSync(OUT_PATH, merged);
  const stats = fs.statSync(OUT_PATH);
  console.log(`PDF written: ${stats.size} bytes (${out.getPageCount()} pages)`);
  console.log(`  cover: ${cover.getPageCount()}, TOC: ${toc.getPageCount()}, body: ${body.getPageCount()}`);
})();
