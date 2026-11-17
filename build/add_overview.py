"""Turn 'How to Read This Proposal' into a full contents page (page 2) and shift page refs by +1."""
import re, html

src = open("proposal.html", encoding="utf-8").read()

# 1. remove the old "How to Read" block from Competition Fit
src, n = re.subn(r'<h2>How to Read This Proposal</h2>\s*<table class="plain">.*?</table>\s*', '', src, flags=re.S)
assert n == 1

# 2. shift page cross-references (p.N, pp.N–M, pp.N-M) by +1
def shift(m):
    pre, a, sep, b = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    out = f"{pre}{a+1}"
    if sep:
        out += f"{sep}{int(b)+1}"
    return out
src = re.sub(r'\b(pp?\.)(\d+)(?:(–|-)(\d+))?', shift, src)

# 3. collect titles / subtitles per section (each section = one printed page)
body = src.split("<body>")[1]
sections = re.findall(r'<section[^>]*>(.*?)</section>', body, flags=re.S)
def clean(s): return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()
entries = []
for i, s in enumerate(sections):
    h1 = re.search(r'<h1>(.*?)</h1>', s, re.S)
    h2s = [clean(x) for x in re.findall(r'<h2>(.*?)</h2>', s, re.S)]
    if h1:
        title = clean(h1.group(1))
    else:  # cover page
        title, h2s = h2s[0], h2s[1:]
    if not h2s:
        h2s = [re.sub(r'^Figure \d+\.\s*', '', clean(x)) for x in re.findall(r'<p class="figt">(.*?)</p>', s, re.S)]
    page = i + 1 if i == 0 else i + 2   # overview page is inserted as page 2
    entries.append((page, title, h2s))

groups = [
    ("Introduction", [1, 3]),
    ("Problem and Evidence", [4, 5, 6, 7]),
    ("Market Gap", [8, 9]),
    ("Solution and Pilot", [10, 11, 12, 13, 14]),
    ("Sustainable Impact", [15]),
    ("Market and Business Model", [16, 17, 18, 19, 20, 21]),
    ("Scale, Team and Risks", [22, 23, 24, 25]),
]
byp = {p: (t, h) for p, t, h in entries}
assert sorted(byp) == [p for _, ps in groups for p in ps], sorted(byp)

rows = []
for gi, (gname, pages) in enumerate(groups, 1):
    rows.append(f'<div class="ov-part"><span>Part {gi}</span>{gname}</div>')
    for p in pages:
        t, h = byp[p]
        subs = "".join(f'<li>{html.escape(x)}</li>' for x in h)
        rows.append(f'<div class="ov-item"><div class="ov-t"><b>{html.escape(t)}</b><i></i><em>{p}</em></div>'
                    + (f'<ul>{subs}</ul>' if subs else '') + '</div>')

overview = f'''
<!-- 2 overview -->
<section class="overview">
<h1>Proposal Overview</h1>
<p class="ov-lead">How to read this proposal. Each part answers one question for the jury. Section titles are in bold, subtitles are listed beneath, and the number on the right is the page.</p>
<div class="ov-grid">
{chr(10).join(rows)}
</div>
</section>
'''

css = '''
.overview .ov-lead{color:var(--mut);margin-bottom:8pt}
.ov-grid{column-count:2;column-gap:18pt}
.ov-part{break-after:avoid;break-inside:avoid;font-size:8.6pt;font-weight:700;color:#fff;background:var(--g);padding:2.5pt 6pt;margin:7pt 0 3pt}
.ov-part:first-child{margin-top:0}
.ov-part span{font-weight:400;opacity:.85;margin-right:6pt;font-size:7.6pt;text-transform:uppercase;letter-spacing:.06em}
.ov-item{break-inside:avoid;margin:0 0 3.5pt}
.ov-t{display:flex;align-items:baseline;font-size:8.8pt;line-height:1.3}
.ov-t i{flex:1;border-bottom:1px dotted #9fb1a8;margin:0 4pt;transform:translateY(-2pt)}
.ov-t em{font-style:normal;font-weight:700;color:var(--g)}
.ov-item ul{margin:1pt 0 0;padding-left:10pt;list-style:none}
.ov-item li{font-size:7.7pt;line-height:1.3;color:var(--mut)}
.ov-item li::before{content:"– ";color:var(--g2)}
'''
src = src.replace("</style>", css + "</style>", 1)
src = src.replace("<!-- 2 -->", overview + "\n<!-- 3 -->", 1)
open("proposal.html", "w", encoding="utf-8").write(src)
for e in entries: print(e)
