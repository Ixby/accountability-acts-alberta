"""Build policy-brief.html from policy-brief.md.

Self-contained single-file HTML with:
- Cover page (front matter)
- Auto-generated table of contents from h1/h2/h3 headings
- Internal anchor links
- Inline CSS for typography and print
- Header and footer linking to the repository
"""

import markdown
import re
from datetime import datetime
from pathlib import Path

REPO_URL = "https://github.com/Ixby/accountability-acts-alberta"
SOURCE = Path(__file__).parent / "policy-brief.md"
TARGET = Path(__file__).parent / "policy-brief.html"

PUBLICATION_DATE = "April 2026"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400;1,8..60,600&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --ink: #1a1a1a;
  --ink-soft: #444;
  --paper: #fdfaf3;
  --paper-deep: #f4ecd9;
  --muted: #5d5d5d;
  --rule: #d8d0bd;
  --accent: #003f87;
  --accent-soft: #2a5fa0;
  --accent-warm: #c08a1a;
  --link: #003f87;
  --link-visited: #2a4a7a;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: "Source Serif 4", "Iowan Old Style", "Palatino Linotype", Georgia, serif;
  font-size: 18px;
  line-height: 1.55;
  font-feature-settings: "onum", "kern";
  -webkit-font-smoothing: antialiased;
}

/* ===== Cover page (scaffolding / stepping-toward-justice) ===== */

.cover {
  position: relative;
  min-height: 100vh;
  background: #f2ead0;
  color: #003f87;
  padding: 0;
  overflow: hidden;
  page-break-after: always;
}

.cover-inner {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 1.4in 1.1in 1.1in;
}

.cover-eyebrow {
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.72rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: #a4253a;
  font-weight: 600;
  margin: 0 0 1em;
}

.cover-title-block {
  margin-top: auto;
  margin-bottom: 1.4em;
}

.cover-title {
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 700;
  font-size: clamp(2.2rem, 7.8vw, 5.4rem);
  line-height: 0.96;
  letter-spacing: -0.025em;
  color: #003f87;
  margin: 0;
  text-transform: uppercase;
}
.cover-title .word { display: block; }
.cover-title .word--line-1,
.cover-title .word--line-2,
.cover-title .word--line-3 { margin-bottom: 0.04em; }
.cover-title .word--line-4 {
  font-style: italic;
  font-weight: 400;
  letter-spacing: -0.02em;
}

/* Five wheat-gold rungs forming a forced-perspective scaffold beneath
   the title. The longest rung sits farthest from the viewer (top, near
   the title); each successive rung is shorter, thicker, and more
   saturated, layered in front of the rung above it. The shorter
   foreground rungs partially overlap the longer ones behind without
   covering them — the unobscured ends remain visible, preserving the
   sense of depth and proportionality. The eye reads the stack as
   looking up a ladder from below. */
.cover-scaffold {
  position: relative;
  margin: 1.2em 0 1.6em;
  height: 56px;
}
.cover-scaffold .rung {
  position: absolute;
  left: 0;
  display: block;
  border: none;
  background: #f2a900;
}
/* Top rung — farthest from viewer, closest to the title above.
   Longest, thinnest, most faded. */
.cover-scaffold .rung-5 {
  top: 0;
  width: 80%;
  height: 1px;
  opacity: 0.4;
  z-index: 1;
}
.cover-scaffold .rung-4 {
  top: 9px;
  width: 58%;
  height: 2px;
  opacity: 0.65;
  z-index: 2;
}
.cover-scaffold .rung-3 {
  top: 19px;
  width: 40%;
  height: 3px;
  background: #f2a900;
  z-index: 3;
}
.cover-scaffold .rung-2 {
  top: 30px;
  width: 26%;
  height: 4px;
  background: #e69d00;
  z-index: 4;
}
/* Bottom rung — closest to viewer, foreground.
   Shortest, thickest, deepest saturation. */
.cover-scaffold .rung-1 {
  top: 42px;
  width: 14%;
  height: 5px;
  background: #d99100;
  z-index: 5;
}

.cover-subtitle {
  font-family: "Source Serif 4", Georgia, serif;
  font-style: italic;
  font-weight: 400;
  font-size: clamp(1rem, 1.7vw, 1.18rem);
  line-height: 1.45;
  color: #003f87;
  margin: 0;
  max-width: 42ch;
}

