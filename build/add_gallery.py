"""Insert a 2-page Prototype Gallery after the Field Node page; shift pages >=13 by 2, figures >=9 by 1,
and align the starting rain trigger with the prototype (30 mm)."""
import re, shutil
shutil.copy("proposal.html", "proposal_before_gallery.html")
s = open("proposal.html", encoding="utf-8").read()

# rain trigger: match the prototype's 30 mm demo trigger
assert s.count("at least 20 mm in 24 hours") == 1
s = s.replace("at least 20 mm in 24 hours", "at least 30 mm in 24 hours (the threshold used in the prototype)")

# figures >= 9 -> +1
s = re.sub(r'\bFigure (\d+)\b', lambda m: f"Figure {int(m.group(1)) + (1 if int(m.group(1)) >= 9 else 0)}", s)
s = re.sub(r'Figures 3–5 and 10 use published sector data\..*?after the pilot\.',
           "Figures 3–5 and 11 use published sector data. Figure 6 contains credited reference photographs. "
           "Figures 7, 8, 9 and 15 show the software and CAD deliverables, including the prototype gallery. "
           "Figures 1–2, 10, 12–14 and 16 show team assessments, sample inputs, financial assumptions or plans. "
           "Field results will be added after the pilot.", s, flags=re.S)

# pages >= 13 -> +2
def shift(m):
    pre, a, sep, b = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    f = lambda n: n + 2 if n >= 13 else n
    return f"{pre}{f(a)}" + (f"{sep}{f(int(b))}" if sep else "")
s = re.sub(r'\b(pp?\.)(\d+)(?:(–|-)(\d+))?', shift, s)
s = re.sub(r'<em>(\d+)</em>', lambda m: f"<em>{int(m.group(1)) + 2 if int(m.group(1)) >= 13 else m.group(1)}</em>", s)
# also the guide table on the Competition Fit page: "products ... (pp.x)" handled above

# overview entry
entry = ('<div class="ov-item"><div class="ov-t"><b>Prototype Gallery: The Solution in Use</b><i></i><em>13–14</em></div>'
         '<ul><li>Plan, walk and record on a phone</li><li>Review cases in the scout log</li>'
         '<li>Compare routes, handle missing data and use sensor readings</li></ul></div>')
anchor = re.search(r'<div class="ov-item"><div class="ov-t"><b>Product Two: KokoShield Field Node \(Concept\)</b>.*?</ul></div>', s, re.S).group(0)
s = s.replace(anchor, anchor + entry, 1)

gallery = '''
<!-- gallery -->
<section>
<h1>Prototype Gallery: The Solution in Use</h1>
<p>These screens come from the working Field Desk prototype, captured with its built-in demo farm. They follow one post-rain round from start to finish. Maps, readings and cases are demo data, and the scout photo is a reference image. [18]</p>
<div class="steps">
<div><b>1  Plan</b>Rain reading ranks the blocks and sizes the route to 30 minutes.</div>
<div><b>2  Walk</b>The scout follows the route on a phone or a printed checklist.</div>
<div><b>3  Record</b>Each stop logs block, pod count, note and an optional photo.</div>
<div><b>4  Review</b>The grower or adviser confirms or rules out each case.</div>
<div><b>5  Compare</b>Ranked and usual routes are compared in the same time.</div>
</div>
<p class="figt">Figure 9. Prototype gallery (panels A–G)</p>
<div class="gal-row">
<figure class="phone"><img src="img/g_mobile_plan.jpg" alt="Field plan on a phone"><figcaption><b>A. Plan on a phone.</b> 48 mm of rain is above the 30 mm trigger, so the app asks the scout to cover A, G, D and B within 30 minutes.</figcaption></figure>
<figure class="phone"><img src="img/g_mobile_log.jpg" alt="Scout log on a phone"><figcaption><b>B. Record in the field.</b> Each observation shows block, note, pod count, route and time, with its review status.</figcaption></figure>
<figure class="wide"><img src="img/g_print.jpg" alt="Printable route checklist"><figcaption><b>C. Printable route.</b> The same ranked route as a printed checklist with minutes per stop, for use without a signal. Blocks over the time budget and closed blocks are listed as excluded.</figcaption></figure>
</div>
<figure><img src="img/g_scoutlog.jpg" alt="Scout log review on desktop"><figcaption><b>D. Review queue.</b> The adviser confirms two cases and rules out one possible mechanical-damage spot. Only confirmed pods count toward the primary measure (p.17).</figcaption></figure>
</section>

<section>
<h1>Prototype Gallery (continued)</h1>
<figure><img src="img/g_compare.jpg" alt="Route comparison screen"><figcaption><b>E. Compare routes.</b> The ranked and usual routes side by side under the same 30-minute limit, with time to first find and affected blocks missed. These are preset mock findings that demonstrate the method. Pilot results will come from timed field rounds (p.16).</figcaption></figure>
<div class="gal-two">
<figure><img src="img/g_missing.jpg" alt="Missing weather reading warning"><figcaption><b>F. Missing data.</b> With no weather reading, the app does not guess. It disables the priority route and offers the usual round or a sensor sample (p.15).</figcaption></figure>
<figure><img src="img/g_sensor.jpg" alt="Sensor node screen"><figcaption><b>G. Sensor-node input.</b> A demo Field Node reading (air temperature, humidity, rainfall and leaf wetness) can be applied to the field plan. Live device links are future work.</figcaption></figure>
</div>
<div class="callout"><b>What the gallery shows.</b> The full decision loop already runs in a browser on a phone or desktop: trigger, ranked route, field record, review and comparison. The pilot now needs to test it on a real farm with real rain.</div>
</section>
'''
anchor2 = re.search(r'<!-- 10 -->\s*<section>.*?</section>', s, re.S).group(0)
assert "Product Two" in anchor2
s = s.replace(anchor2, anchor2 + gallery, 1)

css = '''
.steps{display:grid;grid-template-columns:repeat(5,1fr);gap:4pt;margin:4pt 0 6pt}
.steps div{background:var(--hd);border-top:3px solid var(--g);padding:4pt 5pt;font-size:7.6pt;line-height:1.3}
.steps b{display:block;color:var(--g);font-size:8.4pt;margin-bottom:1pt}
.gal-row{display:grid;grid-template-columns:24% 24% 1fr;gap:9pt;align-items:start}
.gal-row figure,.gal-two figure{margin:0}
.phone img{border:1px solid var(--line);border-radius:6pt}
.wide img,.gal-two img,figure img.bd{border:1px solid var(--line)}
.gal-two{display:grid;grid-template-columns:1fr 1fr;gap:9pt;margin:6pt 0 8pt}
'''
s = s.replace("</style>", css + "</style>", 1)
open("proposal.html", "w", encoding="utf-8").write(s)
print(sorted(set(re.findall(r'Figure \d+', s)), key=lambda x: int(x.split()[1])))
print(re.findall(r'<em>[^<]*</em>', s))
