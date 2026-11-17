"""Storyboard for the v5 cinematic pitch video. Writes layout_v5.html; print to PDF with Edge. Thumbnails from the finished MP4."""
import json, html, pathlib, subprocess, imageio_ffmpeg
from scenes_v5 import SCENES
FF = imageio_ffmpeg.get_ffmpeg_exe(); ROOT = pathlib.Path("C:/Users/User/Documents/GSC"); VID = ROOT / "KokoShield_Pitch_Video.mp4"
tl = json.load(open("timeline.json", encoding="utf-8")); S = tl["starts"]; END = tl["end"]
TH = pathlib.Path("thumbs"); TH.mkdir(exist_ok=True)
LINK = "https://claude.ai/artifact/2tEKvFyTkykWYMHAH7ot2T"
SEE = {1: "THE DISEASE. Real rain footage on a tropical plantation and leaves (cold grade, light lightning), then a real black pod photo; the loss figure counts up to 20–30%.",
       2: "THE PROBLEM. A real cocoa farmer (Ghana), then a man walking his usual round down a misty farm road. The 30:00 clock runs down while a problem card states it in three lines: rain spreads black pod, ~30 minutes to scout, the usual round finds the wettest blocks late.",
       3: "THE SOLUTION. Near-silence; the holographic rain gauge passes the 30 mm trigger and the KokoShield title appears, then the real Field Desk prototype opens on a laptop and pushes into its alert.",
       4: "HOW IT WORKS. Drone hologram marks standing water while the four inputs check in and the route A → D → B → G draws. Then real prototype footage: blocks on the aerial map, usual round vs priority, the route list, Start scouting.",
       5: "The Field Node CAD model in 3D (turntable and explode) with callouts, then the same node on the prototype's Sensor node page.",
       6: "THE PROOF. Split screen of two real scouts walking farm paths, each with the prototype's aerial mini-map: GPS trail along the real footpaths, a pin for each find, one shared 30-minute clock. Usual round 2 finds (first at minute 4), priority route 7 (first at minute 2). Ends on the real Compare screen.",
       7: "THE FIND. A real black pod photo, then the scout's phone running the real Walk screen (Found, 3 pods, Save) and the adviser confirming on the Scout log.",
       8: "IMPACT. Real drone footage over a tree-crop farm, cocoa farmers, impact check-ins, then a rice paddy with the prototype's real rice-blast profile on the phone.",
       9: "THE ASK. Real footage of a farmer walking into the farm, the RM 1,200 card, then the end card with logo and credits."}
SOUND = {1: "Real rain ambience under heavy rain, thunder after each lightning flash, a low drone and a ticking minor pulse.",
         2: "Rain eases; a clock tick every second under the voice; a pop as each problem line appears; a riser into the cut.",
         3: "Silence, one high ding, gauge ticks, a trigger chime, then a thud and chime on the KokoShield title as an electronic pulse starts.",
         4: "Drone hum, water drips, four input pops, a rising sweep as the route draws, a chime; then soft clicks on each real click in the app. Electronic bass and kick build.",
         5: "Whoosh in, a rising sweep as the parts explode, pops on each callout, two clicks as it snaps back together, a chime.",
         6: "Heartbeat under the walk, clock ticks, a bright blip each time the priority scout drops a pin, duller bells for the usual round, finish bell. Driving peak.",
         7: "Taps on the phone (Found, plus, plus, Save), a blip and chime, then clicks as the adviser confirms.",
         8: "Music opens into a broad hopeful resolve; gentle pops on the impact lines; a big whoosh into the rice paddy.",
         9: "Thud and chime on the ask; closing chime and bell as the music fades."}
def mmss(t): return f"{int(t//60)}:{t%60:04.1f}"
rows = []
for k, s in enumerate(SCENES):
    t0, t1 = S[k], S[k + 1]; th = TH / f"s{s['id']}.jpg"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t0 + (t1 - t0) * 0.55:.2f}", "-i", str(VID), "-frames:v", "1", "-vf", "scale=640:-1", str(th)], check=True)
    rows.append(f"""<tr><td class="n">{s['id']}<div class="tc">Act {s['act']}<br>{mmss(t0)}–{mmss(t1)}<br>{t1 - t0:.1f} s</div></td>
<td class="th"><img src="{th.resolve().as_uri()}"><div class="st">{s['title']}</div></td><td>{SEE[s['id']]}</td><td class="snd">{SOUND[s['id']]}</td><td class="vo">“{html.escape(s['narration'])}”</td></tr>""")
CLIPS = [("1 Storm", "15 s", "Rain hammering pods, orchard in the storm, the farmer steps out and looks across the rows, uncertain", "Scene 2 placeholder"),
         ("2 Decision", "15 s", "He raises his phone (blank screen, the real Walk screen composited), his expression sets, he strides into the rows", "Scene 4, before Start scouting"),
         ("3 Drone", "10 s", "Quadcopter lifts off a muddy path and climbs over the wet canopy with standing water visible", "Scene 4, before the map"),
         ("4 Find", "15 s", "Fast walk, a leaf lifted, the brown lesion revealed, phone photo, the pod cut off with a parang", "Scene 6 placeholder")]