.cover-foot-block {
  margin-top: auto;
  padding-top: 2em;
  border-top: 1px solid rgba(0, 63, 135, 0.18);
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.78rem;
  line-height: 1.6;
  color: #003f87;
}
.cover-foot-grid {
  display: block;
}
.cover-foot-name-label {
  display: block;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-size: 0.7rem;
  color: #a4253a;
  margin-bottom: 0.3em;
}
.cover-foot-author {
  display: block;
  font-family: "Source Serif 4", Georgia, serif;
  font-style: italic;
  font-size: 1.1rem;
  color: #003f87;
  margin-bottom: 1em;
}
.cover-foot-license {
  display: block;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
}
.cover-foot-license .license-line { display: block; }
.cover-foot-license a {
  color: inherit;
  text-decoration: none;
  border-bottom: 1px solid #f2a900;
}

/* ===== Site chrome ===== */

.site-header {
  background: var(--ink);
  color: var(--paper);
  padding: 1.6rem 0 1.4rem;
  border-bottom: 1px solid rgba(250,246,236,0.15);
  position: sticky;
  top: 0;
  z-index: 50;
}
.site-header .wrap {
  max-width: 920px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.site-header .brand {
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.78rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-weight: 500;
}
.site-header a {
  color: var(--paper);
  text-decoration: none;
  border-bottom: 1px dotted rgba(250,246,236,0.5);
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  letter-spacing: 0.04em;
}
.site-header a:hover { border-bottom-style: solid; }

main {
  max-width: 720px;
  margin: 0 auto;
  padding: 4rem 1.5rem 5rem;
}

/* ===== Headings ===== */

h1, h2, h3, h4 {
  font-family: "Source Serif 4", Georgia, serif;
  color: var(--ink);
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: -0.005em;
}
h1 {
  font-size: clamp(2rem, 4vw, 2.6rem);
  margin: 0.2em 0 0.7em;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--accent);
}
h2 {
  font-size: 1.65rem;
  margin: 3.5em 0 0.8em;
  padding-bottom: 0.25rem;
  position: relative;
}
h2::before {
  content: "";
  display: block;
  width: 2.5rem;
  height: 2px;
  background: var(--accent);
  margin-bottom: 1.2rem;
}

/* Part-opener: each "Part I/II/.../VII — Title" h2 carries a separate
   monumental Roman-numeral prefix in deep Alberta-blue, with the title
   in italic serif beneath it. Pulls the cover's blue cameo into the body. */
h2.part-opener {
  margin-top: 4em;
  padding-top: 0.6em;
  border-top: 1px solid var(--rule);
  display: block;
}
h2.part-opener::before {
  content: attr(data-numeral);
  display: block;
  width: auto;
  height: auto;
  background: transparent;
  font-family: "Source Serif 4", Georgia, serif;
  font-size: 4rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.02em;
  color: #003f87;
  margin: 0 0 0.15em;
}
h2.part-opener .part-prefix {
  display: block;
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #003f87;
  margin-bottom: 0.2em;
}
h2.part-opener .part-title {
  display: block;
  font-family: "Source Serif 4", Georgia, serif;
  font-style: italic;
  font-weight: 600;
  font-size: 1.4rem;
  color: var(--ink);
  letter-spacing: -0.005em;
}
h3 {
  font-size: 1.25rem;
  margin: 2.4em 0 0.6em;
  font-weight: 600;
}
h4 {
  font-size: 1.05rem;
  margin: 1.8em 0 0.5em;
  font-weight: 600;
}
h1 + p em, h2 + p em {
  color: var(--muted);
  font-style: italic;
}

/* ===== Body text ===== */

p, ul, ol { margin: 0.85em 0; }
ul, ol { padding-left: 1.6em; }
li { margin: 0.35em 0; }
strong { font-weight: 700; }
em { font-style: italic; }

a {
  color: var(--link);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-decoration-color: rgba(107, 31, 31, 0.4);
  text-underline-offset: 3px;
  transition: text-decoration-color 0.15s;
}
a:visited { color: var(--link-visited); }
a:hover { text-decoration-color: var(--accent); }

code {
  background: var(--paper-deep);
  padding: 0.1em 0.4em;
  border-radius: 2px;
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.88em;
}
pre {
  background: var(--paper-deep);
  padding: 1.2em;
  border-radius: 3px;
  overflow-x: auto;
  font-size: 0.88em;
  border-left: 3px solid var(--accent);
}
pre code { background: none; padding: 0; }

blockquote {
  margin: 1.5em 0;
  padding: 1em 1.5em;
  background: var(--paper-deep);
  border-left: 3px solid var(--accent);
  font-size: 0.97em;
  color: var(--ink-soft);
}
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }

