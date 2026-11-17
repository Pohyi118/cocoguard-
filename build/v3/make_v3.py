"""KokoShield GSC Ignite proposal v3: product first, ~20 pages, app visual language, real screenshots only.
Writes proposal_v3.html next to this file. Print with Edge (see print_v3.ps1 / build steps in README)."""
import pathlib, html
from charts import hbars, vbars, contribution, heat, gantt, BR, BRD, TINT, INK, INK2, INK3, LINE, HI, MID, LO, RAIN, SOFT
HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
PH = (ROOT / "video/v5/photos").as_uri() + "/"
SH = "shots/"
FONT = (HERE / "plexfont.css").read_text(encoding="utf-8")
AERIAL = (ROOT / "prototype/assets/farm_aerial.jpg").as_uri()
CAD = (ROOT / "build/kit/KokoShield_Field_Node_Exploded.png").as_uri()

PAGES = []
def page(body, cls="", header=True):
    PAGES.append((body, cls, header))

def fig(src, cap, style="", cls=""):
    return f'<figure class="{cls}" style="{style}"><img src="{src}" alt=""><figcaption>{cap}</figcaption></figure>'

def table(head, rows, cls="", widths=None):
    cg = "".join(f'<col style="width:{w}">' for w in widths) if widths else ""
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><colgroup>{cg}</colgroup><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

def laptop(src, w="150mm"):
    return f'<div class="laptop" style="width:{w}"><div class="lscreen"><img src="{src}" alt=""></div><div class="lbase"></div></div>'

def phone(src, w="46mm", extra=""):
    return f'<div class="phone" style="width:{w};{extra}"><div class="pscreen"><img src="{src}" alt=""></div></div>'

# ---------------- block geometry from the prototype (map units 650 x 357) ----------------
POLY = {"A": "68,57 191,39 215,105 181,150 66,142", "B": "209,38 362,34 367,133 286,151 232,125", "C": "382,40 534,64 558,135 474,160 385,127",
        "D": "64,159 181,169 217,236 173,272 80,248 51,216", "E": "221,154 287,170 368,151 391,236 319,273 244,250", "F": "390,145 474,176 562,152 595,221 550,273 416,255",
        "G": "99,267 178,291 222,260 276,292 267,334 121,333", "H": "283,290 322,286 405,263 547,291 503,333 291,335"}
LBL = {"A": (137, 73), "B": (308, 73), "C": (462, 98), "D": (113, 205), "E": (307, 205), "F": (491, 214), "G": (185, 320), "H": (387, 308)}

def drone_svg():
    water = {"A": [(118, 104, 34, 18), (160, 70, 20, 12)], "D": [(118, 222, 40, 20), (158, 245, 18, 10)], "G": [(150, 312, 36, 14), (222, 302, 22, 10)]}
    sweep = [(40, 42), (610, 42), (610, 130), (40, 130), (40, 218), (610, 218), (610, 306), (40, 306)]
    s = ['<svg viewBox="0 0 650 357" width="100%" role="img" style="display:block;border-radius:6px">',
         f'<defs>{"".join(f"<clipPath id=dc{k}><polygon points=\"{p}\"/></clipPath>" for k, p in POLY.items())}</defs>',
         f'<image href="{AERIAL}" x="-40" y="-188" width="1100" height="733" preserveAspectRatio="none"/><rect x="0" y="0" width="650" height="357" fill="rgba(10,30,20,.18)"/>']
    for k, p in POLY.items():
        s.append(f'<polygon points="{p}" fill="none" stroke="#fff" stroke-opacity=".85" stroke-width="2" stroke-linejoin="round"/>')
        s.append(f'<text x="{LBL[k][0]}" y="{LBL[k][1]}" font-size="17" font-weight="700" fill="#fff" text-anchor="middle" style="paint-order:stroke" stroke="rgba(0,0,0,.5)" stroke-width="3">{k}</text>')
    s.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in sweep)}" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="7 6" opacity=".8"/>')
    for k, bl in water.items():
        s.append(f'<g clip-path="url(#dc{k})">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#7fc4ef" fill-opacity=".85" stroke="#fff" stroke-width="1.2"/>' for x, y, rx, ry in bl) + "</g>")
    for k in "ADG":
        x, y = water[k][0][0], water[k][0][1] - 34
        s.append(f'<rect x="{x - 52}" y="{y - 13}" width="104" height="20" rx="5" fill="{RAIN}"/><text x="{x}" y="{y + 1.5}" font-size="11.5" font-weight="700" fill="#fff" text-anchor="middle">Standing water</text>')
    return "".join(s) + "</svg>"

def system_svg():
    """Plan, Walk, Prove inside the Field Desk; optional inputs feed Plan; confirmed cases feed back."""
    W, H = 760, 330
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" style="display:block">',
         f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BR}"/></marker>'
         f'<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{INK3}"/></marker></defs>']
    # inputs
    ins = [("Rain reading (required)", "Public gauge or the", "grower's own gauge", True), ("Field Node (optional)", "Temperature and humidity,", "CAD concept", False), ("Drone survey (optional)", "Standing water after rain,", "borrowed drone", False)]
    for i, (a, b, c, req) in enumerate(ins):
        x = 14 + i * 178
        dash = 'stroke-dasharray="5 4"' if not req else ""
        s.append(f'<rect x="{x}" y="6" width="170" height="60" rx="7" fill="{"#fff" if req else "#F3F4F1"}" stroke="{BR if req else LINE}" stroke-width="{1.6 if req else 1.2}" {dash}/>')
        s.append(f'<text x="{x + 12}" y="25" font-size="12.5" font-weight="700" fill="{INK}">{a}</text><text x="{x + 12}" y="42" font-size="10.5" fill="{INK2}">{b}</text><text x="{x + 12}" y="56" font-size="10.5" fill="{INK2}">{c}</text>')
        dash2 = 'stroke-dasharray="4 4"' if not req else ""
        s.append(f'<path d="M{x + 85} 66 C {x + 85} 88, 130 82, 130 104" fill="none" stroke="{BR if req else INK3}" stroke-width="1.6" {dash2} marker-end="url(#{"ah" if req else "ag"})"/>')
    # Field Desk container
    s.append(f'<rect x="6" y="108" width="{W - 12}" height="168" rx="12" fill="{TINT}" stroke="{BR}" stroke-width="1.4"/>')
    s.append(f'<text x="22" y="130" font-size="12" font-weight="700" fill="{BRD}" letter-spacing=".06em">KOKOSHIELD FIELD DESK (THE CORE WEB APP)</text>')
    steps = [("1", "Plan", ["Rain over the trigger ranks", "every block and builds a route", "that fits the time budget."]),
             ("2", "Walk", ["The scout follows one stop", "at a time on a phone and logs", "suspect pods, even offline."]),
             ("3", "Prove", ["The adviser confirms or rules", "out each case. Compare counts", "confirmed pods per scouting hour."])]
    for i, (n, t, lines) in enumerate(steps):
        x = 22 + i * 248
        s.append(f'<rect x="{x}" y="142" width="222" height="120" rx="9" fill="#fff" stroke="{LINE}"/>')
        s.append(f'<circle cx="{x + 24}" cy="168" r="13" fill="{BR}"/><text x="{x + 24}" y="172.5" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">{n}</text>')
        s.append(f'<text x="{x + 46}" y="174" font-size="19" font-weight="700" fill="{INK}">{t}</text>')
        for j, l in enumerate(lines): s.append(f'<text x="{x + 16}" y="{204 + j * 17}" font-size="12" fill="{INK2}">{l}</text>')
        if i < 2: s.append(f'<path d="M{x + 224} 202 L{x + 246} 202" stroke="{BR}" stroke-width="2" marker-end="url(#ah)"/>')
    # feedback loop and output
    s.append(f'<path d="M630 276 C 630 312, 130 312, 130 280" fill="none" stroke="{BR}" stroke-width="1.6" marker-end="url(#ah)"/>')
    s.append(f'<rect x="250" y="296" width="262" height="24" rx="6" fill="#fff" stroke="{LINE}"/><text x="381" y="312" font-size="11" fill="{INK2}" text-anchor="middle">Confirmed cases become "Confirmed before" next time</text>')
    s.append(f'<path d="M653 108 L653 70" stroke="{BR}" stroke-width="1.6" marker-end="url(#ah)"/>')
    s.append(f'<rect x="560" y="6" width="186" height="60" rx="7" fill="#fff" stroke="{BR}" stroke-width="1.4"/><text x="572" y="25" font-size="12.5" font-weight="700" fill="{INK}">Coverage report</text><text x="572" y="42" font-size="10.5" fill="{INK2}">CSV export for a</text><text x="572" y="56" font-size="10.5" fill="{INK2}">cooperative or buyer</text>')
    return "".join(s) + "</svg>"

