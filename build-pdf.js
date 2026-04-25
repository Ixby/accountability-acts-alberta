// Build the policy-brief PDF in three stages, then merge.
//
// Stage 1: cover.pdf already exists at the repo root (a Canva-designed cover).
// Stage 2: render the BODY of the brief (Parts I–VII + Appendices), without TOC.
//          During this render we measure where each Part / Appendix landing falls
//          in the resulting PDF, so the TOC page numbers can be accurate.
// Stage 3: render the TOC PAGE alone, with the measured page numbers injected.
// Stage 4: merge cover + TOC + body via pdf-lib. Body pages carry the
//          running header/footer with page numbers starting at 1.
//
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
    <span style="letter-spacing: 0.06em;">Drafted by Will Conner &middot; CC BY-SA 4.0</span>
    <span style="font-feature-settings: 'tnum';"><span class="pageNumber"></span></span>
  </div>`;
const EMPTY = `<span style="display:none"></span>`;

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

// Compute page numbers for headings by measuring each anchor's position in
// the printed body PDF. Body pages start at "1" — the cover and TOC are
// outside the numbered range.
async function measureBodyPositions() {
  return await withPage(async (page) => {
    // Hide the TOC and the html-cover-shim and the site-header/footer so the
    // measured positions reflect the BODY-only layout.
    await page.addStyleTag({
      content: `
        @media screen {
          .toc, .html-cover-shim, .site-header, .site-footer { display: none !important; }
          body { background: white; }
        }
      `,
    });

    // Render to a temp PDF using the same print settings as the final.
    const tmpPath = path.resolve(__dirname, '_body-measure.pdf');
    await page.pdf({
      path: tmpPath,
      format: 'Letter',
      margin: { top: '0.85in', right: '0.7in', bottom: '0.95in', left: '0.7in' },
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: false,
    });

    // Use pdf-lib to count pages, but for page-mapping we use a different
    // technique: render each heading marker with a page-break-before:always
    // for measurement is too disruptive. Instead, use the rendered HTML
    // viewport positions and divide by content height per page.

    // Print page content height (Letter 11in - 0.85in - 0.95in = 9.2in = 9.2*96 = 883.2 px at 96 DPI).
    // But puppeteer prints at 96 DPI for HTML, so the screen layout maps directly.
    const PAGE_CONTENT_PX = 9.2 * 96; // 883.2

    const headings = await page.evaluate((PAGE_CONTENT_PX) => {
      const out = [];
      const all = document.querySelectorAll('main h1, main h2');
      all.forEach((el) => {
        const id = el.id;
        if (!id) return;
        const text = el.textContent.replace(/¶$/, '').trim();
        const rect = el.getBoundingClientRect();
        const top = rect.top + window.scrollY;
        // Body-only page number = floor(top / page_content_px) + 1
        const pageNum = Math.floor(top / PAGE_CONTENT_PX) + 1;
        const tag = el.tagName.toLowerCase();
        out.push({ id, tag, text, top, pageNum });
      });
      return out;
    }, PAGE_CONTENT_PX);

    // Cleanup temp
    try { fs.unlinkSync(tmpPath); } catch (e) {}
    return headings;
  });
}

async function renderBody() {
  return await withPage(async (page) => {
    await page.addStyleTag({
      content: `@media print { .toc { display: none !important; } }`,
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

async function renderToc(headings) {
  // Build a TOC HTML page that prints standalone, with the measured page
  // numbers shown to the right of each entry. We render this by injecting
  // a printable TOC into the existing HTML (replacing the existing .toc
  // contents) and using pageRanges to grab only the TOC page(s).

  // Build TOC HTML with page numbers
  const items = headings
    .filter((h) => h.tag === 'h1' || h.tag === 'h2')
    .filter((h) => {
      const lc = h.text.toLowerCase();
      // Skip the title/document h1 (it's the cover).
      // Skip "At a glance" and "A note from the drafter".
      if (lc.startsWith('a note from')) return false;
      if (lc.startsWith('at a glance')) return false;
      // Skip h2s INSIDE appendices — only show appendix titles (h1s).
      return true;
    });

  // Walk the items: keep h2 only when not inside an appendix; keep h1 only
  // when it's "Appendix ..."; skip the leading document title h1.
  const tocItems = [];
  let inAppendix = false;
  for (const h of items) {
    if (h.tag === 'h1') {
      if (h.text.toLowerCase().startsWith('appendix')) {
        tocItems.push({ kind: 'appendix', text: h.text, pageNum: h.pageNum, id: h.id });
        inAppendix = true;
      } else {
        // Document title — skip
        inAppendix = false;
      }
    } else if (h.tag === 'h2' && !inAppendix) {
      tocItems.push({ kind: 'part', text: h.text, pageNum: h.pageNum, id: h.id });
    }
  }

  return await withPage(async (page) => {
    // Hide everything except the TOC area, replace TOC content with our own
    await page.evaluate((items) => {
      // Hide everything in main except a special TOC container we'll inject
      const main = document.querySelector('main');
      if (main) {
        // Wrap the existing main content so we can hide it
        const allChildren = Array.from(main.children);
        allChildren.forEach((c) => { c.style.display = 'none'; });
      }
      const cover = document.querySelector('.html-cover-shim');
      if (cover) cover.style.display = 'none';

      // Build the TOC container
      const toc = document.createElement('div');
      toc.className = 'print-toc-page';
      toc.innerHTML = `
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
      main.appendChild(toc);
    }, tocItems);

    // Add print CSS for the TOC page
    await page.addStyleTag({
      content: `
        @media print {
          .site-header, .site-footer { display: none !important; }
        }
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
          color: #6b1f1f;
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
        }
        .toc-appendix-line {
          font-size: 11pt;
          font-style: italic;
        }
        .toc-appendix-line:first-of-type {
          margin-top: 1.4em;
          padding-top: 0.9em;
          border-top: 1px solid #c9bfa6;
        }
        .toc-text {
          flex: 0 0 auto;
        }
        .toc-leader {
          flex: 1 1 auto;
          border-bottom: 1px dotted #c9bfa6;
          height: 0.7em;
          margin: 0 0.2em;
        }
        .toc-page {
          flex: 0 0 auto;
          color: #6b1f1f;
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

(async () => {
  console.log('Stage 1: cover.pdf (already on disk, Canva-designed)');
  const coverPath = path.resolve(__dirname, 'cover.pdf');
  if (!fs.existsSync(coverPath)) {
    throw new Error(`cover.pdf not found at ${coverPath}. Generate one via Canva (or any PDF) and place it at the repo root.`);
  }

  console.log('Stage 2: measuring heading positions in body…');
  const headings = await measureBodyPositions();
  console.log(`  found ${headings.length} headings`);

  console.log('Stage 3: rendering TOC page…');
  const tocBuf = await renderToc(headings);

  console.log('Stage 4: rendering body…');
  const bodyBuf = await renderBody();

  console.log('Merge…');
  const cover = await PDFDocument.load(fs.readFileSync(coverPath));
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
  console.log(`  cover: 1 page, TOC: ${toc.getPageCount()}, body: ${body.getPageCount()}`);
})();
