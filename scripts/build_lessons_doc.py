"""Render docs/lessons/*.md plus the lesson sources into one site, then a PDF.

Layout follows the Rust book: a narrow fixed chapter list on the left, a single
readable column on the right. Each lesson carries its own .rin source inline,
syntax-highlighted, because the code is the lesson -- the prose only frames it.

There is no markdown library here and adding one for twenty files of known
shape is not worth a dependency, so this handles exactly the subset those files
use: headings, blockquotes, fenced and indented code, bullet lists, and inline
`code`, **bold**, *italic* and [links](...).

The PDF comes from headless Chrome, which every Windows box already has.
"""
from __future__ import annotations

import html
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LESSON_DIR = ROOT / "docs" / "lessons"
SOURCE_DIR = ROOT / "src" / "lessons"
OUT_HTML = ROOT / "docs" / "lessons.html"
OUT_PDF = ROOT / "docs" / "lessons.pdf"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

KEYWORDS = {
    "proc", "struct", "enum", "union", "alias", "if", "else", "for", "while",
    "switch", "case", "default", "return", "break", "continue", "import",
    "cinclude", "cast", "sizeof", "alignof", "offsetof", "and", "or", "not",
    "external", "external_emit", "static", "const", "null", "true", "false",
    "align", "defer",
}
TYPES = {
    "i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64", "f32", "f64",
    "b8", "b16", "b32", "b64", "c8", "char", "usize", "uintptr", "intptr",
    "void", "ptrdiff", "intmax", "uintmax", "long",
}
TOKEN = re.compile(
    r'(?P<comment>//[^\n]*|/\*.*?\*/)'
    r'|(?P<string>"(?:[^"\\\n]|\\.)*")'
    r"|(?P<char>'(?:[^'\\\n]|\\.)*')"
    r'|(?P<number>\b\d[\w.]*)'
    r'|(?P<directive>^[ \t]*#[a-z]+)'
    r'|(?P<word>[A-Za-z_]\w*)',
    re.S | re.M)


def highlight(code: str) -> str:
    """Tokenise rin for display. Deliberately shallow -- it colours what a
    reader scans for and never tries to parse."""
    out, last = [], 0
    for m in TOKEN.finditer(code):
        out.append(html.escape(code[last:m.start()]))
        kind = m.lastgroup
        text = html.escape(m.group())
        if kind == "word":
            if m.group() in KEYWORDS:
                out.append('<span class="k">%s</span>' % text)
            elif m.group() in TYPES:
                out.append('<span class="t">%s</span>' % text)
            else:
                out.append(text)
        else:
            cls = {"comment": "c", "string": "s", "char": "s",
                   "number": "n", "directive": "d"}[kind]
            out.append('<span class="%s">%s</span>' % (cls, text))
        last = m.end()
    out.append(html.escape(code[last:]))
    return "".join(out)


def inline(text: str) -> str:
    spans: list[str] = []

    def stash(m: re.Match[str]) -> str:
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = text.replace("--", "\u2014")

    def restore(m: re.Match[str]) -> str:
        return "<code>%s</code>" % html.escape(spans[int(m.group(1))])

    return re.sub(r"\x00(\d+)\x00", restore, text)