def position_svg():
    W, H = 330, 236; L, T, PW, PH_ = 40, 10, 276, 186
    pts = [("Usual round and paper log", .12, .30, False, "r"), ("Spreadsheet records", .22, .14, False, "r"), ("Forecast models", .86, .22, False, "u"),
           ("Plantix", .18, .52, False, "r"), ("PlantwisePlus", .40, .40, False, "r"), ("KokoShield (designed)", .84, .84, True, "l")]
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img">', f'<rect x="{L}" y="{T}" width="{PW}" height="{PH_}" fill="#FAFBF9" stroke="{LINE}"/>',
         f'<line x1="{L + PW / 2}" y1="{T}" x2="{L + PW / 2}" y2="{T + PH_}" stroke="{LINE}" stroke-dasharray="3 3"/><line x1="{L}" y1="{T + PH_ / 2}" x2="{L + PW}" y2="{T + PH_ / 2}" stroke="{LINE}" stroke-dasharray="3 3"/>']
    for lab, x, y, me, side in pts:
        cx, cy = L + PW * x, T + PH_ * (1 - y)
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{7 if me else 5}" fill="{BR if me else SOFT}" stroke="#fff" stroke-width="1.5"/>')
        anchor = {"r": "start", "l": "end", "u": "middle"}[side]; dx = {"r": 10, "l": -10, "u": 0}[side]; dy = -10 if side == "u" else 4
        s.append(f'<text x="{cx + dx:.1f}" y="{cy + dy:.1f}" font-size="{10.5 if me else 10}" font-weight="{700 if me else 400}" fill="{INK if me else INK2}" text-anchor="{anchor}">{lab}</text>')
    s.append(f'<text x="{L + PW / 2}" y="{H - 14}" font-size="10" fill="{INK3}" text-anchor="middle">Uses the weather to decide when to scout</text>')
    s.append(f'<text transform="translate(14 {T + PH_ / 2}) rotate(-90)" font-size="10" fill="{INK3}" text-anchor="middle">Plans where to walk, block by block</text>')
    return "".join(s) + "</svg>"

# =====================================================================================
# 1 Cover
page(f'''<div class="cover-photo" style="background-image:url('{PH}15_farmer.jpg')"><div class="cover-cap">Cocoa farmer David Kebu Jnr and his son Snider, Solomon Islands. Photo: Irene Scott for AusAID, CC BY 2.0 [27]. Not the pilot farm.</div></div>
<div class="cover-body">
  <div class="kicker">Global Sustainability Challenge 2026-27, Ignite</div>
  <h1 class="cover-title">KokoShield</h1>
  <div class="cover-sub">Weather-guided black pod scouting for smallholder cocoa farms</div>
  <div class="cover-meta"><div><b>Track</b>Adaptation and Resilience, Food Resilience</div><div><b>Team</b>Leow Shen En, Chong Pohyi, Choong Zhuo Lin, Lee Jia Shern and Teoh Xi Xian</div><div><b>University</b>Universiti Malaya, Malaysia</div></div>
</div>''', "cover", header=False)

# 2 Executive summary
page(f'''<h1>Executive summary</h1>
<p class="lead">KokoShield Field Desk is a working web app that tells a cocoa scout where to look first after heavy rain. It turns a rain reading into a ranked 30-minute route through the farm's blocks, guides the scout stop by stop on a phone, and lets an agricultural adviser confirm what was found.</p>
<p>Black pod is a rain-driven disease estimated to cost 20 to 30% of world cocoa production each year [25]. After a storm a smallholder has a short window and many blocks, and the usual round often reaches the wettest blocks late. Field Desk replaces that guess with a plan: score each block on slow drainage and previous confirmed cases, choose the highest-risk blocks that fit the time available, and walk them as the shortest loop from the gate.</p>
<p>We will test one question on a Malaysian cocoa farm: in the same 30 minutes, does the ranked route find more <b>confirmed pods per scouting hour</b> than the grower's usual round? Two scouts walk matched groups of blocks after each qualifying rain, and a common follow-up check counts what each route missed.</p>
<div class="cards">
  <div class="card"><b>What we built</b>Field Desk with five screens: Field plan, Walk, Scout log, Compare and Sensor node. A cocoa profile and a rice-blast profile. Page 3.</div>
  <div class="card"><b>First deployment</b>One cocoa farm in Selangor, four usable paired rounds over about six weeks from February 2027. Page 10.</div>
  <div class="card ask"><b>The ask</b>RM1,200 cash for the one-farm pilot, plus access to one farm and one agricultural adviser. Page 19.</div>
  <div class="card"><b>Sustainable impact</b>Fewer pods lost, treatment aimed at affected blocks instead of the whole farm, and a planned response to extreme rain. SDG 2.3, 2.4 and 13.1. Page 12.</div>
  <div class="card"><b>Business model</b>Free for growers. A cooperative or buyer pays RM75 per active farm per season for a cluster of about 20 farms. Page 16.</div>
  <div class="card"><b>Go-to-market</b>One farm, then a paid 20-farm cluster in Sabah or Sarawak (2027), then three clusters (2028), each behind a go or no-go gate. Page 17.</div>
</div>
<div class="band"><img src="{PH}16_farmer.jpg" alt=""><div><h2>Who it is for</h2><p><b>The grower or a farm scout</b> walks the route on a phone. <b>An agricultural adviser</b> confirms what was found. <b>A cooperative or buyer</b> sponsors a cluster of farms and receives the coverage record.</p><p class="small">Cocoa farmer Flora Kebu, Solomon Islands. Photo: Irene Scott for AusAID, CC BY 2.0 [30]. Not the pilot farm.</p></div></div>
<p class="note">What is built, tested and still pending is listed once, on page 4. The rest of this proposal is written on that basis.</p>''')

# 3 The system in one picture
page(f'''<h1>One system: Plan, Walk, Prove</h1>
<p class="lead">KokoShield is one system, not three products. The Field Desk web app is the core. A rain reading is the only required input. The Field Node and a borrowed drone are optional inputs that can sharpen the plan later.</p>
<div class="hero">{laptop(SH + "desk_plan.jpg", "142mm")}{phone(SH + "phone_walk.jpg", "40mm", "position:absolute;right:2mm;bottom:0")}</div>
<p class="figcap">Figure 1. Field Desk on a laptop (Field plan) and a phone (Walk), real screenshots of the prototype. The farm, its aerial view (AI-generated) and the 48 mm reading are demo data.</p>
<div class="sysfig">{system_svg()}</div>
<p class="figcap">Figure 2. How the parts fit. Solid lines are required; dashed inputs are optional and not needed for the pilot.</p>''')

