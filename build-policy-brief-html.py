"""Build policy-brief.html from policy-brief.md.

Self-contained single-file HTML with:
- Auto-generated table of contents from h1/h2/h3 headings
- Internal anchor links
- Inline CSS for typography and print
- Header and footer linking to the repository
"""

import markdown
import re
from pathlib import Path

REPO_URL = "https://github.com/Ixby/accountability-acts-alberta"
SOURCE = Path(__file__).parent / "policy-brief.md"
TARGET = Path(__file__).parent / "policy-brief.html"

CSS = """
:root {
  --ink: #1a1a1a;
  --paper: #fefefe;
  --muted: #555;
  --rule: #d4d4d4;
  --accent: #1f4068;
  --link: #1f4068;
  --link-visited: #5a3a8a;
  --code-bg: #f4f1eb;
  --quote-bg: #f7f3eb;
  --quote-border: #c9a96e;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
  font-size: 18px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}
.site-header {
  background: var(--ink);
  color: var(--paper);
  padding: 1rem 0;
  border-bottom: 4px solid var(--accent);
}
.site-header .wrap {
  max-width: 880px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.site-header .brand {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  font-size: 0.95rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.site-header a {
  color: var(--paper);
  text-decoration: none;
  border-bottom: 1px dotted rgba(255,255,255,0.5);
}
.site-header a:hover { border-bottom-style: solid; }
main {
  max-width: 880px;
  margin: 0 auto;
  padding: 3rem 1.5rem 4rem;
}
h1, h2, h3, h4 {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  color: var(--ink);
  line-height: 1.25;
  margin: 2.4em 0 0.8em;
  font-weight: 600;
}
h1 {
  font-size: 2.4rem;
  margin-top: 0.4em;
  letter-spacing: -0.01em;
  border-bottom: 3px solid var(--accent);
  padding-bottom: 0.5rem;
}
h2 {
  font-size: 1.7rem;
  border-bottom: 1px solid var(--rule);
  padding-bottom: 0.3rem;
}
h3 { font-size: 1.3rem; }
h4 { font-size: 1.1rem; }
h1 + p em, h2 + p em {
  color: var(--muted);
  font-style: italic;
}
p, ul, ol { margin: 0.8em 0; }
ul, ol { padding-left: 1.6em; }
li { margin: 0.3em 0; }
a {
  color: var(--link);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
}
a:visited { color: var(--link-visited); }
a:hover { text-decoration-thickness: 2px; }
strong { font-weight: 700; }
em { font-style: italic; }
code {
  background: var(--code-bg);
  padding: 0.1em 0.35em;
  border-radius: 3px;
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.9em;
}
pre code { background: none; padding: 0; }
pre {
  background: var(--code-bg);
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 0.9em;
}
blockquote {
  margin: 1.2em 0;
  padding: 0.8em 1.2em;
  background: var(--quote-bg);
  border-left: 4px solid var(--quote-border);
  font-size: 0.97em;
}
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }
hr {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 2.5em 0;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.2em 0;
  font-size: 0.95em;
}
th, td {
  border: 1px solid var(--rule);
  padding: 0.55em 0.8em;
  text-align: left;
  vertical-align: top;
}
th {
  background: var(--code-bg);
  font-weight: 600;
}
.toc {
  background: #fbf9f4;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1.5em 2em;
  margin: 2em 0 3em;
}
.toc h2 {
  margin-top: 0;
  border: none;
  font-size: 1.2rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--muted);
}
.toc ol {
  list-style: none;
  padding-left: 0;
  margin: 0.5em 0;
  counter-reset: toc;
}
.toc ol ol {
  padding-left: 1.5em;
  margin: 0.2em 0 0.4em;
  font-size: 0.95em;
}
.toc li { margin: 0.25em 0; }
.toc a {
  color: var(--ink);
  text-decoration: none;
  border-bottom: 1px dotted var(--rule);
}
.toc a:hover {
  color: var(--link);
  border-bottom-color: var(--link);
}
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
.back-to-top {
  display: inline-block;
  font-size: 0.85em;
  color: var(--muted);
  text-decoration: none;
  margin-top: 0.6em;
}
.back-to-top:hover { color: var(--link); }
.site-footer {
  border-top: 1px solid var(--rule);
  margin-top: 4rem;
  padding: 2rem 0;
  background: #fbf9f4;
  font-size: 0.92em;
  color: var(--muted);
}
.site-footer .wrap {
  max-width: 880px;
  margin: 0 auto;
  padding: 0 1.5rem;
}
.site-footer p { margin: 0.4em 0; }
.site-footer a { color: var(--link); }
@media (max-width: 600px) {
  body { font-size: 17px; }
  main { padding: 2rem 1rem 3rem; }
  h1 { font-size: 2rem; }
  h2 { font-size: 1.45rem; }
  h3 { font-size: 1.2rem; }
  .toc { padding: 1em 1.2em; }
}
@media print {
  .site-header, .site-footer, .heading-anchor, .back-to-top { display: none; }
  body { font-size: 11pt; }
  main { max-width: none; padding: 0; }
  h1, h2, h3 { page-break-after: avoid; }
  blockquote, table, pre { page-break-inside: avoid; }
  a { color: inherit; text-decoration: none; }
  .toc { page-break-after: always; }
}
"""

def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text or "section"


def build():
    md_text = SOURCE.read_text(encoding="utf-8")

    md = markdown.Markdown(
        extensions=["extra", "tables", "sane_lists"],
        output_format="html5",
    )
    body_html = md.convert(md_text)

    # Convert any surviving relative .md links to GitHub absolute URLs.
    # Internal anchors (#...) are left alone.
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

    # Build hierarchical TOC. Treat the very first h1 (document title) specially.
    toc_entries = headings
    if toc_entries and toc_entries[0][0] == 1:
        # Skip the very first heading (the document title)
        toc_entries = toc_entries[1:]

    toc_html = ['<nav class="toc" aria-label="Table of contents">',
                '<h2>Contents</h2>',
                '<ol>']
    current_level = 1
    for level, text, slug in toc_entries:
        # Normalize: collapse to top-of-tree levels 1 and 2
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
    # Close any open lists
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

    # Add "back to top" links after major Part headings.
    body_html = re.sub(
        r'(<h2 id="part-[^"]+"[^>]*>.*?</h2>)',
        r'\1',
        body_html,
        flags=re.DOTALL,
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>What Accountable Government Looks Like — Alberta Accountability Bills Policy Brief</title>
<meta name="description" content="Unified policy brief for the Honest Government Act and Open Books Act — two drafted bills for Alberta with cost analysis, philosophical defence, and adversarial analysis of failure modes.">
<meta property="og:title" content="What Accountable Government Looks Like">
<meta property="og:description" content="Two bills, the reasoning behind them, and an honest assessment of what they can't do.">
<meta property="og:type" content="article">
<style>{CSS}</style>
</head>
<body>
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