hr {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 2.8em auto;
  max-width: 6rem;
}

/* ===== Tables ===== */

table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.6em 0;
  font-size: 0.96em;
  font-feature-settings: "tnum", "lnum";
}
th, td {
  padding: 0.65em 0.9em;
  text-align: left;
  vertical-align: top;
  border-bottom: 1px solid var(--rule);
}
th {
  background: transparent;
  font-weight: 600;
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.85em;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--accent);
  border-top: 2px solid var(--ink);
  border-bottom: 1px solid var(--ink);
}
table tr:last-child td {
  border-bottom: 2px solid var(--ink);
}

/* Cost table — promoted */
.at-a-glance + table,
table.cost-table {
  margin: 2em 0 2.5em;
}
table td:nth-child(2),
table td:nth-child(3) {
  font-feature-settings: "tnum", "lnum";
}

/* ===== TOC ===== */

.toc {
  background: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 3px;
  padding: 2em 2.5em;
  margin: 3em 0 4em;
  position: relative;
}
.toc::before {
  content: "";
  position: absolute;
  top: -1px; left: -1px; right: -1px;
  height: 3px;
  background: var(--accent);
  border-radius: 3px 3px 0 0;
}
.toc h2 {
  margin-top: 0;
  border: none;
  padding-bottom: 0;
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.85rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--accent);
  font-weight: 600;
}
.toc h2::before { display: none; }
.toc ol {
  list-style: none;
  padding-left: 0;
  margin: 0.8em 0 0;
  counter-reset: toc;
}
.toc ol ol {
  padding-left: 1.5em;
  margin: 0.3em 0 0.5em;
  font-size: 0.94em;
}
.toc li { margin: 0.55em 0; }
.toc li.toc-part {
  font-family: "Source Serif 4", Georgia, serif;
  font-size: 1.05rem;
  font-weight: 600;
}
.toc li.toc-appendix {
  font-family: "Source Serif 4", Georgia, serif;
  font-size: 0.98rem;
  font-style: italic;
  margin-top: 0.85em;
}
.toc li.toc-appendix:first-of-type {
  margin-top: 1.6em;
  padding-top: 0.9em;
  border-top: 1px solid var(--rule);
}
.toc a {
  color: var(--ink);
  text-decoration: none;
  border-bottom: 1px dotted transparent;
  transition: all 0.15s;
}
.toc a:hover {
  color: var(--accent);
  border-bottom-color: var(--accent);
  border-bottom-style: solid;
}

/* ===== Bill text — statutory typography ===== */

.bill-text {
  font-size: 0.95em;
  line-height: 1.45;
}
.bill-text h2 {
  font-family: "Inter", system-ui, sans-serif;
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--accent);
  text-transform: none;
  margin-top: 2.4em;
}
.bill-text h2::before {
  width: 1.8rem;
  background: var(--accent-soft);
}
.bill-text h3 {
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.92rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent);
}
.bill-text blockquote {
  background: transparent;
  border-left: 2px solid var(--rule);
  margin: 0.8em 0;
  padding: 0.4em 1.2em;
  font-size: 0.96em;
  color: var(--ink);
}

/* ===== At a glance — promoted block ===== */

.at-a-glance-block {
  margin: 3em 0 2em;
}
.at-a-glance-block h2 {
  margin-top: 0;
}
.at-a-glance-block table {
  margin-top: 1em;
}
.at-a-glance-block table td:nth-child(2),
.at-a-glance-block table td:nth-child(3) {
  font-feature-settings: "lnum", "tnum";
  font-weight: 600;
}
.at-a-glance-block table td:last-child {
  font-style: italic;
  color: var(--ink-soft);
}

/* ===== Heading anchors ===== */

.heading-anchor {
  color: var(--rule);
  text-decoration: none;
  margin-left: 0.4em;
  font-size: 0.7em;
  opacity: 0;
  transition: opacity 0.15s;
}
h1:hover .heading-anchor,
h2:hover .heading-anchor,
h3:hover .heading-anchor,
h4:hover .heading-anchor { opacity: 1; }

/* ===== Display moments ===== */

.display-cost {
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 700;
  font-size: clamp(2.5rem, 6vw, 4rem);
  line-height: 1;
  letter-spacing: -0.02em;
  color: var(--accent);
  text-align: center;
  margin: 2em 0 0.4em;
  font-feature-settings: "tnum", "lnum";
}
.display-cost-label {
  display: block;
  text-align: center;
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.78rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 2em;
  font-weight: 500;
}