# 4 Status
page(f'''<h1>What is built, tested and pending</h1>
<p class="lead">This is the one place where we list what exists today and what does not. Everything after this page describes the system as designed, and the pilot tests it.</p>
{table(["Component", "Built", "Tested", "Pending"], [
  ["<b>Field Desk web app</b>", "Single-file browser app with Field plan, Walk, Scout log, Compare and Sensor node screens. Cocoa (Malaysia) and rice (China) profiles. CSV export.", "Desktop and phone browsers with demo data. Records save in the browser when offline.", "Use on a real farm. A hosted link for pilot users."],
  ["<b>Ranking and route rule</b>", "Block scores for Slow drainage and Confirmed before, a time-budget fit and the shortest loop from the gate along the footpaths.", "On the demo farm and the rice demo paddy.", "Weights agreed with the grower and adviser, then frozen before the first scored round."],
  ["<b>Bahasa Malaysia</b>", "An English and Bahasa Malaysia switch on the Walk screen.", "Not yet.", "Wording checked by a native speaker before any field use."],
  ["<b>Field Node</b>", "CAD model (STEP, STL, GLB) and the app's Sensor node page with a demo feed.", "Fit checked in CAD only.", "A 3D print, electronics, a power design and outdoor testing. It measures temperature and humidity only."],
  ["<b>Drone survey</b>", "Flight plan and how the Field Desk uses it.", "Not yet.", "Borrowing the Universiti Malaya drone, CAAM rules check, grower consent."],
  ["<b>Pilot</b>", "Protocol, measures, decision rule and RM1,200 budget.", "Not yet.", "Signed site (Tanjung Sepat is the candidate) and one agricultural adviser."],
  ["<b>Business model</b>", "Pricing, unit economics and phased plan.", "Not yet.", "Sponsor interviews and a paid cluster trial."],
], "status", ["17%", "31%", "22%", "30%"])}
<h2>How the figures are labelled</h2>
<div class="twocol small">
<p><b>Demo data.</b> The Tanjung Sepat demo farm, its eight blocks, the 48 mm reading, the seeded Scout log records and the Compare screen's preset finds all come from the prototype. Each figure says so once in its caption.</p>
<p><b>Illustrative images.</b> The aerial view of the demo farm is AI-generated. Stock photographs carry a country and a credit and never show the pilot farm. Charts on the market and economics pages use published data or our stated assumptions.</p>
</div>''')

# 5 The problem
page(f'''<h1>The problem: the right block, too late</h1>
<div class="probgrid">
<div>
<p class="lead">Black pod, caused mainly by <i>Phytophthora palmivora</i>, spreads from infected pods to healthy ones by rain splash [9, 25]. After heavy rain the useful action is simple: find and remove infected pods quickly. The hard part is knowing where to look first.</p>
<p>A smallholder or a single scout has a short window and limited labour. Without a plan, the walk follows memory and habit, so wet, slow-draining blocks with a history of disease may be reached last or not at all. Advisers cannot visit every farm after every storm. Existing tools forecast weather, identify symptoms or keep records, but none turns "it rained heavily" into "walk these blocks first, in this order, in the time you have", or shows whether that advice worked.</p>
<div class="stats">
  <div><span>20-30%</span>of world cocoa production estimated lost to black pod each year [25]</div>
  <div><span>86%</span>of Malaysia's 6,580 ha of cocoa is smallholdings (2025) [2]</div>
  <div><span>3 countries</span>where heavy wet-season rain is linked to lower cocoa yield: Ghana, Ecuador and Indonesia [3]</div>
</div>
</div>
{fig(PH + "13_black_pod.jpg", "Figure 3. Black pod rot on cacao pods. Reference photograph, location not recorded. Scot Nelson, CC0 [18].", "", "probphoto")}
</div>
{table(["Evidence", "What it found", "What it changes in KokoShield"], [
  ["Guest, 2007 [25]", "Estimated annual losses of 20-30% of global production, spread by rain splash.", "Prompt detection and removal after rain is the action to support."],
  ["Malaysian review [4]", "Severity rises under wetter, more humid conditions.", "Rate drainage at block level and ask where moisture lingers."],
  ["Ling et al., 2019 [5]", "A weekly model with weather inputs beat one based on disease history alone.", "Combine rain with field history, and show the reason for each stop."],
  ["Albright et al., 2026 [3]", "In a Ghana model, excess wet-season rain and dry-season drought explain 68% of year-to-year yield variation.", "Use rain as the trigger, and measure scouting before claiming yield effects."],
], "", ["20%", "42%", "38%"])}
<p class="note">The 20-30% figure describes the size of the problem, not the share KokoShield can recover. A confirmed pod is an operational finding; a later harvest check is needed to judge marketable pods saved.</p>''')

# 6 Plan
page(f'''<div class="steplabel">Step 1</div><h1>Plan: a route that fits the time you have</h1>
{laptop(SH + "desk_plan.jpg", "176mm")}
<p class="figcap">Figure 4. Field plan after 48 mm of rain on the demo farm (demo data; aerial view AI-generated). The route is A North terraces, D Lower grove, B East rows and G South rows: 4 stops, 30 of 30 min, back to gate.</p>
<div class="twocol">
<div><h2>How the route is built</h2>
<ol class="steps">
<li><b>Trigger.</b> A round is suggested when the nearest public gauge [8] or the grower's own gauge records at least 30 mm in 24 hours.</li>
<li><b>Score.</b> Each open block earns 3 points for Slow drainage when the trigger is met and 2 points for Confirmed before. Blocks show as Priority, Watch, Routine or Closed.</li>
<li><b>Fit.</b> Pick the highest-risk blocks whose scouting times fit the budget (15, 20, 30 or 45 minutes).</li>
<li><b>Order.</b> Walk the chosen blocks as the shortest loop from the gate along the farm's footpaths, and come back to the gate.</li>
</ol></div>
<div><h2>What the scout sees</h2>
<p>Each stop shows its reason, such as "Slow drainage" and "Confirmed before", so the grower can check the logic. Blocks left out are listed as "Not this round", and closed blocks are excluded rather than scored as zero.</p>
<p>If the rain reading is missing, the app does not guess. It disables the priority route and offers the usual round. The route can be printed as a checklist for a walk without signal.</p>
<p class="small">Before the pilot, the grower and adviser agree the trigger and weights, then freeze them for every scored round.</p></div>
</div>''')

# 7 Walk
page(f'''<div class="steplabel">Step 2</div><h1>Walk: one stop at a time, on a phone</h1>
<p class="lead">The Walk screen is built for the field: one block per screen, large buttons, a running clock and a short note on what to check. Every save is stored on the phone first, so a weak signal does not lose a record.</p>
<div class="phones">{phone(SH + "phone_walk.jpg", "52mm")}{phone(SH + "phone_count.jpg", "52mm")}{phone(SH + "phone_next.jpg", "52mm")}</div>
<div class="phonecaps"><p><b>Stop 1 of 4.</b> Block A, North terraces, with its reasons and what to check: lower pods and trunk base.</p><p><b>Found black pod.</b> The scout enters how many pods, here 3, and saves.</p><p><b>Next stop.</b> The record is saved for review and the scout moves to block D, Lower grove.</p></div>
<p class="figcap">Figure 5. The Walk screen on a phone, real screenshots of the prototype with demo data.</p>
<div class="twocol">
<div><h2>What each record holds</h2>
<p>Block, time, the route that led there, the suspected pod count and an optional note or photo. Each record starts as Pending, so a field observation stays separate from a confirmed finding.</p></div>
<div><h2>Language and access</h2>
<p>The Walk screen has an English and Bahasa Malaysia switch; its wording will be checked by a native speaker before field use. The app runs in a phone browser, with no app store install, and a printed route is the fallback.</p></div>
</div>''')

# 8 Prove
page(f'''<div class="steplabel">Step 3</div><h1>Prove: confirm cases and count what was found</h1>
<div class="provegrid">
{laptop(SH + "desk_log.jpg", "100%")}
<div><h2>Scout log</h2><p>The grower or adviser confirms or rules out each pending case, using one standard for both routes. Only confirmed pods count toward the primary measure. Ruled-out records, such as squirrel damage, stay visible.</p><p class="small">Figure 6. Scout log with seeded demo records and reference photos.</p></div>
</div>
<div class="provegrid">
{laptop(SH + "desk_compare.jpg", "100%")}
<div><h2>Compare</h2><p>Compare puts the priority route and the usual round side by side under the same time limit: pods per scouting hour, pods found, time to first find and blocks with disease missed.</p><p>On the demo farm the screen shows 14 against 4 pods per scouting hour. These are <b>preset finds that demonstrate the method</b>; pilot numbers will come from timed field rounds.</p><p class="small">Figure 7. Compare screen, demo farm with preset finds.</p></div>
</div>
<p class="note">The Scout log exports a dated CSV. The same file gives a cooperative or buyer a coverage record for every farm in a cluster.</p>''')