clip_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in CLIPS)
doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>KokoShield Pitch Video Layout</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>@page{{size:A4 landscape;margin:11mm}} body{{font-family:'Noto Sans','Segoe UI',sans-serif;color:#1f2421;font-size:8pt;line-height:1.36;margin:0}}
h1{{font-size:18pt;margin:0 0 2pt;color:#2B654F}} h2{{font-size:11pt;margin:10pt 0 4pt}} .meta{{color:#5f6b65;margin-bottom:6pt}}
.facts{{display:grid;grid-template-columns:repeat(6,1fr);gap:5pt;margin:6pt 0 8pt}} .facts div{{background:#eef3ef;border-top:3px solid #2B654F;padding:4pt 6pt;font-size:7.6pt}} .facts b{{display:block;font-size:9.6pt;color:#2B654F}}
table{{width:100%;border-collapse:collapse}} th{{background:#2B654F;color:#fff;text-align:left;padding:4pt 5pt;font-size:7.8pt}} td{{border-bottom:1px solid #d7e0db;padding:4.5pt 5pt;vertical-align:top}} tr{{break-inside:avoid}}
td.n{{width:7%;font-size:14pt;font-weight:700;color:#2B654F}} .tc{{font-size:7.2pt;font-weight:400;color:#5f6b65;margin-top:2pt}} td.th{{width:21%}} td.th img{{width:100%;border:1px solid #d7e0db;display:block}} .st{{font-weight:700;font-size:8pt;margin-top:2pt}}
td.snd{{width:17%;color:#33403a}} td.vo{{width:26%;font-style:italic}} .cols{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12pt}} ul{{margin:2pt 0 0;padding-left:13pt}} li{{margin-bottom:2pt}} code{{background:#eef3ef;padding:0 3pt;font-size:7.6pt}} a{{color:#2B654F}}</style></head><body>
<h1>KokoShield Pitch Video: Layout and Script (v7: problem → solution → proof, real footage and real prototype)</h1>
<div class="meta">GSC 2026–27 Ignite · Two-minute pitch film · The problem → the solution → how it works → the proof → impact and the ask · Universiti Malaya</div>
<div class="facts"><div><b>{mmss(END)}</b>Total length (limit 2:00)</div><div><b>Clear story</b>The problem → the solution → how it works → the proof → the ask</div><div><b>Real photos</b>15 credited Wikimedia Commons photos, cinematic grades</div>
<div><b>Real prototype</b>Footage recorded click by click from prototype/KokoShield_Prototype.html on laptop and phone</div><div><b>Score</b>Ticking dread → electronic pulse → driving peak → hopeful resolve</div><div><b>Real footage</b>11 Pexels clips: rain, cocoa farmer, two scouts, drone</div></div>
<table><tr><th>Beat / time</th><th>Frame</th><th>What is on screen</th><th>Sound</th><th>Narration</th></tr>{''.join(rows)}</table>
<h2>Rebuild</h2>
<div class="cols"><div><b>Voice</b><ul><li><code>python voice_v5.py</code> (AI voice) or <code>--recordings</code> with <code>audio/s1.wav … s8.wav</code>; then rerun the hold-stretch step.</li></ul></div>
<div><b>Sound</b><ul><li><code>python make_sound_v5.py</code> then <code>python sound_v5.py</code>.</li></ul></div><div><b>Render</b><ul><li><code>python record_proto.py</code> re-records the prototype; <code>python build_page.py</code> then <code>python capture_v5.py</code> (about 10 minutes).</li><li>Interactive page (real-image story): <a href="{LINK}">{LINK}</a></li></ul></div></div>
<h2>Honesty notes</h2><div>Footage comes from Pexels (Pexels License); photos show cocoa farming in Vietnam, Indonesia, the Solomon Islands, Ghana, Sri Lanka, Ecuador and a rice paddy in India; none were taken on the pilot farm. The drone survey, route race and counts are a demo simulation on the prototype's demo farm (preset findings); the app footage is the real prototype running on demo data, and its aerial view is illustrative. The two scouts are stock footage; their routes and finds are a demo simulation on the prototype map. The voice is AI-generated. The 20–30% figure is Guest (2007); the RM1,200 ask matches the proposal's pilot budget.</div>
</body></html>"""
pathlib.Path("layout_v5.html").write_text(doc, encoding="utf-8"); print("layout_v5.html written", mmss(END))
