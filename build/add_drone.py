"""Add the drone survey (concept) to the proposal: new page 13, cross-references, budget/risk/pilot rows, renumbering."""
import re, shutil, pathlib
P = pathlib.Path("proposal.html"); s = P.read_text(encoding="utf-8")
assert "Product Three: Drone Survey" not in s, "already added"
shutil.copy(P, "proposal_before_drone.html")
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90]); s = s.replace(a, b)

# 1. figures >= 9 shift by one; the new drone figure becomes Figure 9
s = re.sub(r'\bFigure (\d+)\b', lambda m: f"Figure {int(m.group(1)) + (1 if int(m.group(1)) >= 9 else 0)}", s)
s = re.sub(r'Figures 3–5 and 11 use published sector data\..*?after the pilot\.',
           "Figures 3–5 and 12 use published sector data. Figure 6 contains credited reference photographs. Figures 7, 8, 9, 10 and 16 show the software, CAD and drone-survey concepts, including the prototype gallery. Figures 1–2, 11, 13–15 and 17 show team assessments, sample inputs, financial assumptions or plans. Field results will be added after the pilot.", s, flags=re.S)

# 2. pages >= 13 shift by one (text references and overview numbers)
def shift(m):
    pre, a, sep, b = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    f = lambda n: n + 1 if n >= 13 else n
    return f"{pre}{f(a)}" + (f"{sep}{f(int(b))}" if sep else "")
s = re.sub(r'\b(pp?\.)(\d+)(?:(–|-)(\d+))?', shift, s)
s = re.sub(r'<em>(\d+)(?:–(\d+))?</em>', lambda m: "<em>" + "–".join(str(int(x) + 1 if int(x) >= 13 else int(x)) for x in m.groups() if x) + "</em>", s)

# 3. overview entry for the new page
rep('<b>Product Two: KokoShield Field Node (Concept)</b><i></i><em>12</em></div><ul><li>Field Node CAD assembly in exploded view</li></ul></div>',
    '<b>Product Two: KokoShield Field Node (Concept)</b><i></i><em>12</em></div><ul><li>Field Node CAD assembly in exploded view</li></ul></div>'
    '<div class="ov-item"><div class="ov-t"><b>Product Three: Drone Survey (Concept)</b><i></i><em>13</em></div><ul><li>Mapping flight and post-rain flight</li><li>Permission, safety and how we test it</li></ul></div>')

# 4. the new page (written with final page numbers)
DRONE = """<!-- drone -->
<section>
<h1>Product Three: Drone Survey (Concept)</h1>
<p>A small camera drone, borrowed from Universiti Malaya, gives the Field Desk two things from above: an accurate block map at setup, and a quick check for standing water after heavy rain. That check strengthens the “wet or slow-draining block” signal (p.16). The drone does not look for disease: black pod develops on pods hanging under the canopy, which a drone cannot see reliably.</p>
<p class="figt">Figure 9. Drone survey concept: mapping flight and post-rain flight</p>
<figure><div style="display:grid;grid-template-columns:1fr 1fr;gap:8pt"><img src="img/fig_drone_map.png" alt="Mapping flight over the block map"><img src="img/fig_drone_water.png" alt="Post-rain flight showing standing water in blocks A, D and G"></div><figcaption>Left: a back-and-forth flight maps the farm and confirms its eight blocks. Right: after a 48 mm storm, a second flight marks standing water in blocks A, D and G, which the ranked route then puts first. Drawn on the KokoShield app’s map of the demo farm; illustrative, not field data.</figcaption></figure>
<table>
<tr><th style="width:17%">Flight</th><th style="width:24%">When</th><th style="width:27%">What it produces</th><th>How KokoShield uses it</th></tr>
<tr><td>Mapping flight</td><td>Once at setup, with the grower</td><td>An overhead photo mosaic of the farm</td><td>Draw and check block boundaries in the Field Desk map</td></tr>
<tr><td>Post-rain flight</td><td>Within 24 hours of a rain trigger, once it is safe to fly</td><td>Photos showing standing water and slow-draining ground</td><td>Mark wet blocks, alongside the grower’s own observation</td></tr>
</table>
<h2>What the Drone Will Not Do</h2>
<p>It will not detect black pod and it will not spray. Every confirmed case still comes from scouts on foot and adviser review.</p>
<h2>Equipment, Permission and Safety</h2>
<p>The team will borrow a camera drone from Universiti Malaya, flown by a trained team member, so it adds no cash cost to the pilot (p.25). Flights happen only with the grower’s written consent, under current Civil Aviation Authority of Malaysia (CAAM) rules, and never during storms or lightning. Drone photos follow the same data terms as farm maps.</p>
<h2>How We Will Test It</h2>
<p>In each pilot round, the team records whether the drone’s wet-block reading matches the grower’s. If the drone adds no new information after two rounds, the pilot keeps the grower’s observation and drops the extra flight (p.28).</p>
</section>
"""
rep("<!-- gallery -->", DRONE + "<!-- gallery -->")

# 5. cross-references elsewhere
rep("Bubble account integration, physical hardware checks and farm validation remain pending.",
    "A borrowed university camera drone will map the blocks and check for standing water after heavy rain (concept, p.13). Bubble account integration, physical hardware checks and farm validation remain pending.")
rep("An optional sensor-node concept (CAD and demo data) shows how local readings could feed the plan later.",
    "An optional sensor-node concept (CAD and demo data) shows how local readings could feed the plan later, and a borrowed camera drone maps the blocks and shows standing water after heavy rain (p.13).")
rep("<td>Use a grower observation or a mapped rating. Distinguish the two in the record.</td>",
    "<td>Use a grower observation, a mapped rating or a post-rain drone photo of standing water (p.13). Record which source was used.</td>")
rep("<tr><td>Before the round</td><td>Confirm the rain trigger, access and the two block groups. Record the usual route before showing recommendations.</td></tr>",
    "<tr><td>Before the round</td><td>Confirm the rain trigger, access and the two block groups. Record the usual route before showing recommendations.</td></tr>\n"
    "<tr><td>Drone check (optional)</td><td>Within 24 hours of the trigger, where safe and permitted, fly the post-rain survey and note which blocks show standing water. Compare it with the grower’s own reading.</td></tr>")
rep("<tr><td>Contingency</td><td>Extra travel or field materials, for example a fifth round if one is unusable</td><td>180</td></tr>",
    "<tr><td>Contingency</td><td>Extra travel or field materials, for example a fifth round if one is unusable</td><td>180</td></tr>\n"
    "<tr><td>Drone survey</td><td>Camera drone borrowed from Universiti Malaya; batteries charged on campus</td><td>0</td></tr>")
rep("<tr><td>Data privacy concerns</td>",
    "<tr><td>Drone cannot fly</td><td>Use the grower’s own wet-block observation, which the route already supports. Fly only with consent, under current CAAM rules and never in storms.</td><td>Keep the drone optional until it adds information in two rounds.</td></tr>\n<tr><td>Data privacy concerns</td>")
P.write_text(s, encoding="utf-8")
print("drone added;", len(s), "chars")