# 9 Optional inputs
page(f'''<h1>Optional inputs: the Field Node and a drone survey</h1>
<p class="lead">Neither input is needed for the pilot. Each can add a better signal to the Plan step once it proves it adds information.</p>
<div class="twocol wide">
<div>
<h2>Field Node (CAD concept)</h2>
<img class="framed" src="{SH}desk_sensor_crop.jpg" alt="">
<p class="small">Figure 8. The Sensor node page of the prototype, showing the CAD model exploded and a demo feed.</p>
<p>A small enclosure for an air temperature and humidity sensor at block level: an 86 x 62 x 32 mm base, a removable lid and a vented sensor hood, with an ESP32-class controller as a size envelope.</p>
<p><b>At its true level:</b> it is a CAD design. It measures temperature and humidity only; rainfall needs a separate gauge, and leaf wetness its own sensor or a field record. Power, mounting and outdoor testing are not designed yet. A photo of a 3D print will replace the render once printed. CAD files are attached to this PDF.</p>
</div>
<div>
<h2>Drone survey (borrowed)</h2>
<div class="framed">{drone_svg()}</div>
<p class="small">Figure 9. Illustrative post-rain flight drawn on the prototype's AI-generated aerial view of the demo farm. Not field data.</p>
<p>A camera drone borrowed from Universiti Malaya maps the blocks once at setup, then flies within 24 hours of a rain trigger, when safe, to mark standing water. That strengthens the Slow drainage signal, here in blocks A, D and G.</p>
<p><b>What it will not do:</b> detect black pod, which develops on pods under the canopy, or spray. Flights need the grower's written consent and follow current CAAM rules, never in storms. If the drone adds nothing new after two rounds, the pilot drops it and keeps the grower's own observation.</p>
</div>
</div>''')

# 10 Pilot
page(f'''<h1>The pilot: one farm, two routes, same 30 minutes</h1>
<div class="pilotgrid">
<div class="keynums">
  <div><span>1</span>Malaysian cocoa farm, Selangor</div><div><span>8-12</span>blocks in two matched groups</div><div><span>2</span>scouts, 30 minutes each</div>
  <div><span>4</span>usable paired rounds</div><div><span>6</span>weeks, subject to rain</div><div><span>RM1,200</span>cash budget</div>
</div>
<div>
<p class="lead">The design compares the order in which scouts walk, within the same time budget. Nothing else changes.</p>
<p>The grower's scouted area is divided into 8 to 12 blocks of similar size, split into two groups matched on size, drainage and past cases. Each group holds more blocks than one scout can cover in 30 minutes, so the order of visits matters. In each round one scout follows the KokoShield order in one group and the other follows the grower's usual order in the other. Groups and scouts swap every round.</p>
</div>
</div>
{table(["Stage", "Protocol"], [
  ["Before the round", "Confirm the 30 mm trigger, access and the two groups. Record the usual route before showing any recommendation."],
  ["Drone check (optional)", "Within 24 hours, where safe and permitted, note blocks with standing water and compare with the grower's reading."],
  ["Two timed routes", "Both scouts start together and work 30 minutes each. Walking and recording count toward the time. The first assignment is random."],
  ["Confirmation", "One agreed review standard. Where practical, the reviewer does not see which route produced each case."],
  ["Follow-up check", "On the same visit, the same systematic check of every eligible block in both groups counts the cases each route missed."],
], "", ["24%", "76%"])}
<div class="twocol">
<div><h2>When a round is usable</h2><p>Both timed walks, eligible blocks, timestamps and the follow-up result are recorded. Rounds with zero cases are kept. If too few rain events occur, we report usability and data coverage and extend the test before claiming performance.</p></div>
<div><h2>Site and data</h2><p>Tanjung Sepat, about 1.5 hours from Universiti Malaya, is the candidate site; a farm there is listed by the Kuala Langat council [7], and access is not yet confirmed. The grower owns the record. Maps and photos are shared only with trial participants.</p></div>
</div>
<div class="band low"><img src="{PH}14_farmer.jpg" alt=""><div><h2>What scouts look for</h2><p>Lower pods and the trunk base, for dark, spreading patches: the same check the Walk screen shows at every stop. Each suspect pod is counted once, tagged to its block and confirmed or ruled out by the adviser.</p><p class="small">Pruning a cocoa tree in Deli Serdang, North Sumatra, Indonesia. Photo: USAID Indonesia, public domain [29]. Not the pilot farm.</p></div></div>''')

# 11 Measures
page(f'''<h1>How we will measure it</h1>
<p class="lead">The primary outcome is <b>confirmed pods per scouting hour</b>: newly confirmed diseased pods divided by recorded scouting hours. Speed and misses are measured too, so a route cannot look good by visiting a few obvious blocks.</p>
{table(["Measure", "Calculation", "Why it matters"], [
  ["<b>Confirmed pods per scouting hour</b> (primary)", "Newly confirmed pods divided by recorded scouting hours, by round and in total.", "The direct test of the route."],
  ["First detection", "Minutes to the first observation later confirmed.", "Earlier removal limits rain-splash spread."],
  ["Missed cases", "Cases first found on the common follow-up check, by block.", "Stops a route winning by concentrating."],
  ["Response time", "Hours from trigger to round; days from confirmation to pod removal.", "The climate-adaptation link."],
  ["Usability", "Route completion, grower overrides and willingness to rerun.", "Adoption beyond the pilot."],
  ["Harvest observation", "Marketable pods as a share of pods assessed, where harvest overlaps.", "Exploratory at one site."],
], "", ["30%", "44%", "26%"])}
<div class="decision"><h2>Decision rule for a second site</h2>
<p>We go on to a second site only when all three hold:</p>
<ol><li>the ranked route records more confirmed pods per scouting hour in at least 3 of 4 usable rounds (or 75% of usable rounds if the trial is extended);</li>
<li>the follow-up check finds no block missed by the ranked route in two or more rounds; and</li>
<li>the grower says they would use it again.</li></ol></div>
<h2>How we will report</h2>
<p>Every paired round with its conditions and the cases verified later, and a count of rounds with improvement, no clear difference and lower performance. One farm can guide a second pilot; a harvest or income claim needs more farms and seasons.</p>''')

# 12 Impact
page(f'''<h1>Sustainable impact</h1>
<p class="lead">The impact comes from one behaviour change: after heavy rain, scouts look in the right place sooner. Each link in the pathway has an indicator, so the pilot shows which links hold.</p>
<div class="pathway">
  <div><b>Activity</b>A rain trigger produces a ranked 30-minute route. Scouts log and an adviser confirms.</div>
  <div><b>Output</b>More confirmed pods per scouting hour, found sooner, with misses counted.</div>
  <div><b>Outcome</b>Infected pods are removed earlier, and treatment targets affected blocks instead of the whole farm.</div>
  <div><b>Impact</b>Fewer pods lost, steadier smallholder income and a cocoa supply that copes better with wet seasons.</div>
</div>
{table(["Dimension", "How KokoShield contributes", "Indicator in the pilot"], [
  ["Economic", "Earlier removal limits spread to healthy pods and protects saleable beans [9, 25].", "Confirmed pods per scouting hour in every round; marketable share where harvest overlaps."],
  ["Environmental", "A block map of confirmed cases lets the grower treat only affected blocks, which could reduce fungicide use, including copper products [4].", "Blocks treated per round against a two-week baseline. No reduction is claimed until measured."],
  ["Climate adaptation", "Turns rainfall extremes into a planned, timed response.", "Hours from trigger to round; days from confirmation to removal."],
  ["Social", "Makes limited labour count, gives scouts a simple digital skill and the grower a record they own.", "Scouts trained, routes completed, interviews after rounds 1 and 4."],
], "", ["17%", "47%", "36%"])}
<h2>Sustainable Development Goals [26]</h2>
<div class="sdgs"><div><span>2.3</span>Smallholder productivity and incomes: protects saleable cocoa with a low-cost, sponsor-paid service.</div><div><span>2.4</span>Resilient agricultural practice: a repeatable post-rain scouting routine.</div><div><span>13.1</span>Resilience to climate hazards: links rain extremes to a farm action with measured response times.</div><div><span>17.17</span>Partnerships: grower, adviser, university and sponsor share the cost and the evidence.</div></div>
<p class="note">What one farm cannot show: a yield increase, a fungicide reduction or income gains. These need repeat seasons and more farms, and are reported as hypotheses until then.</p>''')