.pull-quote {
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 600;
  font-size: 1.4rem;
  line-height: 1.35;
  color: var(--accent);
  border-left: none;
  border-top: 2px solid var(--accent);
  border-bottom: 2px solid var(--accent);
  padding: 1.2em 0;
  margin: 2em 0;
  text-align: center;
  background: transparent;
  font-style: italic;
}

/* ===== Footer ===== */

.site-footer {
  border-top: 1px solid var(--rule);
  margin-top: 5rem;
  padding: 2.5rem 0;
  background: var(--paper);
  font-size: 0.92em;
  color: var(--muted);
}
.site-footer .wrap {
  max-width: 720px;
  margin: 0 auto;
  padding: 0 1.5rem;
}
.site-footer p { margin: 0.5em 0; }
.site-footer a { color: var(--accent); }

.back-to-top {
  display: inline-block;
  font-size: 0.85em;
  color: var(--muted);
  text-decoration: none;
  margin-top: 0.6em;
}
.back-to-top:hover { color: var(--accent); }

/* ===== Responsive ===== */

@media (max-width: 700px) {
  body { font-size: 17px; }
  main { padding: 2.5rem 1.2rem 3.5rem; }
  h1 { font-size: 1.85rem; }
  h2 { font-size: 1.4rem; margin-top: 2.5em; }
  h3 { font-size: 1.15rem; }
  .toc { padding: 1.2em 1.5em; }
  .cover { padding: 8vh 6vw 5vh; }
  .cover-meta .meta-label { width: 6rem; }
}

/* ===== Print ===== */

@page {
  size: Letter;
  margin: 0.85in 0.7in 0.95in 0.7in;
  @top-left {
    content: string(brief-title);
    font-family: "Inter", sans-serif;
    font-size: 8pt;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6b1f1f;
    vertical-align: bottom;
    padding-bottom: 0.3in;
  }
  @top-right {
    content: string(running-part);
    font-family: "Inter", sans-serif;
    font-size: 8pt;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #003f87;
    vertical-align: bottom;
    padding-bottom: 0.3in;
  }
  @bottom-left {
    content: "Drafted by Will Conner · CC BY-SA 4.0";
    font-family: "Inter", sans-serif;
    font-size: 8pt;
    color: #4a4a4a;
    letter-spacing: 0.06em;
    vertical-align: top;
    padding-top: 0.35in;
  }
  @bottom-right {
    content: counter(page);
    font-family: "Inter", sans-serif;
    font-size: 8pt;
    color: #4a4a4a;
    font-feature-settings: "tnum";
    vertical-align: top;
    padding-top: 0.35in;
  }
}
@page :first {
  margin: 0;
  @top-left { content: ""; }
  @top-right { content: ""; }
  @bottom-left { content: ""; }
  @bottom-right { content: ""; }
}
/* Document title is set once on the body via a hidden anchor, then
   string()-referenced from @top-left on every page. */
body::before {
  content: "What Accountable Government Looks Like";
  string-set: brief-title content();
  display: none;
}
/* Each Part-opener H2 sets the running-part string. As the layout
   engine paginates, the latest string-set value is what appears in
   @top-right — so each Part's pages carry that Part's name. */
h2.part-opener .part-prefix {
  string-set: running-part content();
}
/* Hidden span anchors set the running-part string for the bill
   appendices. They don't render visually (visibility:hidden keeps
   them in the page flow so string-set fires) but the engine captures
   the content into the running header string. */
.running-anchor {
  visibility: hidden;
  height: 0;
  overflow: hidden;
  string-set: running-part content();
}