def render(md: str) -> str:
    out: list[str] = []
    lines = md.split("\n")
    i = 0
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            close_list()
            i += 1
            body = []
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(body)))
            continue

        if line.startswith("    ") and line.strip():
            close_list()
            body = []
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                body.append(lines[i][4:] if lines[i].startswith("    ") else "")
                i += 1
            while body and not body[-1].strip():
                body.pop()
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(body)))
            continue

        m = re.match(r"^(#{1,4}) (.*)$", line)
        if m:
            close_list()
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2)), level))
            i += 1
            continue

        if line.startswith("|"):
            # A pipe table: header row, a ---|--- separator, then body rows.
            close_list()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body_rows = rows[0], [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]
            cells = "".join("<th>%s</th>" % inline(c) for c in head)
            body_html = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in body_rows)
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (cells, body_html))
            continue

        if line.startswith("> "):
            close_list()
            body = []
            while i < len(lines) and lines[i].startswith("> "):
                body.append(lines[i][2:])
                i += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(body)))
            continue

        if line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>%s</li>" % inline(line[2:]))
            i += 1
            continue

        if line.strip() == "---":
            close_list()
            out.append("<hr>")
            i += 1
            continue

        if not line.strip():
            close_list()
            i += 1
            continue

        close_list()
        body = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,4} |> |- |```|    |---$)", lines[i]):
            body.append(lines[i])
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(body)))

    close_list()
    return "\n".join(out)


CSS = """
/* A committed dark reading ground with one red accent, laid out the way the
   Rust book is: a narrow fixed chapter list, then a single readable column.
   Every colour is painted explicitly so the page holds on any host ground. */
:root {
  --ground:  #12100f;   /* warm near-black, biased toward the accent */
  --rail:    #0d0b0a;
  --ink:     #e6ded9;
  --muted:   #8f817b;
  --dim:     #6b5f5a;
  --accent:  #d93a2b;
  --accent-d:#7d211a;
  --rule:    #2c2421;
  --well:    #0a0807;
  --mono: ui-monospace, "Cascadia Mono", "JetBrains Mono", Consolas, monospace;
  --text: "Charter", "Iowan Old Style", "Source Serif Pro", Georgia, serif;
  --railw: 17rem;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body {
  margin: 0; background: var(--ground); color: var(--ink);
  font: 16px/1.7 var(--text); -webkit-font-smoothing: antialiased;
}

code, pre, .path { text-transform: none; }
table { border-collapse: collapse; margin: 1.1rem 0; font-size: .95rem; width: 100%; }
th, td { text-align: left; padding: .35rem .7rem; border-bottom: 1px solid var(--rule, rgba(127,127,127,.25)); vertical-align: top; }
th { font-weight: 600; }

/* Chapter rail ----------------------------------------------------------- */
.rail {
  position: fixed; inset: 0 auto 0 0; width: var(--railw);
  background: var(--rail); border-right: 1px solid var(--rule);
  overflow-y: auto; padding: 1.6rem 0 3rem;
  display: flex; flex-direction: column; gap: 1.4rem;
}
.rail .brand { padding: 0 1.25rem; display: flex; flex-direction: column; gap: .25rem; }
.rail .brand .name { font-family: var(--mono); font-size: 1.5rem; font-weight: 600;
                     letter-spacing: -.03em; color: var(--ink); text-decoration: none; }
.rail .brand .tag { font-family: var(--mono); font-size: .62rem; letter-spacing: .24em;
                    text-transform: none; color: var(--accent); }
.rail ol { list-style: none; margin: 0; padding: 0 .6rem;
           display: flex; flex-direction: column; gap: 1px; }
.rail a.ch {
  display: flex; gap: .7rem; align-items: baseline;
  padding: .38rem .65rem; border-radius: 3px;
  color: var(--muted); text-decoration: none; font-size: .82rem;
  font-family: var(--text); line-height: 1.35;
}
.rail a.ch .n { font-family: var(--mono); font-size: .7rem; color: var(--dim);
                font-variant-numeric: tabular-nums; min-width: 1.5rem; }
.rail a.ch:hover { color: var(--ink); background: #171312; }
.rail a.ch:hover .n { color: var(--accent); }
.rail a.ch.on { color: var(--ink); background: #1b1615; }
.rail a.ch.on .n { color: var(--accent); }
.rail a.ch:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.rail a.ch.front .n { color: var(--accent-d); }
.rail li.sep { margin: .9rem .65rem .3rem; padding-top: .7rem;
               border-top: 1px solid var(--rule); }
.rail li.sep span { font-family: var(--mono); font-size: .6rem; letter-spacing: .24em;
                    text-transform: none; color: var(--dim); }
section.lesson.front > h1 { border-bottom-color: var(--accent-d); }

/* Reading column --------------------------------------------------------- */
.page { margin-left: var(--railw); }
.col  { max-width: 44rem; margin: 0 auto; padding: 4.5rem 2.5rem 8rem; }

.cover { display: flex; flex-direction: column; gap: 1rem;
         padding-bottom: 2.5rem; margin-bottom: 3rem;
         border-bottom: 1px solid var(--rule); }
.cover h1 { font-family: var(--mono); font-size: clamp(2.6rem, 7vw, 4rem);
            line-height: .95; margin: 0; letter-spacing: -.04em; font-weight: 600; }
.cover .sub { color: var(--muted); font-size: 1.08rem; margin: 0; max-width: 34rem;
              text-wrap: balance; }

section.lesson { scroll-margin-top: 1rem; padding-top: 2rem; margin-bottom: 4.5rem; }
section.lesson > h1 {
  font-family: var(--mono); font-size: 1.5rem; font-weight: 600;
  letter-spacing: -.02em; margin: 0 0 1.2rem; padding-bottom: .7rem;
  border-bottom: 2px solid var(--accent); text-wrap: balance;
}
h2 { font-family: var(--mono); font-size: .68rem; letter-spacing: .22em;
     text-transform: none; color: var(--muted); font-weight: 500;
     margin: 2.3rem 0 .8rem; }
p { margin: 0 0 1.1rem; }
blockquote { margin: 0 0 1.8rem; padding: 0 0 0 1.1rem;
             border-left: 2px solid var(--accent); color: var(--ink); font-size: 1.06rem; }
ul { margin: 0 0 1.2rem; padding-left: 1.2rem;
     display: flex; flex-direction: column; gap: .35rem; }
li::marker { color: var(--accent-d); }
code { font-family: var(--mono); font-size: .86em; background: var(--well);
       color: #f2b9b2; padding: .12em .38em; border-radius: 2px; }
pre { background: var(--well); border: 1px solid var(--rule);
      border-left: 2px solid var(--accent-d); padding: 1rem 1.15rem;
      margin: 0 0 1.5rem; overflow-x: auto; border-radius: 2px; }
pre code { background: none; padding: 0; color: var(--ink);
           font-size: .82rem; line-height: 1.6; }

/* The lesson's own source ------------------------------------------------ */
.source { margin: 0 0 1.6rem; border: 1px solid var(--rule); border-radius: 3px;
          overflow: hidden; background: var(--well); }
.source .bar { display: flex; justify-content: space-between; align-items: center;
               gap: 1rem; padding: .5rem .9rem; background: #151110;
               border-bottom: 1px solid var(--rule); }
.source .path { font-family: var(--mono); font-size: .7rem; color: var(--muted); }
.source .lines { font-family: var(--mono); font-size: .66rem; color: var(--dim);
                 font-variant-numeric: tabular-nums; }
.source pre { border: 0; margin: 0; border-radius: 0; background: none;
              max-height: 34rem; }
.s  { color: #e0a89f; }   /* strings and chars */
.c  { color: #6f625c; font-style: italic; }   /* comments */
.k  { color: #d93a2b; }   /* keywords */
.t  { color: #c98a5e; }   /* built-in types */
.n  { color: #b0a49f; }   /* numbers */
.d  { color: #8f6ad9; }   /* preprocessor directives */

a { color: var(--accent); text-decoration: none;
    border-bottom: 1px solid rgba(217,58,43,.32); }
a:hover { border-bottom-color: var(--accent); }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 2.2rem 0 1.2rem; }
section.lesson em { color: var(--muted); font-size: .92rem; font-style: normal; }

@media (max-width: 60rem) {
  .rail { position: static; width: auto; height: auto; border-right: 0;
          border-bottom: 1px solid var(--rule); }
  .rail ol { display: grid; grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr)); }
  .page { margin-left: 0; }
  .col { padding: 2.5rem 1.25rem 5rem; }
}

/* Phones. A code block scrolls inside its own box, but prose must not: an
   unbreakable token -- a path, a URL, `import "std/Print.rin"` -- is otherwise
   wider than the screen and takes the whole page sideways with it. */
@media (max-width: 34rem) {
  .col { padding: 1.75rem 1rem 4rem; }
  .rail ol { grid-template-columns: 1fr; }
  body { font-size: .97rem; }
  h1 { font-size: 1.7rem; }
  h2 { font-size: 1.28rem; }
  p, li, blockquote { overflow-wrap: break-word; }
  code { overflow-wrap: anywhere; }
  pre { padding: .8rem .85rem; }
  pre code { font-size: .76rem; }
  /* The source header is a two-up row; stacked, it stops pushing the page. */
  .source .bar { flex-wrap: wrap; gap: .2rem .75rem; }
  .source .path { min-width: 0; overflow-wrap: anywhere; }
  .source .lines { flex: 0 0 auto; }
  table { display: block; overflow-x: auto; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { animation: none !important; transition: none !important; }
}

/* Print: no rail, no dark ground -- paper is a different medium. --------- */
@media print {
  body { background: #fff; color: #171310; font-size: 10pt; line-height: 1.5; }
  .rail { display: none; }
  .page { margin-left: 0; }
  .col { max-width: none; padding: 0; }
  .cover { page-break-after: always; border-bottom-color: var(--accent); }
  .cover h1, section.lesson > h1 { color: #171310; }
  section.lesson { page-break-before: always; padding-top: 0; margin-bottom: 0; }
  h2 { color: var(--accent-d); }
  blockquote { color: #4a403c; border-left-color: var(--accent); }
  code { background: #f5efed; color: #7d211a; }
  pre { background: #faf7f6; border-color: #e0d6d2; border-left-color: var(--accent-d); }
  pre code { color: #171310; }
  .source { border-color: #e0d6d2; background: #faf7f6; }
  .source .bar { background: #f2ecea; border-bottom-color: #e0d6d2; }
  .source .path, .source .lines { color: #6b5f5a; }
  .source pre { max-height: none; }
  .s { color: #9b5b2e; } .c { color: #6b5f5a; } .k { color: #a32718; }
  .t { color: #7a4a1e; } .n { color: #444; } .d { color: #5a3f9b; }
  a { color: #7d211a; border: 0; }
  section.lesson em { color: #6b5f5a; }
}
"""

JS = """
// Highlight the chapter you are reading. IntersectionObserver rather than a
// scroll handler so it costs nothing while you are not moving.
(function () {
  var links = {};
  document.querySelectorAll('.rail a.ch').forEach(function (a) {
    links[a.getAttribute('href').slice(1)] = a;
  });
  var current = null;
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var a = links[e.target.id];
      if (!a || a === current) return;
      if (current) current.classList.remove('on');
      a.classList.add('on');
      current = a;
    });
  }, { rootMargin: '-10% 0px -80% 0px' });
  document.querySelectorAll('section.lesson').forEach(function (s) { obs.observe(s); });
})();
"""


def main() -> int:
    files = sorted(LESSON_DIR.glob("*.md"))
    if not files:
        print("no lesson markdown found in %s" % LESSON_DIR)
        return 1

    rail, body, missing = [], [], []

    # Front matter: what the language is, and how to install it. These come
    # before the numbered lessons and carry no source of their own.
    for stem, label in (("intro", "What rin is"), ("install", "Installing")):
        front = ROOT / "docs" / (stem + ".md")
        if not front.exists():
            continue
        rail.append('<li><a class="ch front" href="#%s"><span class="n">·</span>'
                    '<span>%s</span></a></li>' % (stem, html.escape(label)))
        body.append('<section class="lesson front" id="%s">%s</section>'
                    % (stem, render(front.read_text(encoding="utf-8"))))
    if body:
        rail.append('<li class="sep"><span>The lessons</span></li>')

    for f in files:
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^# (\S+) \u2014 (.*)$", text.split("\n")[0])
        num, title = (m.group(1), m.group(2)) if m else (f.stem, f.stem)
        anchor = f.stem
        rail.append(
            '<li><a class="ch" href="#%s"><span class="n">%s</span>'
            '<span>%s</span></a></li>' % (anchor, html.escape(num), html.escape(title)))

        parts = [render(text)]
        src = SOURCE_DIR / (f.stem + ".rin")
        if src.exists():
            code = src.read_text(encoding="utf-8").rstrip("\n")
            parts.append(
                '<h2>The code</h2>'
                '<div class="source"><div class="bar">'
                '<span class="path">src/lessons/%s.rin</span>'
                '<span class="lines">%d lines</span></div>'
                '<pre><code>%s</code></pre></div>'
                % (f.stem, code.count("\n") + 1, highlight(code)))
        else:
            missing.append(f.stem)
        body.append('<section class="lesson" id="%s">%s</section>' % (anchor, "".join(parts)))

    page = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>rin \u2014 the lessons</title><style>%s</style></head><body>'
        '<nav class="rail"><div class="brand">'
        '<a class="name" href="#top">rin</a>'
        '<span class="tag">the lessons</span></div>'
        '<ol>%s</ol></nav>'
        '<div class="page"><div class="col" id="top">'
        '<header class="cover"><h1>rin</h1>'
        '<p class="sub">Twenty programs, read in order. Each one is short, runs, '
        'and teaches exactly one thing about how the machine actually works.</p>'
        '</header>%s</div></div><script>%s</script></body></html>'
    ) % (CSS, "\n".join(rail), "\n".join(body), JS)

    OUT_HTML.write_text(page, encoding="utf-8")
    print("wrote %s (%d lessons, %d KB)" % (OUT_HTML.name, len(files), len(page) // 1024))
    if missing:
        print("  no source found for: %s" % ", ".join(missing))

    chrome = next((c for c in CHROME_CANDIDATES if pathlib.Path(c).exists()), None)
    if not chrome:
        chrome = shutil.which("chrome") or shutil.which("msedge")
    if not chrome:
        print("no Chrome or Edge found; HTML written, PDF skipped")
        return 0

    proc = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         "--print-to-pdf=%s" % OUT_PDF, OUT_HTML.as_uri()],
        capture_output=True, text=True, timeout=180)
    if OUT_PDF.exists():
        print("wrote %s (%d KB)" % (OUT_PDF.name, OUT_PDF.stat().st_size // 1024))
        return 0
    print("PDF generation failed:\n%s" % (proc.stderr or proc.stdout)[:400])
    return 1


if __name__ == "__main__":
    sys.exit(main())