# 13 Market (global and Malaysia)
page(f'''<h1>Market: where cocoa is grown and who grows it</h1>
<p class="lead">Cocoa is a 4.7 million tonne crop [20] grown mostly on small farms. Malaysia is a small producer, which makes it a practical place to prove a method that can travel to the large producing regions.</p>
<div class="twocol wide">
<div><h2>Global supply, 2024/25</h2>{hbars([("Africa", 3.25, True), ("Americas", 1.15, False), ("Asia and Oceania", .30, False)], lambda v: f"{v:.2f}", w=330, label_w=110, axis="Million tonnes of cocoa beans")}
<p class="small">Figure 10. ICCO Annual Report 2024/25 regional estimates [19]. The August 2026 bulletin puts 2024/25 gross output at 4.733 million tonnes [20].</p></div>
<div><h2>Malaysian bean production</h2>{vbars([("2021", 537, False), ("2022", 493, False), ("2023", 269, False), ("2024", 445, False), ("2025", 268, True)], lambda v: f"{v}", axis="Tonnes, Malaysian Cocoa Board [2]")}
<p class="small">Figure 11. National totals from all causes; the series does not identify disease losses [2].</p></div>
</div>
<div class="twocol wide">
<div><h2>Malaysian cocoa area, 2025</h2>{hbars([("Smallholdings", 5662, True), ("Estates", 918, False)], lambda v: f"{v:,} ha", w=330, label_w=110, axis="Cultivated hectares [2]")}
<p class="small">Figure 12. Smallholdings are 86% of the 6,580 ha total [2].</p></div>
<div><h2>Why the demand is growing</h2>
<p><b>More rain extremes.</b> Heavy wet-season rain is already linked to lower yields in three producing countries [3], so growers face more post-rain decisions with the same labour.</p>
<p><b>Scattered holdings.</b> Advisers cannot visit every farm after every storm. A cooperative or buyer that reaches many farms through one coordinator is the practical channel [16].</p>
<p><b>Supply continuity.</b> Buyers that depend on smallholder beans have a reason to fund a low-cost service that protects supply.</p></div>
</div>''')

# 14 Addressable market
page(f'''<h1>Addressable market and the first cluster</h1>
<div class="twocol wide">
<div><p class="lead">Malaysia's Agriculture Census counted 4,147 individual cocoa holdings in 2023, 3,358 of them in Sabah and Sarawak [21]. Selangor, with 42 holdings, suits a pilot near the university but is too small for a 20-farm paid cluster, so the first paid cluster is planned for Sabah or Sarawak.</p>
{hbars([("Sabah", 2217, True), ("Sarawak", 1141, False), ("Peninsular Malaysia", 789, False)], lambda v: f"{v:,}", w=330, label_w=120, axis="Individual cocoa holdings, 2023 [21]")}
<p class="small">Figure 13. Department of Statistics Malaysia. Peninsular is the national total less Sabah and Sarawak.</p></div>
<div>{table(["Level", "Arithmetic", "Seasonal fee pool"], [
  ["Malaysia ceiling", "4,147 holdings x RM75", "RM311,025"],
  ["Sabah and Sarawak", "3,358 holdings x RM75", "RM251,850"],
  ["Peninsular", "789 holdings x RM75", "RM59,175"],
  ["2028 target", "60 active farms x RM75", "RM4,500 (1.4% of the ceiling)"],
  ["First paid cluster", "20 active farms x RM75", "RM1,500"],
], "small", ["32%", "38%", "30%"])}
<p class="small">The census counts holdings; the RM75 fee is our assumption, so these ceilings show arithmetic only. A reachable market is the eligible farms on a sponsor's roster with a confirmed budget.</p>
<h2>Beyond Malaysia</h2>
<p>The same service applies to cocoa smallholders in Indonesia (about 200,000 tonnes in 2024/25 [19]) and West Africa, priced locally. The prototype already includes a rice-blast profile for China, the proposed first cross-crop demonstration (page 20).</p></div>
</div>
<div class="photostrip">{fig(PH + "02_hook_close.jpg", "Cocoa farm, Can Tho, Vietnam. Isabell Schulz, CC BY-SA 2.0 [28].")}{fig(PH + "10_pods.jpg", "Cocoa pods at a farm in Hingurakgoda, Sri Lanka. Pierre Andre Leclercq, CC BY 4.0 [31].")}</div>''')

# 15 Competitors
page(f'''<h1>Competitors and where KokoShield fits</h1>
<p class="lead">Each existing option does one job well: forecasts say when, diagnosis apps say what, logs record what happened. None turns a rain event into a time-limited, block-level route and then measures whether it worked.</p>
{table(["Capability", "Usual round and paper log", "Spreadsheet records [6]", "Forecast models [5]", "Plantix [23]", "PlantwisePlus [24]", "KokoShield (designed)"], [
  ["Works offline or on paper", "Yes", "Partly", "No", "Partly", "Partly", "Yes"],
  ["Uses rainfall as a trigger", "No", "Partly", "Yes", "No", "No", "Yes"],
  ["Ranks blocks within one farm", "No", "No", "No", "No", "No", "Yes"],
  ["Fits a fixed time budget", "No", "No", "No", "No", "No", "Yes"],
  ["Identifies symptoms from photos", "No", "No", "No", "Yes", "Factsheets", "Photo for review"],
  ["Confirms cases with an adviser", "Informal", "No", "No", "No", "No", "Yes"],
  ["Measures finds and misses per hour", "No", "No", "No", "No", "No", "Yes"],
  ["Coverage report for a sponsor", "No", "Manual", "No", "No", "No", "CSV export"],
], "comp", ["22%", "13%", "13%", "13%", "11%", "13%", "15%"])}
<p class="small">Our assessment from public product descriptions and the cited studies, to be checked with growers. "Partly" means the capability needs manual work or a connection. KokoShield's column describes designed features that the pilot will test, so we do not add up or rank the scores.</p>
<div class="twocol wide">
<div>{position_svg()}<p class="small">Figure 14. Qualitative positioning of the options a Malaysian cocoa grower can use today.</p></div>
<div><h2>Partners, not rivals</h2><p>KokoShield does not rebuild diagnosis. A scout who needs help with a symptom can use Plantix or a PlantwisePlus factsheet, and the case still goes to the adviser for confirmation.</p>
<h2>What could erode the advantage</h2><p>A diagnosis app could add field routing, or a cooperative could write its own spreadsheet rule. Our defence is evidence and fit: paired results by round, setup a cluster coordinator can manage, and a record sponsors can use. Without field results we claim no advantage.</p></div>
</div>''')

# 16 Business model
page(f'''<h1>Business model: growers free, sponsors pay</h1>
<p class="lead">The daily user is the grower or scout. The paying customer is a sponsor, a cooperative, buyer or programme, that pays per active farm per season because it gains a cluster-wide record and protects the beans it buys. Smallholders, the most price-sensitive group, pay nothing.</p>
{table(["Tier", "Who pays", "What is included"], [
  ["Grower Basic", "Free", "Ranked route, Walk screen, printable checklist, the farm's own log and CSV export."],
  ["Cluster Service", "Sponsor, RM75 per active farm per season", "Coordinator setup, adviser review workflow, monthly coverage reports and support."],
  ["Field Node", "Not priced", "Offered at cost only after hardware testing. Not part of the 2027 offer."],
], "", ["20%", "28%", "52%"])}
<div class="twocol wide">
<div><h2>Contribution per cluster at RM75</h2>{contribution()}<p class="small">Figure 15. Contribution = (RM75 - RM30) x active farms - RM600 per cluster. At 20 farms: RM1,500 revenue, RM1,200 direct cost.</p></div>
<div><h2>Sensitivity to fee and size</h2>{heat()}<p class="small">Figure 16. Contribution in RM per cluster per season. Red cells are a shortfall on direct costs.</p></div>
</div>
<div class="twocol">
<div><h2>Break-even</h2><p>Direct-cost break-even is 14 active farms at RM75, 20 at RM60 and 10 at RM90. It excludes product development, overhead and taxes. The fee, the RM600 per-cluster cost and the RM30 per-farm cost are planning assumptions that the first paid trial will measure.</p></div>
<div><h2>What a sponsor gets</h2><p>A dated record of scouting coverage, confirmed cases and follow-up for every farm, monthly. Farm-level data is shared only with the grower's consent; the sponsor sees cluster totals otherwise.</p></div>
</div>''')

