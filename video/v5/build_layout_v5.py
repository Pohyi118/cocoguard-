"""Storyboard for the v5 cinematic pitch video. Writes layout_v5.html; print to PDF with Edge. Thumbnails from the finished MP4."""
import json, html, pathlib, subprocess, imageio_ffmpeg
from scenes_v5 import SCENES
FF = imageio_ffmpeg.get_ffmpeg_exe(); ROOT = pathlib.Path("C:/Users/User/Documents/GSC"); VID = ROOT / "KokoShield_Pitch_Video.mp4"
tl = json.load(open("timeline.json", encoding="utf-8")); S = tl["starts"]; END = tl["end"]
TH = pathlib.Path("thumbs"); TH.mkdir(exist_ok=True)
LINK = "https://claude.ai/artifact/2tEKvFyTkykWYMHAH7ot2T"
SEE = {1: "Cold, desaturated grade. Rain hammers leaves and a cocoa pod with live rain streaks and three lightning flashes. The loss figure counts up to 20–30%.",
       2: "Placeholder for AI clip 1 (farmer steps out after the storm). The 30:00 clock starts running down; '?' chips pop over every block.",
       3: "Hard cut to near-silence. The holographic rain gauge counts to 48 mm and passes the trigger; the KokoShield title appears with 'SYSTEM ACTIVE'.",
       4: "Hologram of the Field Desk map: the drone sweeps and standing water lights up in A, D and G; the four inputs check in; the route A → G → D → B draws itself; the real app screen floats in. Placeholder for AI clip 2 (he decides and walks in).",
       5: "The real Field Node CAD model (GLB from the kit) rendered in 3D: it turns on a glowing ring, the lid and ventilated hood explode apart and reassemble while four callouts step in (hood, enclosure, controller envelope, status).",
       6: "Split screen: usual round (left, grey) vs KokoShield route (right, green), both scouts walking the map against one 30-minute clock; finds counted as they happen.",
       7: "Placeholder for AI clip 4 (minute 7, the find). Phone scout log with a lock-on highlight, then the real reviewed scout log; 'Treat only block A'.",
       8: "Golden grade. Harvested pods, cocoa farmers, impact check-ins, then a match cut to an aerial rice paddy with the rice-blast phone profile.",
       9: "The ask card: RM 1,200 for the first single-farm pilot. End card with the logo, tagline and credits."}
SOUND = {1: "Thunder after each flash, heavy rain, low drone and a ticking minor pulse that gets louder (act-1 dread).",
         2: "Rain fades; a clock tick every second under the voice; pops on the '?' chips; a riser into the cut.",
         3: "Silence, one high ding, gauge ticks, a trigger chime, then a thud and chime on 'SYSTEM ACTIVE' as an electronic pulse starts.",
         4: "Drone hum, water drips, four input pops, a rising sweep as the route draws, a chime. Electronic bass and kick build.",
         5: "Whoosh in, a rising sweep as the parts explode, pops on each callout, two clicks as it snaps back together, a chime.",
         6: "Heartbeat under the race, clock ticks, bright lock-on blips for ranked finds, duller bells for the usual round, finish bell. Driving peak.",
         7: "Camera shutter and a lock-on blip on the find, whoosh to the app, chime.",
         8: "Music opens into a broad hopeful resolve; gentle pops on the impact lines; a big whoosh on the match cut.",
         9: "Thud and chime on the ask; closing chime and bell as the music fades."}
def mmss(t): return f"{int(t//60)}:{t%60:04.1f}"
rows = []
for k, s in enumerate(SCENES):
    t0, t1 = S[k], S[k + 1]; th = TH / f"s{s['id']}.jpg"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t0 + (t1 - t0) * 0.55:.2f}", "-i", str(VID), "-frames:v", "1", "-vf", "scale=640:-1", str(th)], check=True)
    rows.append(f"""<tr><td class="n">{s['id']}<div class="tc">Act {s['act']}<br>{mmss(t0)}–{mmss(t1)}<br>{t1 - t0:.1f} s</div></td>
<td class="th"><img src="{th.resolve().as_uri()}"><div class="st">{s['title']}</div></td><td>{SEE[s['id']]}</td><td class="snd">{SOUND[s['id']]}</td><td class="vo">“{html.escape(s['narration'])}”</td></tr>""")
CLIPS = [("1 Storm", "15 s", "Rain hammering pods, orchard in the storm, the farmer steps out and looks across the rows, uncertain", "Scene 2 placeholder"),
         ("2 Decision", "15 s", "He raises his phone (blank screen, UI composited), his expression sets, pockets it and strides into the rows", "Scene 4, after the hologram"),
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
<h1>KokoShield Pitch Video: Layout and Script (v5, cinematic four-act cut)</h1>
<div class="meta">GSC 2026–27 Ignite · Two-minute pitch film · Storm and crisis → activation → the race → vision and the ask · Universiti Malaya</div>
<div class="facts"><div><b>{mmss(END)}</b>Total length (limit 2:00)</div><div><b>4 acts, 9 beats</b>The team's film outline plus the Field Node 3D beat</div><div><b>Real photos</b>15 credited Wikimedia Commons photos, cinematic grades</div>
<div><b>Hologram + 3D</b>Real Field Desk screens with scanlines; drone sweep on the app map; the Field Node CAD model in 3D</div><div><b>Score</b>Ticking dread → electronic pulse → driving peak → hopeful resolve</div><div><b>AI clips pending</b>4 live-action clips await Canva's AI limit reset</div></div>
<table><tr><th>Beat / time</th><th>Frame</th><th>What is on screen</th><th>Sound</th><th>Narration</th></tr>{''.join(rows)}</table>
<h2>Live-action clips still to generate (Canva AI, fictional farmer, labelled AI-generated)</h2>
<table><tr><th>Clip</th><th>Length</th><th>Action</th><th>Where it goes</th></tr>{clip_rows}</table>
<div style="margin-top:4pt">When Canva's AI limit resets or is topped up, say "generate the clips". Each clip replaces the orange placeholder tag in the video; the phone screens are composited with the real app UI. Then <code>python capture_v5.py</code> renders the final cut.</div>
<h2>Rebuild</h2>
<div class="cols"><div><b>Voice</b><ul><li><code>python voice_v5.py</code> (AI voice) or <code>--recordings</code> with <code>audio/s1.wav … s8.wav</code>; then rerun the hold-stretch step.</li></ul></div>
<div><b>Sound</b><ul><li><code>python make_sound_v5.py</code> then <code>python sound_v5.py</code>.</li></ul></div><div><b>Render</b><ul><li><code>python capture_v5.py</code> (about 7 minutes).</li><li>Interactive page (real-image story): <a href="{LINK}">{LINK}</a></li></ul></div></div>
<h2>Honesty notes</h2><div>Photos show cocoa farming in Vietnam, Indonesia, the Solomon Islands, Ghana, Sri Lanka, Ecuador and a rice paddy in India; none were taken on the pilot farm. The drone survey, route race and counts are a demo simulation on the app's demo farm (prototype preset findings). The farmer in the pending clips is fictional and AI-generated. The voice is AI-generated. The 20–30% figure is Guest (2007); the RM1,200 ask matches the proposal's pilot budget.</div>
</body></html>"""
pathlib.Path("layout_v5.html").write_text(doc, encoding="utf-8"); print("layout_v5.html written", mmss(END))