@media print {
  html, body { background: white; }
  body {
    font-size: 11pt;
    line-height: 1.5;
    color: var(--ink);
    font-weight: 400;
    orphans: 3;
    widows: 3;
    -webkit-font-smoothing: antialiased;
  }
  /* The HTML TOC is replaced in the merged PDF by a measurement-driven
     TOC page rendered separately. Hide the inline TOC in print. The
     cover (now designed in HTML/CSS) is rendered as page 1 separately
     too — the build-pdf pipeline extracts it via pageRanges. */
  .toc { display: none !important; }
  .html-cover-shim { display: block; }
  .cover {
    display: flex !important;
    page-break-after: always;
    width: 8.5in;
    height: 11in;
    min-height: 11in;
    background: #f2ead0;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
  }
  .cover-inner {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    padding: 1.2in 1in;
  }
  .cover-eyebrow {
    font-size: 8pt;
    margin-bottom: 1.2in;
  }
  .cover-title { font-size: 50pt; line-height: 0.96; }
  .cover-subtitle { font-size: 11pt; max-width: 36ch; }
  .cover-foot-block {
    font-size: 9pt;
  }
  .cover-foot-name { font-size: 8.5pt; letter-spacing: 0.14em; }
  .cover-foot-license { font-size: 10pt; }
  .cover-foot-source { font-size: 8pt; }
  p, li, blockquote { orphans: 3; widows: 3; }
  .site-header, .site-footer, .heading-anchor, .back-to-top { display: none !important; }

  /* Universal column: every section uses the same text width.
     The page margin (0.7in) sets the column. main and bill-text and
     at-a-glance-block all live inside the same column. */
  main {
    max-width: none;
    padding: 0;
    margin: 0;
  }
  main > * { max-width: none; }

  /* Headings — no forced page breaks. Let content flow naturally.
     keep-with-next: page-break-after:avoid + ensure at least 3 lines
     of body land underneath, otherwise the heading migrates to the
     next page (the user's stated exception: a header alone at end of
     page is OK only if its paragraph won't fit beneath it). */
  h1 {
    page-break-before: avoid;
    page-break-after: avoid;
    break-after: avoid-page;
    font-size: 22pt;
    line-height: 1.1;
    margin: 2em 0 0.5em;
    border-bottom: 0.5pt solid var(--accent);
    padding-bottom: 0.3em;
  }
  /* Defensive top-padding on the very first H1 of the document so the
     puppeteer running header (which prints in the page margin) clears
     the H1 baseline. Without this, "REBUILDING TRUST" oxblood caps
     and the H1's own border-bottom can graze. */
  main > h1:first-child {
    margin-top: 0.4in;
  }
  h1 + h2 { margin-top: 0.8em; }
  h2 {
    page-break-after: avoid;
    break-after: avoid-page;
    font-size: 13pt;
    line-height: 1.2;
    margin: 1.5em 0 0.45em;
  }
  h2::before { width: 1.8em; height: 1pt; margin-bottom: 0.6em; }
  /* Part-opener in print: each Part starts a new page with the
     oversized Roman numeral and the deep-blue prefix. */
  h2.part-opener {
    page-break-before: always;
    margin-top: 0;
    padding-top: 0.6in;
    border-top: none;
  }
  h2.part-opener::before {
    font-size: 48pt;
    margin-bottom: 0.1em;
  }
  h2.part-opener .part-prefix {
    font-size: 9pt;
    margin-bottom: 0.3em;
  }
  h2.part-opener .part-title {
    font-size: 18pt;
  }
  h3 {
    page-break-after: avoid;
    break-after: avoid-page;
    font-size: 11.5pt;
    line-height: 1.25;
    margin: 1.1em 0 0.35em;
    font-weight: 600;
  }
  /* Keep at least three lines of paragraph with the heading above. */
  h2 + p, h3 + p, h4 + p { page-break-before: avoid; break-before: avoid-page; }

  /* Statutory text — same column width as narrative, slightly smaller
     type. 10pt with 1.4 line-height keeps Source Serif 4 strokes solid;
     9.5pt was thinning the rendering at print resolution. Statutory
     paragraphs are structurally self-bounded by their (1)/(2)/(a)/(b)
     numbering — they don't need novel-prose orphan/widow protection,
     so we relax the rule to 2 lines inside .bill-text. This recovers
     the heading-can't-fit-paragraph ghost pages that were dropping
     ~3 inches of cream after short cross-reference headings. */
  .bill-text {
    font-size: 10pt;
    line-height: 1.45;
    font-weight: 400;
  }
  .bill-text p, .bill-text li, .bill-text blockquote {
    orphans: 2;
    widows: 2;
  }
  /* Short cross-reference headings ("15A. The following is added after
     section 82.1:") are connectors, not section openers. Don't bind
     them to the next paragraph. */
  .bill-text p + h3, .bill-text blockquote + h3 {
    page-break-after: auto;
    break-after: auto;
  }
  .bill-text h2 {
    font-size: 11pt;
    color: var(--accent);
    text-transform: none;
    margin-top: 1.4em;
    font-weight: 600;
  }
  .bill-text h3 {
    font-size: 9.5pt;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--accent);
    margin-top: 1em;
    font-weight: 600;
  }
  .bill-text blockquote {
    margin: 0.4em 0;
    padding: 0.3em 0.9em;
    font-size: 9.5pt;
    border-left-width: 1pt;
    border-color: var(--rule);
  }

  /* Page-break-inside: avoid for atomic units, no forced breaks. */
  blockquote, table, pre, .display-cost, .pull-quote {
    page-break-inside: avoid;
  }

  /* At-a-glance table sits in line with the rest of the narrative now —
     no forced page break before or after. */
  .at-a-glance-block {
    margin: 1.5em 0 1.2em;
    page-break-inside: avoid;
  }
  .at-a-glance-block h2 {
    font-size: 11pt;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.16em;
    margin-bottom: 0.6em;
  }
  .at-a-glance-block h2::before { display: none; }
  .at-a-glance-block table {
    margin-top: 0.4em;
    font-size: 10.5pt;
  }
  .at-a-glance-block table td {
    padding: 0.55em 0.7em;
  }
  .at-a-glance-block table td:nth-child(2) {
    font-size: 12pt;
    color: var(--accent);
    font-weight: 700;
  }

  a {
    color: var(--ink);
    text-decoration: none;
    border-bottom: none;
  }
  a[href^="http"]:after { content: ""; }

  table th {
    border-top: 1pt solid var(--ink);
    border-bottom: 0.5pt solid var(--ink);
    background: transparent;
  }
  table tr:last-child td {
    border-bottom: 1pt solid var(--ink);
  }

  /* Display moment — sized to be a real event but not its own page. */
  .display-cost {
    font-size: 44pt;
    margin: 0.5em 0 0.1em;
    letter-spacing: -0.02em;
    line-height: 1;
  }
  .display-cost-label {
    margin-bottom: 0.6em;
    font-size: 8.5pt;
    letter-spacing: 0.24em;
  }

  .pull-quote {
    font-size: 13pt;
    border-color: var(--accent);
  }

  blockquote {
    background: transparent;
    border-left-width: 1.5pt;
    padding: 0.4em 1em;
    margin: 0.8em 0;
  }

  /* Closing end-mark + colophon on the final page — turns trailing
     cream into intentional silence rather than a trailing-off feeling. */
  .end-mark {
    text-align: center;
    color: var(--accent);
    font-size: 14pt;
    letter-spacing: 0.5em;
    margin: 3em 0 1.5em;
    page-break-before: avoid;
  }
  .end-colophon {
    text-align: center;
    font-family: "Inter", system-ui, sans-serif;
    font-size: 8.5pt;
    line-height: 1.7;
    color: var(--muted);
    letter-spacing: 0.04em;
    page-break-before: avoid;
  }
  .end-colophon em {
    font-family: "Source Serif 4", Georgia, serif;
    font-style: italic;
    font-size: 10pt;
    color: var(--ink-soft);
    display: block;
    margin-bottom: 0.4em;
  }
}