# 17 Go-to-market
page(f'''<h1>Go-to-market: four gated phases</h1>
<p class="lead">Each phase has a scale, a cost and a go or no-go gate, so we spend more only after the previous step has worked.</p>
<div class="phases">
  <div><em>Phase 0, Jan-Feb 2027</em><b>Validate</b>One farm in Selangor, four paired rounds. RM1,200 cash, no revenue.<i>Gate: the decision rule on page 11 is met.</i></div>
  <div><em>Phase 1, Jul-Dec 2027</em><b>First paid cluster</b>One cooperative or buyer in Sabah or Sarawak, 20 active farms x RM75 = RM1,500. Direct cost RM1,200.<i>Gate: at least 14 active farms all season and a written renewal intent.</i></div>
  <div><em>Phase 2, 2028</em><b>Scale in Malaysia</b>Three clusters, 60 farms. Revenue RM4,500, contribution RM900. Rice-blast field trial with a partner.<i>Gate: two of three sponsors renew.</i></div>
  <div><em>Phase 3, 2029</em><b>Regional</b>A partner pilot for cocoa in Indonesia with the same protocol. License the playbook to programmes and buyers.<i>Gate: a local equal-time test confirms results.</i></div>
</div>
<p class="small">Revenue at this scale is small. The commercial goal of Phases 1 and 2 is to prove that sponsors pay and renew, not to cover development costs.</p>
<div class="twocol wide">
<div><h2>Sales steps for the first paid cluster</h2>
{table(["When", "Step"], [
  ["Mar 2027", "Shortlist five cooperatives, buyers or cluster programmes in Sabah and Sarawak from public sources [16]."],
  ["Mar-Apr", "Discovery calls with pilot results by round: decision maker, budget holder, renewal criterion."],
  ["May", "Letter of intent: 20 farms, RM75 per active farm, onboarding plan and renewal measure."],
  ["Jun", "Train one coordinator; map each farm's blocks in one visit of about 90 minutes."],
  ["Jul-Dec", "Monthly coverage report; one messaging group for support; log support hours."],
  ["Dec 2027", "Renewal review with results by farm and the real support cost."],
], "small", ["20%", "80%"])}</div>
<div><h2>Delivery</h2>
<p><b>Setup.</b> The coordinator maps blocks with the grower and sets the trigger. We support the first two farms in person.</p>
<p><b>Weather.</b> The nearest public gauge [8] or the grower's own reading.</p>
<p><b>Confirmation.</b> The cluster's adviser reviews pending cases within 48 hours.</p>
<p><b>Partners to approach.</b> The pilot grower [7], an agricultural adviser, the Malaysian Cocoa Board cluster programme [16], a cooperative or buyer, and UM supervisors for study design and Field Node testing. No agreement is signed yet.</p></div>
</div>''')

# 18 Team and timeline
TEAM = [("LS", "Leow Shen En", "Grower engagement", "Site agreement, grower interviews, block mapping and permissions."),
        ("CP", "Chong Pohyi", "Prototype and data", "Field Desk, data model and CSV analysis."),
        ("CZ", "Choong Zhuo Lin", "Trial coordination", "Rain trigger, round scheduling, scout rotation and adviser reviews."),
        ("LJ", "Lee Jia Shern", "Commercial", "Sponsor shortlist, discovery calls, pricing and the letter of intent."),
        ("TX", "Teoh Xi Xian", "Presentation and impact", "Overview video, impact indicators and the regional presentation.")]
page(f'''<h1>The team and the plan</h1>
<p class="lead">Five students at Universiti Malaya, each owning one part of the pilot. Protocol versions and decisions are kept in one shared project log.</p>
<div class="team">{"".join(f'<div><span class="av">{i}</span><b>{n}</b><em>{r}</em><p>{d}</p></div>' for i, n, r, d in TEAM)}</div>
<h2>Competition timeline</h2>
{table(["GSC phase", "What we deliver"], [
  ["Ignite", "This proposal, team information and a two-minute overview video [1]."],
  ["Build, to 22 Feb 2027", "Take Field Desk into the Malaysian field comparison and present findings, user feedback and a live prototype at the regional final if selected [1, 10]."],
  ["Shine, if selected", "Pilot results, first sponsor conversations and a rice-blast demonstration at the Global Finale, Zhejiang University, Hangzhou, 20-21 May 2027 [10]."],
], "", ["24%", "76%"])}
<h2>Eight-week Build plan</h2><div style="width:150mm">{gantt()}</div>
<p class="small">Figure 17. Field weeks depend on a signed site agreement, safe access and usable rain. If no site is signed by the end of week 1 we switch to a backup grower and the dry run moves to week 3.</p>''')

# 19 Budget and risks
page(f'''<h1>Budget and risks</h1>
<div class="twocol wide">
<div><h2>Pilot cash budget: RM1,200</h2>
{table(["Cost line", "Basis", "RM"], [
  ["Field verification", "4 adviser review sessions x RM120, one per scored round", "480"],
  ["Travel", "6 trips x RM60: setup, dry run and 4 scored rounds", "360"],
  ["Supplies and hosting", "Printed materials, hosting and connectivity", "180"],
  ["Contingency", "For example a fifth round if one is unusable", "180"],
  ["Drone survey", "Borrowed from Universiti Malaya; charged on campus", "0"],
  ["<b>Total</b>", "Student time and existing phones tracked separately", "<b>1,200</b>"],
], "small", ["30%", "56%", "14%"])}
<p class="small">Planning estimates; quotes and adviser arrangements are pending. The total equals the direct cost of a 20-farm cluster on page 16 by coincidence; the two are unrelated.</p></div>
<div>{hbars([("Field verification", 480, True), ("Travel", 360, False), ("Supplies and hosting", 180, False), ("Contingency", 180, False)], lambda v: f"RM{v}", w=330, label_w=130, axis="Planned cash outlay (RM)")}<p class="small">Figure 18. Cash estimate for the first farm pilot.</p></div>
</div>
<h2>Risks and how we respond</h2>
{table(["Risk", "Response", "Decision point"], [
  ["Pilot access is delayed", "Approach a backup grower with comparable access and a review contact.", "Site confirmed by the end of Build week 1."],
  ["Few usable rain events", "Keep dry-run feedback and extend observation.", "Explain limited evidence at Build."],
  ["Rain data too coarse", "Record gauge distance and data age [8]; allow the grower's own readings.", "Drop a signal that cannot separate blocks."],
  ["More finds, but more misses", "Same follow-up check for both routes; report missed cases.", "Investigate blind spots before a second site."],
  ["Low grower or sponsor uptake", "Record why scouts override routes; test renewal criteria with five sponsors.", "Re-price or revise delivery after measuring support."],
  ["Drone cannot fly", "Use the grower's own wet-block observation.", "Drone stays optional until it adds information in two rounds."],
  ["Data privacy", "Grower owns the record; sponsors see totals unless the grower consents.", "Data terms agreed before collection."],
], "small", ["24%", "44%", "32%"])}''')

