#!/usr/bin/env python3
"""Render Shopper_Agent_Connected_Subagent_Architecture.md to a standalone index.html.

Usage: python3 build_html.py   (requires the `markdown` package)
Mermaid diagrams render client-side from the jsDelivr CDN; click any diagram to zoom.
"""
import html
import pathlib
import re

import markdown

HERE = pathlib.Path(__file__).parent
SRC = HERE / "Shopper_Agent_Connected_Subagent_Architecture.md"
OUT = HERE / "index.html"

src = SRC.read_text()
title = re.search(r"^# (.+)$", src, re.M).group(1)

# Pull mermaid blocks out so markdown doesn't mangle them.
blocks = []
def stash(m):
    blocks.append(m.group(1))
    return f"\n\nMERMAIDBLOCK{len(blocks) - 1}\n\n"
src = re.sub(r"```mermaid\n(.*?)```", stash, src, flags=re.S)

# python-markdown needs 4-space indentation for nested lists.
src = re.sub(r"(?m)^ {2,3}(\* )", r"    \1", src)

md = markdown.Markdown(
    extensions=["tables", "fenced_code", "toc", "sane_lists"],
    extension_configs={"toc": {"toc_depth": "2-3"}},
)
body = md.convert(src)
for i, b in enumerate(blocks):
    body = body.replace(
        f"<p>MERMAIDBLOCK{i}</p>",
        f'<figure class="diagram" title="Click to zoom"><pre class="mermaid">{html.escape(b)}</pre>'
        f'<figcaption>Click to zoom</figcaption></figure>',
    )

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--fg:#1d2433;--muted:#5b6475;--bg:#fff;--panel:#f6f8fb;--line:#e2e7ef;--accent:#0b5cab;--code:#f1f4f9}
@media (prefers-color-scheme:dark){:root{--fg:#e6e9ef;--muted:#a3abba;--bg:#14171d;--panel:#1b1f27;--line:#2c323d;--accent:#6cb2ff;--code:#222835}}
*{box-sizing:border-box}
body{margin:0;font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg)}
.layout{display:grid;grid-template-columns:280px minmax(0,1fr);max-width:1400px;margin:0 auto}
nav{position:sticky;top:0;height:100vh;overflow:auto;padding:24px 16px;border-right:1px solid var(--line);background:var(--panel);font-size:13.5px}
nav .toc ul{list-style:none;padding-left:12px;margin:4px 0} nav .toc>ul{padding-left:0}
nav a{color:var(--muted);text-decoration:none} nav a:hover{color:var(--accent)}
nav .toc>ul>li>a{color:var(--fg);font-weight:600}
main{padding:32px 48px 80px;min-width:0}
h1{font-size:28px;line-height:1.25;margin:0 0 16px} h2{margin-top:48px;padding-top:12px;border-top:1px solid var(--line)} h3{margin-top:28px}
hr{display:none}
a{color:var(--accent)}
blockquote{margin:16px 0;padding:10px 16px;background:var(--panel);border-left:4px solid var(--accent);border-radius:4px} blockquote p{margin:6px 0}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:14px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:8px 10px;vertical-align:top;text-align:left} th{background:var(--panel)}
td ul{margin:0;padding-left:18px}
code{background:var(--code);padding:1px 5px;border-radius:4px;font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}
pre{background:var(--code);padding:14px;border-radius:6px;overflow:auto} pre code{padding:0;background:none}
figure.diagram{background:#fff;border:1px solid var(--line);border-radius:8px;padding:16px;margin:16px 0;cursor:zoom-in;overflow-x:auto}
figure.diagram pre.mermaid{background:#fff;margin:0;padding:0;text-align:center}
figure.diagram figcaption{font-size:12px;color:#8a93a3;text-align:right;margin-top:4px}
#zoom{position:fixed;inset:0;background:rgba(10,14,22,.85);display:none;z-index:10;overflow:auto;cursor:zoom-out}
#zoom .inner{background:#fff;margin:24px auto;padding:24px;border-radius:8px;width:max-content;max-width:none}
#zoom svg{max-width:none!important;height:auto}
@media (max-width:900px){.layout{grid-template-columns:1fr} nav{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)} main{padding:24px 18px}}
@media print{nav,#zoom,figcaption{display:none} .layout{display:block}}
</style>
</head>
<body>
<div class="layout">
<nav><strong>Contents</strong>__TOC__</nav>
<main>__BODY__</main>
</div>
<div id="zoom"><div class="inner"></div></div>
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
mermaid.initialize({startOnLoad:false,theme:"default",flowchart:{htmlLabels:true,useMaxWidth:true},sequence:{useMaxWidth:true}});
await mermaid.run();
const zoom = document.getElementById("zoom"), inner = zoom.querySelector(".inner");
document.querySelectorAll("figure.diagram").forEach(fig => fig.addEventListener("click", () => {
  const svg = fig.querySelector("svg").cloneNode(true);
  const vb = svg.viewBox.baseVal;
  svg.removeAttribute("style");
  svg.setAttribute("width", Math.max(vb.width * 1.4, Math.min(window.innerWidth - 96, vb.width * 2)));
  inner.replaceChildren(svg);
  zoom.style.display = "block";
}));
zoom.addEventListener("click", () => { zoom.style.display = "none"; });
document.addEventListener("keydown", e => { if (e.key === "Escape") zoom.style.display = "none"; });
</script>
</body>
</html>
"""

OUT.write_text(
    PAGE.replace("__TITLE__", html.escape(title))
    .replace("__TOC__", md.toc)
    .replace("__BODY__", body)
)
print(f"wrote {OUT} ({len(blocks)} diagrams)")