/* Screen styles for end-mark/colophon — keep visible on web too. */
.end-mark {
  text-align: center;
  color: var(--accent);
  font-size: 1.1rem;
  letter-spacing: 0.6em;
  margin: 3rem 0 1.5rem;
}
.end-colophon {
  text-align: center;
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.82rem;
  line-height: 1.7;
  color: var(--muted);
}
.end-colophon em {
  font-family: "Source Serif 4", Georgia, serif;
  font-size: 1rem;
  color: var(--ink-soft);
  display: block;
  margin-bottom: 0.3em;
}
"""

def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text or "section"


COVER_HTML = f"""<section class="cover" aria-label="Cover">
  <div class="cover-inner">
    <div class="cover-eyebrow">A drafted policy package &nbsp; {PUBLICATION_DATE}</div>
    <div class="cover-title-block">
      <h1 class="cover-title">
        <span class="word word--line-1">What</span>
        <span class="word word--line-2">Accountable</span>
        <span class="word word--line-3">Government</span>
        <span class="word word--line-4">Looks Like</span>
      </h1>
      <div class="cover-scaffold" aria-hidden="true">
        <span class="rung rung-5"></span>
        <span class="rung rung-4"></span>
        <span class="rung rung-3"></span>
        <span class="rung rung-2"></span>
        <span class="rung rung-1"></span>
      </div>
      <p class="cover-subtitle">Two drafted bills &mdash; the Public Integrity Act of Alberta and the Open Books Act &mdash; the rules Alberta should already have, drafted as if we did.</p>
    </div>
    <div class="cover-foot-block">
      <div class="cover-foot-grid">
        <div>
          <span class="cover-foot-name-label">Drafted by</span>
          <span class="cover-foot-author">Will Conner</span>
        </div>
        <div class="cover-foot-license">
          <span class="license-line">Creative Commons Attribution-ShareAlike 4.0</span>
          <span class="license-line"><a href="{REPO_URL}">{REPO_URL.replace('https://','')}</a></span>
        </div>
      </div>
    </div>
  </div>