# 20 Next steps and references
REFS = [
 "Global Sustainability Challenge. 2026-27 Program Guide. globalsustainabilitychallenge.org/challenge-details",
 "Malaysian Cocoa Board. Cocoa cultivated area and bean production statistics. koko.gov.my/doc/en/statistics",
 "Albright et al. Rainfall extremes drive cocoa yield losses across the tropics. PNAS, 2026. doi.org/10.1073/pnas.2606123123",
 "A review of current management strategies for controlling black pod disease in Malaysia. FAO AGRIS. agris.fao.org/search/en/providers/122640/records/6671960b75507fed3402cb1b",
 "Ling et al. Application of ARIMAX model to forecast weekly cocoa black pod disease incidence, 2019. doi.org/10.13189/ms.2019.070705",
 "Malaysian Cocoa Journal. Monitoring cocoa black pod disease incidence with Excel tool, 2022. mcj.koko.gov.my/ArticleDetail.aspx?ID=52",
 "Kuala Langat Municipal Council. Ladang Koko Lee Tanjung Sepat. mpkl.gov.my/pelawat/tarikan-pelancong/ladang-koko-lee-tanjung-sepat",
 "Department of Irrigation and Drainage Malaysia. Public InfoBanjir rainfall data. publicinfobanjir.water.gov.my/hujan/data-hujan",
 "International Cocoa Organization. Cocoa pests and diseases. icco.org/pests-diseases",
 "Global Sustainability Challenge. Regional finals and global finale. globalsustainabilitychallenge.org",
 "University of California Agriculture and Natural Resources. Weather conditions favorable to blast. ucanr.edu/blog/uc-rice-blog/article/weather-conditions-favorable-blast",
 "Government of India and ICAR. Paddy disease surveillance advisory. pib.gov.in/PressReleasePage.aspx?PRID=2315084",
 "Cornell Integrated Pest Management. Grapevine downy mildew fact sheet. cals.cornell.edu/integrated-pest-management",
 "Phytopathology. Spatial analysis of rice blast in China at three different scales. doi.org/10.1094/PHYTO-01-18-0006-R",
 "Embrapa Hortalicas. Potato diseases and late blight. embrapa.br/en/web/hortalicas/batata/doencas",
 "Malaysian Cocoa Board. Cocoa Cluster Development Programme. ecocoa.koko.gov.my/program-pembangunan-rantaian-kluster-koko",
 "Otuo-Akyampong Boakye. Cocoa tree with pods. Wikimedia Commons, CC BY-SA 4.0. commons.wikimedia.org/wiki/File:Cocoa_tree_with_pods.jpg",
 "Scot Nelson. Cacao black pod rot 29064726523. Wikimedia Commons, CC0 1.0. commons.wikimedia.org/wiki/File:Cacao_black_pod_rot_29064726523.jpg",
 "International Cocoa Organization. Annual Report 2024/25, global cocoa production. icco.org/wp-content/uploads/ICCO-Annual-Report-2024-2025-EN.pdf",
 "International Cocoa Organization. August 2026 Quarterly Bulletin of Cocoa Statistics. icco.org/august-2026-quarterly-bulletin-of-cocoa-statistics",
 "Department of Statistics Malaysia. Agriculture Census 2024, cocoa, 2023 reference year. storage.dosm.gov.my/census/census_agri_2023_cocoa.pdf",
 "Global Sustainability Challenge. Frequently asked questions. globalsustainabilitychallenge.org/faqs",
 "Plantix. Crop diagnosis app and field use. plantix.net/en",
 "CABI. PlantwisePlus digital tools and factsheets. cabi.org/plantwiseplus/resources",
 "Guest, D. Black pod: diverse pathogens with a global impact on cocoa yield. Phytopathology 97(12), 2007. doi.org/10.1094/PHYTO-97-12-1650",
 "United Nations. Sustainable Development Goals: targets 2.3, 2.4, 13.1 and 17.17. sdgs.un.org/goals",
 "Irene Scott for AusAID. Cocoa farmer David Kebu Jnr and his son Snider Kebu display cocoa pods from Kebu farm. Wikimedia Commons, CC BY 2.0.",
 "Isabell Schulz. Cacao farm, Can Tho (45199902095). Wikimedia Commons, CC BY-SA 2.0.",
 "USAID Indonesia. A farmer prunes a cocoa tree at a plantation in Deli Serdang, North Sumatra. Wikimedia Commons, public domain.",
 "Irene Scott for AusAID. Cocoa farmer Flora Kebu explains her farming process at Kebu farm. Wikimedia Commons, CC BY 2.0.",
 "Pierre Andre Leclercq. CIC Farm Hingurakgoda Sri Lanka. Wikimedia Commons, CC BY 4.0.",
]
page(f'''<h1>Next steps</h1>
<div class="twocol wide">
<div><p><b>Second site.</b> Repeat the cocoa comparison with a different grower and compare with the first farm. A partner receives the protocol, a data dictionary, results by round and known limitations.</p>
<p><b>Rice blast in China.</b> The prototype already switches to a rice profile (Hangzhou demo paddy, leaf wetness over an 8-hour trigger) with its own scout log. A field trial needs a local rice partner and adviser; the outcome becomes confirmed affected blocks per scouting hour [11, 14].</p>
<p><b>Other crops.</b> The block map, ranking, Walk screen and review log transfer; local teams set the crop, disease, weather input and confirmation method, for example grape downy mildew [13] or potato late blight [15].</p>
<p><b>Shade as a future input.</b> Dense shade worsens black pod, so shade level per block is a credible next signal for the ranking once the pilot rule is proven.</p>
<p><b>Field Node.</b> Print the enclosure, design power and mounting, and test outdoors before any reading feeds a scored round.</p></div>
{phone(SH + "phone_rice.jpg", "50mm", "margin:0 auto")}
</div>
<p class="figcap" style="text-align:right">Figure 19. Rice profile on a phone, real screenshot with demo data.</p>
<h2>References</h2>
<ol class="refs">{"".join(f"<li>{html.escape(r)}</li>" for r in REFS)}</ol>''')

