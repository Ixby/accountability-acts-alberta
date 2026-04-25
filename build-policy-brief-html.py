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
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Source+Serif+4:ital,opsz,wght@1,8..60,400&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --ink: #0a0a0a;
  --ink-soft: #2a2a2a;
  --paper: #faf6ec;
  --paper-deep: #f0e9d6;
  --muted: #4a4a4a;
  --rule: #c9bfa6;
  --accent: #6b1f1f;
  --accent-soft: #8a3a3a;
  --link: #6b1f1f;
  --link-visited: #4a1717;
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

/* ===== Cover page ===== */

.cover {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 12vh 8vw 8vh;
  background: var(--paper);
  border-bottom: 1px solid var(--rule);
}
.cover-eyebrow {
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.78rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--accent);
  font-weight: 500;
  margin-bottom: 2.4rem;
}
.cover-title {
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 700;
  font-size: clamp(2.4rem, 6vw, 4.2rem);
  line-height: 1.05;
  letter-spacing: -0.015em;
  color: var(--ink);
  margin: 0 0 1.6rem;
  max-width: 14ch;
}
.cover-subtitle {
  font-family: "Source Serif 4", Georgia, serif;
  font-style: italic;
  font-size: clamp(1.1rem, 2vw, 1.4rem);
  line-height: 1.4;
  color: var(--ink-soft);
  margin: 0 0 3rem;
  max-width: 36ch;
}
.cover-rule {
  width: 4rem;
  height: 3px;
  background: var(--accent);
  margin: 1.5rem 0 2rem;
  border: none;
}
.cover-meta {
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.92rem;
  color: var(--muted);
  line-height: 1.6;
}
.cover-meta .meta-line {
  display: block;
  margin: 0.3rem 0;
}
.cover-meta .meta-label {
  display: inline-block;
  width: 7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.75rem;
  color: var(--accent);
  font-weight: 500;
}
.cover-foot {
  font-family: "Inter", system-ui, sans-serif;
  font-size: 0.78rem;
  letter-spacing: 0.06em;
  color: var(--muted);
  border-top: 1px solid var(--rule);
  padding-top: 1.2rem;
}
.cover-foot a {
  color: var(--accent);
  text-decoration: none;
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
.toc li { margin: 0.32em 0; }
.toc a {
  color: var(--ink);
  text-decoration: none;
  border-bottom: 1px dotted var(--rule);
  transition: all 0.15s;
}
.toc a:hover {
  color: var(--accent);
  border-bottom-color: var(--accent);
  border-bottom-style: solid;
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
}
@page :first {
  margin: 0;
}

@media print {
  html, body { background: white; }
  body {
    font-size: 11pt;
    line-height: 1.5;
    color: var(--ink);
  }
  .site-header, .site-footer, .heading-anchor, .back-to-top {
    display: none !important;
  }
  main {
    max-width: none;
    padding: 0;
  }
  .cover {
    page-break-after: always;
    min-height: 9.4in;
    border: none;
    background: var(--paper);
    padding: 1.2in 0.9in 0.9in;
  }
  .cover-title { font-size: 38pt; }
  .cover-subtitle { font-size: 14pt; }
  .toc { page-break-after: always; }
  h1 {
    page-break-before: always;
    page-break-after: avoid;
    font-size: 22pt;
    border-bottom-width: 1.5pt;
  }
  h1:first-of-type, .cover + main h1:first-of-type {
    page-break-before: avoid;
  }
  h2 {
    page-break-after: avoid;
    font-size: 14pt;
    margin-top: 1.6em;
  }
  h2::before { width: 1.8em; }
  h3 {
    page-break-after: avoid;
    font-size: 12pt;
  }
  blockquote, table, pre, .display-cost, .pull-quote {
    page-break-inside: avoid;
  }
  a {
    color: var(--ink);
    text-decoration: none;
    border-bottom: none;
  }
  a[href^="http"]:after {
    content: "";
  }
  table th {
    border-top: 1.5pt solid var(--ink);
    border-bottom: 0.75pt solid var(--ink);
    background: transparent;
  }
  table tr:last-child td {
    border-bottom: 1.5pt solid var(--ink);
  }
  .display-cost {
    font-size: 36pt;
  }
  .pull-quote {
    font-size: 14pt;
    border-color: var(--accent);
  }
  blockquote {
    background: transparent;
    border-left-width: 2pt;
  }
}
"""

def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text or "section"


COVER_HTML = f"""<section class="cover" aria-label="Cover">
  <div class="cover-top">
    <div class="cover-eyebrow">A drafted policy package &middot; Alberta &middot; {PUBLICATION_DATE}</div>
    <h1 class="cover-title">What Accountable Government Looks Like</h1>
    <p class="cover-subtitle">A drafted policy package for Alberta &mdash; two bills, why they were written, and what they could be worth.</p>
    <hr class="cover-rule" />
    <div class="cover-meta">
      <span class="meta-line"><span class="meta-label">The package</span> The Honest Government Act &amp; The Open Books Act</span>
      <span class="meta-line"><span class="meta-label">Drafted by</span> a private citizen of Alberta</span>
      <span class="meta-line"><span class="meta-label">Released</span> Creative Commons Attribution-ShareAlike 4.0</span>
      <span class="meta-line"><span class="meta-label">Source</span> <a href="{REPO_URL}">{REPO_URL.replace('https://','')}</a></span>
    </div>
  </div>
  <div class="cover-foot">
    Adapt &middot; Improve &middot; Table &middot; Build on &middot; The bills were drafted to be used.
  </div>
</section>"""


def build():
    md_text = SOURCE.read_text(encoding="utf-8")

    md = markdown.Markdown(
        extensions=["extra", "tables", "sane_lists"],
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

    # Add display treatment to the $200-300 million cost figure in Part I close.
    # Look for the specific paragraph that contains that text.
    body_html = re.sub(
        r"(<p>The combined cost: somewhere between \$200 and \$300 million\.[^<]*</p>)",
        '<div class="display-cost">$200&ndash;300M</div>'
        '<div class="display-cost-label">across three Alberta decisions</div>'
        r'\1',
        body_html,
    )

    # Build hierarchical TOC. Treat the very first h1 (document title) specially.
    toc_entries = headings
    if toc_entries and toc_entries[0][0] == 1:
        toc_entries = toc_entries[1:]

    toc_html = ['<nav class="toc" aria-label="Table of contents">',
                '<h2>Contents</h2>',
                '<ol>']
    current_level = 1
    for level, text, slug in toc_entries:
        eff = 1 if level == 1 else 2
        if eff > current_level:
            toc_html.append('<ol>')
        elif eff < current_level:
            toc_html.append('</ol></li>')
        else:
            if current_level == eff and not toc_html[-1].endswith('<ol>'):
                toc_html.append('</li>')
        toc_html.append(f'<li><a href="#{slug}">{text}</a>')
        current_level = eff
    while current_level > 1:
        toc_html.append('</li></ol>')
        current_level -= 1
    toc_html.append('</li></ol></nav>')
    toc = "\n".join(toc_html)

    # Inject TOC after the first horizontal rule following the title block.
    parts = body_html.split("<hr />", 1)
    if len(parts) == 2:
        body_html = parts[0] + "<hr />" + toc + parts[1]
    else:
        body_html = toc + body_html

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
{COVER_HTML}
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