</section>"""


def build():
    md_text = SOURCE.read_text(encoding="utf-8")

    md = markdown.Markdown(
        extensions=[
            "extra",
            "tables",
            "sane_lists",
            "footnotes",
        ],
        extension_configs={
            "footnotes": {
                "PLACE_MARKER": "///FOOTNOTES_HERE///",
                "BACKLINK_TEXT": "↩",
            },
        },
        output_format="html5",
    )
    body_html = md.convert(md_text)

    # Convert any surviving relative .md links to GitHub absolute URLs.
    def relink(match):
        href = match.group(1)
        if href.startswith("#") or href.startswith("http") or href.startswith("mailto:"):
            return match.group(0)
        if href.endswith(".md") or href.startswith("LICENSE"):
            return f'href="{REPO_URL}/blob/main/{href}"'
        return match.group(0)
    body_html = re.sub(r'href="([^"]+)"', relink, body_html)

    # Add anchor IDs to headings and build a TOC.
    headings = []
    seen_slugs = {}

    def repl_heading(match):
        level = int(match.group(1))
        attrs = match.group(2) or ""
        inner = match.group(3)
        text_only = re.sub(r"<[^>]+>", "", inner).strip()
        base_slug = slugify(text_only)
        n = seen_slugs.get(base_slug, 0)
        seen_slugs[base_slug] = n + 1
        slug = base_slug if n == 0 else f"{base_slug}-{n}"
        if level <= 3:
            headings.append((level, text_only, slug))
        anchor = f' <a class="heading-anchor" href="#{slug}" aria-label="Link to this section">¶</a>'
        return f'<h{level} id="{slug}"{attrs}>{inner}{anchor}</h{level}>'

    body_html = re.sub(
        r"<h([1-4])([^>]*)>(.*?)</h\1>",
        repl_heading,
        body_html,
        flags=re.DOTALL,
    )

    # Part-opener treatment: every "Part I/II/III/.../VII — Title" h2 gets
    # a class plus a data-numeral attribute (the Roman numeral) so we can
    # render the oversized blue numeral above the heading via CSS.
    def tag_part_opener(match):
        attrs = match.group(1)
        inner = match.group(2)
        m = re.match(r"\s*Part\s+([IVX]+)\s*[—-]\s*(.+)", re.sub(r"<[^>]+>", "", inner).strip())
        if not m:
            return match.group(0)
        numeral = m.group(1)
        title_only = m.group(2).strip()
        # Insert class and data-numeral
        if 'class="' in attrs:
            new_attrs = re.sub(r'class="([^"]*)"', r'class="\1 part-opener"', attrs)
        else:
            new_attrs = attrs + ' class="part-opener"'
        new_attrs += f' data-numeral="{numeral}"'
        # Replace inner with just the title (the Part X — prefix is now visual)
        return f'<h2{new_attrs}><span class="part-prefix">Part {numeral}</span><span class="part-title">{title_only}</span></h2>'

    body_html = re.sub(
        r"<h2([^>]*)>(.*?)</h2>",
        tag_part_opener,
        body_html,
        flags=re.DOTALL,
    )

    # Add display treatment to the $200-300 million cost figure in Part I close.
    # Look for the specific paragraph that contains that text.
    body_html = re.sub(
        r"(<p>The combined cost: somewhere between \$200 and \$300 million\.[^<]*</p>)",
        '<div class="display-cost">$200&ndash;300M</div>'
        '<div class="display-cost-label">across three Alberta decisions</div>'
        r'\1',
        body_html,
    )

    # Build a tight, reader-facing TOC.
    # Rules:
    #   - Skip the document title (first h1).
    #   - Narrative (Parts I–VII): include only h2 (Part headings).
    #   - Appendices (h1 starting with "Appendix"): include the H1 only.
    #     Do NOT include the bill's internal Parts/sections in the TOC —
    #     they have their own internal navigation inside each appendix.
    #   - Skip the "At a glance" / "A note" interjections.
    skip_in_toc = {"a note from the drafter", "at a glance"}
    toc_entries = []
    in_appendix = False
    for level, text, slug in headings:
        text_lc = text.lower().strip()
        if level == 1:
            if text_lc.startswith("appendix"):
                toc_entries.append((1, text, slug))
                in_appendix = True
            else:
                # The document title — skip.
                in_appendix = False
            continue
        if in_appendix:
            continue
        if level == 2 and not any(text_lc.startswith(s) for s in skip_in_toc):
            toc_entries.append((2, text, slug))

    toc_html = ['<nav class="toc" aria-label="Table of contents">',
                '<h2>Contents</h2>',
                '<ol>']
    for level, text, slug in toc_entries:
        if level == 1:
            toc_html.append(f'<li class="toc-appendix"><a href="#{slug}">{text}</a></li>')
        else:
            toc_html.append(f'<li class="toc-part"><a href="#{slug}">{text}</a></li>')
    toc_html.append('</ol></nav>')
    toc = "\n".join(toc_html)

    # Inject TOC after the first horizontal rule following the title block.
    parts = body_html.split("<hr />", 1)
    if len(parts) == 2:
        body_html = parts[0] + "<hr />" + toc + parts[1]
    else:
        body_html = toc + body_html

    # Wrap content following each Bill 1/2 appendix H1 with class="bill-text"
    # so we can apply statutory typography (smaller, hanging indents, sans heads).
    # Inject a hidden running-anchor immediately after each appendix H1 to set
    # the running-part string for the page header.
    def wrap_bill_a(match):
        h1_block = match.group(1)
        body = match.group(2)
        anchor = '<span class="running-anchor">Public Integrity Act of Alberta</span>'
        return f'{h1_block}{anchor}<section class="bill-text">{body}</section>'

    def wrap_bill_b(match):
        h1_block = match.group(1)
        body = match.group(2)
        anchor = '<span class="running-anchor">Open Books Act</span>'
        return f'{h1_block}{anchor}<section class="bill-text">{body}</section>'

    body_html = re.sub(
        r'(<h1 [^>]*id="appendix-a[^"]*"[^>]*>.*?</h1>)(.*?)(?=<h1 [^>]*id="appendix-b)',
        wrap_bill_a,
        body_html,
        flags=re.DOTALL,
    )
    body_html = re.sub(
        r'(<h1 [^>]*id="appendix-b[^"]*"[^>]*>.*?</h1>)(.*)$',
        wrap_bill_b,
        body_html,
        flags=re.DOTALL,
    )

    # Promote the "At a glance" table — give it a class and let it own a print page.
    body_html = re.sub(
        r'(<h2[^>]*id="at-a-glance"[^>]*>.*?</h2>)',
        r'<div class="at-a-glance-block">\1',
        body_html,
        flags=re.DOTALL,
    )
    # Close the at-a-glance block before Part I begins
    body_html = re.sub(
        r'(<h2[^>]*id="part-i[^"]*"[^>]*>)',
        r'</div>\1',
        body_html,
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>What Accountable Government Looks Like — Alberta Accountability Bills</title>
<meta name="description" content="A drafted policy package for Alberta — two bills, why they were written, and what they could be worth.">
<meta property="og:title" content="What Accountable Government Looks Like">
<meta property="og:description" content="Two bills, the reasoning behind them, and an honest assessment of what they can't do.">
<meta property="og:type" content="article">
<style>{CSS}</style>
</head>
<body>
<div class="html-cover-shim">{COVER_HTML}</div>
<header class="site-header">
  <div class="wrap">
    <span class="brand">Honest Government &amp; Open Books Acts</span>
    <a href="{REPO_URL}" rel="noopener">View on GitHub →</a>
  </div>
</header>
<main id="top">
{body_html}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p><strong>Released under <a href="{REPO_URL}/blob/main/LICENSE.md" rel="noopener">Creative Commons Attribution-ShareAlike 4.0</a>.</strong> Adapt, improve, table, build on the material — attribution and same-license required.</p>
    <p>Source repository: <a href="{REPO_URL}" rel="noopener">{REPO_URL}</a> · Markdown source: <a href="{REPO_URL}/blob/main/policy-brief.md" rel="noopener">policy-brief.md</a></p>
    <p>Issues, discussions, and pull requests welcome. Critique from legal drafters, constitutional scholars, Indigenous governance leaders, public administration professionals, journalists, and affected public servants is particularly useful.</p>
    <p><a href="#top">↑ Back to top</a></p>
  </div>
</footer>
</body>
</html>
"""
    TARGET.write_text(html, encoding="utf-8")
    print(f"Wrote {TARGET}")
    print(f"Size: {len(html):,} bytes")
    print(f"TOC entries: {len(toc_entries)}")


if __name__ == "__main__":
    build()