# =====================================================================================
CSS = FONT + f"""
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:#fff}}
body{{font-family:"Plex KS","IBM Plex Sans",system-ui,sans-serif;color:{INK};font-size:9.4pt;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:297mm;padding:13mm 16mm 12mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;display:flex;flex-direction:column}}
.page:last-child{{page-break-after:auto;break-after:auto}}
.hdr{{display:flex;justify-content:space-between;font-size:7.6pt;color:{INK3};letter-spacing:.04em;border-bottom:1px solid {LINE};padding-bottom:2.2mm;margin-bottom:6mm}}
.hdr b{{color:{BR};font-weight:700}}
.content{{flex:1;min-height:0;overflow:hidden}}
h1{{font-size:19pt;line-height:1.15;color:{BRD};margin:0 0 3.5mm;font-weight:700;letter-spacing:-.01em}}
h2{{font-size:10.6pt;color:{INK};margin:4mm 0 1.6mm;font-weight:700}}
p{{margin:0 0 2.4mm}}
.lead{{font-size:10.6pt;line-height:1.45;color:{INK}}}
.small,.small p,.small td{{font-size:8pt;color:{INK2}}}
.note{{font-size:8.4pt;color:{INK2};background:{TINT};border-left:3px solid {BR};padding:2.4mm 3.4mm;border-radius:0 4px 4px 0;margin-top:3mm}}
.figcap,figcaption{{font-size:7.9pt;color:{INK3};margin:1.6mm 0 2.4mm}}
figure{{margin:0}} figure img{{width:100%;display:block;border-radius:5px}}
table{{width:100%;border-collapse:collapse;margin:1.6mm 0 2.4mm;font-size:8.5pt;table-layout:fixed}}
th{{text-align:left;font-weight:700;color:{BRD};background:{TINT};padding:1.6mm 2mm;border-bottom:1.4px solid {BR};font-size:8.2pt}}
td{{padding:1.6mm 2mm;border-bottom:1px solid {LINE};vertical-align:top;color:{INK}}}
table.small td,table.small th{{font-size:7.9pt;padding:1.25mm 1.8mm}}
.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:7mm}}
.twocol.wide{{gap:8mm;align-items:start}}
.steplabel{{display:inline-block;font-size:7.8pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#fff;background:{BR};border-radius:3px;padding:.8mm 2.4mm;margin-bottom:2mm}}
.kicker{{font-size:8.4pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{BR}}}
/* cover */
.cover{{padding:0}}
.cover-photo{{height:178mm;background-size:cover;background-position:50% 40%;position:relative}}
.cover-cap{{position:absolute;left:16mm;right:16mm;bottom:4mm;color:#fff;font-size:7.6pt;text-shadow:0 1px 3px rgba(0,0,0,.8)}}
.cover-body{{padding:12mm 16mm 0}}
.cover-title{{font-size:44pt;margin:2mm 0 1mm;color:{BRD};letter-spacing:-.02em}}
.cover-sub{{font-size:15pt;color:{INK};margin-bottom:9mm;max-width:150mm;line-height:1.3}}
.cover-meta{{display:grid;grid-template-columns:1fr 1.4fr 1fr;gap:6mm;border-top:1.5px solid {BR};padding-top:4mm;font-size:9pt;color:{INK2}}}
.cover-meta b{{display:block;color:{BRD};font-size:8pt;letter-spacing:.08em;text-transform:uppercase;margin-bottom:1mm}}
/* exec cards */
.cards{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin:5mm 0 3mm}}
.card{{border:1px solid {LINE};border-top:3px solid {BR};border-radius:5px;padding:3mm 3.4mm;font-size:8.6pt;color:{INK2};background:#fff}}
.card b{{display:block;color:{INK};font-size:9.6pt;margin-bottom:1.2mm}}
.card.ask{{background:{TINT}}}
/* devices */
.laptop{{margin:0 auto}}
.lscreen{{background:#0d1210;border-radius:3.2mm 3.2mm 0 0;padding:2.4mm 2.4mm 2.6mm;box-shadow:0 1.2mm 4mm rgba(0,0,0,.18)}}
.lscreen img{{width:100%;display:block;border-radius:.8mm}}
.lbase{{height:3.2mm;margin:0 -6%;background:linear-gradient(#cfd4d0,#9aa19c);border-radius:0 0 3mm 3mm}}
.phone{{background:#0d1210;border-radius:6.5mm;padding:1.8mm;box-shadow:0 1.2mm 4mm rgba(0,0,0,.22)}}
.pscreen{{border-radius:5mm;overflow:hidden}} .pscreen img{{width:100%;display:block}}
.hero{{position:relative;width:178mm;height:96mm;margin:2mm 0 0}}
.hero .laptop{{position:absolute;left:0;top:0;margin:0}}
.hero .phone{{width:40mm}}
.sysfig{{margin-top:3mm}}
/* problem */
.probgrid{{display:grid;grid-template-columns:1.55fr 1fr;gap:7mm;align-items:start}}
.probphoto img{{height:96mm;object-fit:cover}}
.stats{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin:3mm 0}}
.stats div{{background:{TINT};border-radius:5px;padding:2.6mm 3mm;font-size:8pt;color:{INK2}}}
.stats span{{display:block;font-size:15pt;font-weight:700;color:{BRD};line-height:1.1;margin-bottom:1mm}}
ol.steps{{padding-left:5mm;margin:0}} ol.steps li{{margin-bottom:1.8mm}}
.phones{{display:flex;justify-content:space-between;margin:3mm 2mm 0}}
.phonecaps{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6mm;font-size:8.2pt;color:{INK2};margin:2.4mm 2mm 0}}
.provegrid{{display:grid;grid-template-columns:1.55fr 1fr;gap:6mm;align-items:start;margin-bottom:3mm}}
.framed{{width:100%;border-radius:5px;border:1px solid {LINE};display:block;overflow:hidden}}
.pilotgrid{{display:grid;grid-template-columns:62mm 1fr;gap:7mm;align-items:start}}
.keynums{{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm}}
.keynums div{{background:{TINT};border-radius:5px;padding:2.4mm 2.8mm;font-size:7.8pt;color:{INK2}}}
.keynums span{{display:block;font-size:14pt;font-weight:700;color:{BRD};line-height:1.1}}
.decision{{background:{TINT};border:1px solid {BR};border-radius:6px;padding:1mm 4mm 2.4mm}}
.decision ol{{margin:0;padding-left:5mm}} .decision li{{margin-bottom:1mm}}
.pathway{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:3mm 0 3mm}}
.pathway div{{position:relative;background:{TINT};padding:3mm 5mm 3mm 4mm;font-size:8.3pt;color:{INK2};margin-right:3mm;clip-path:polygon(0 0,calc(100% - 4mm) 0,100% 50%,calc(100% - 4mm) 100%,0 100%,4mm 50%)}}
.pathway div:first-child{{clip-path:polygon(0 0,calc(100% - 4mm) 0,100% 50%,calc(100% - 4mm) 100%,0 100%)}}
.pathway div:nth-child(4){{background:{BR};color:#fff}} .pathway div:nth-child(4) b{{color:#fff}}
.pathway b{{display:block;color:{BRD};font-size:9.4pt;margin-bottom:1mm;padding-left:2mm}}
.pathway div:not(:first-child){{padding-left:7mm}}
.sdgs{{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm 6mm;font-size:8.3pt;color:{INK2}}}
.sdgs span{{display:inline-block;background:{BR};color:#fff;font-weight:700;border-radius:3px;padding:.3mm 2mm;margin-right:2mm;font-size:8.4pt}}
.band{{display:grid;grid-template-columns:62mm 1fr;gap:6mm;align-items:center;margin-top:4mm;background:#F3F4F1;border-radius:6px;overflow:hidden}}
.band img{{width:100%;height:46mm;object-fit:cover;display:block}} .band>div{{padding:2mm 5mm 1mm 0}} .band h2{{margin-top:0}}
.band.low img{{height:40mm;object-position:50% 30%}}
.photostrip{{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:3mm}}
.photostrip img{{height:52mm;object-fit:cover}}
table.comp td{{text-align:center;font-size:7.9pt}} table.comp td:first-child{{text-align:left}} table.comp th{{font-size:7.6pt}}
table.comp td:last-child{{background:{TINT};font-weight:700;color:{BRD}}}
.phases{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:2mm 0 2mm}}
.phases div{{border:1px solid {LINE};border-top:4px solid {BR};border-radius:5px;padding:2.6mm 3mm;font-size:8.1pt;color:{INK2}}}
.phases div:first-child{{background:{TINT}}}
.phases em{{display:block;font-style:normal;font-size:7.5pt;color:{INK3};letter-spacing:.04em}}
.phases b{{display:block;color:{INK};font-size:10pt;margin:.6mm 0 1.2mm}}
.phases i{{display:block;font-style:normal;margin-top:1.6mm;color:{BRD};font-weight:600}}
.team{{display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin:3mm 0 2mm}}
.team div{{border:1px solid {LINE};border-radius:6px;padding:3mm;font-size:8pt;color:{INK2};text-align:center}}
.team .av{{display:flex;align-items:center;justify-content:center;width:13mm;height:13mm;border-radius:50%;background:{BR};color:#fff;font-weight:700;font-size:11pt;margin:0 auto 2mm}}
.team b{{display:block;color:{INK};font-size:9pt}} .team em{{display:block;font-style:normal;color:{BR};font-weight:700;font-size:8pt;margin:.6mm 0 1.4mm}}
.team p{{margin:0;text-align:left}}
ol.refs{{columns:2;column-gap:7mm;font-size:6.7pt;line-height:1.32;color:{INK2};padding-left:5mm;margin:0}}
ol.refs li{{margin-bottom:.7mm;break-inside:avoid;overflow-wrap:anywhere}}
table.status td{{font-size:8.6pt;padding:2.2mm 2mm}}
"""
def build():
    parts = []
    n = 0
    for body, cls, header in PAGES:
        n += 1
        hdr = f'<div class="hdr"><span><b>KokoShield</b>&nbsp;&nbsp;Weather-guided black pod scouting</span><span>GSC 2026-27 Ignite&nbsp;&nbsp;&nbsp;{n}</span></div>' if header else ""
        parts.append(f'<section class="page {cls}">{hdr}<div class="content">{body}</div></section>')
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>KokoShield GSC Ignite Proposal</title><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
    (HERE / "proposal_v3.html").write_text(doc, encoding="utf-8")
    print("pages", n)

if __name__ == "__main__":
    build()
