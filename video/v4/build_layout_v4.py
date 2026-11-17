"""Video layout / storyboard for the v4 pitch video (real photos, real prototype screens, drone survey).
Writes layout_v4.html (print to PDF with Edge). Thumbnails come from the finished MP4 at mid-scene."""
import json, html, pathlib, subprocess, imageio_ffmpeg
from scenes_v4 import SCENES
FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = pathlib.Path("C:/Users/User/Documents/GSC")
VID = ROOT / "KokoShield_Pitch_Video.mp4"
S = json.load(open("timeline.json", encoding="utf-8"))["starts"]
TH = pathlib.Path("thumbs"); TH.mkdir(exist_ok=True)
LINK = "https://claude.ai/artifact/2tEKvFyTkykWYMHAH7ot2T"
SEE = {
 1: "Real rain on leaves with live rain streaks and two lightning flashes, then cocoa pods on a farm in Vietnam. The 30-minute clock fills, the gauge passes the 30 mm trigger, and a real photo labels a black pod next to a healthy pod.",
 2: "Real black pod rot close-ups with the 20–30% count-up, drying beans in Ghana with three country chips, and an Indonesian smallholder pruning cocoa with the 86% donut.",
 3: "A cocoa farmer in soft focus behind the animated competitor map; KokoShield springs into the empty corner.",
 4: "Real drone photo labelled “Camera drone” (illustrative), then the survey concept on the app’s own block map: flight 1 draws the eight blocks, flight 2 after 48 mm marks standing water in A, D and G. Then the real Field Node CAD render with callouts and the rain gauge.",
 5: "The real Field Desk app in a laptop: the cursor clicks Wet spell and Generate route, and the route changes from B → A → C → G (9 mm) to A → G → D → B (48 mm). Zoom on the route list with reasons, then the phone app and printed checklist.",
 6: "Real black pod photo with the phone scout log, then the real scout log on a laptop: the cursor confirms A and G and rules out D.",
 7: "Route race on the app’s map: ranked and usual scouts walk at once against a 30-minute clock; finds pop (+3, +2, +1, +1); “Missed by usual round” flags; then the pilot facts.",
 8: "Real harvested pods, cocoa farmers in the Solomon Islands and a pod being opened, under the impact cards, money flow and 20 → 60 farm dots.",
 9: "Golden-graded farm photo with the title and team names, then an end card with the logo and photo credits.",
}
SOUND = {
 1: "Rain, two thunder rolls after the flashes, clock ticks, trigger chime, pops on the pod labels. Music: low, tense minor.",
 2: "Fading rain, tick runs on the count-ups, pops on cards and chips.",
 3: "Pops for each tool, a shimmer on the empty corner, thud and chime as KokoShield lands. Riser into scene 4.",
 4: "Music lifts to a hopeful major theme. Drone hum on both flights, water drips as standing water appears, pops on the callouts.",
 5: "Two mouse clicks, a chime as the route changes, whooshes for the zoom and the phone.",
 6: "Camera shutter for the photo log; click + ding for each confirm, click + thud for the rule-out.",
 7: "Start beeps, clock ticks, bright dings for ranked finds and duller ones for the usual round, finish bell, two low buzzes for the misses. Shaker joins the beat.",
 8: "Whooshes, gentle blips along the money flow, quick ticks as the farms fill, a chime.",
 9: "Warm title chime, music resolves; closing bell on the end card.",
}
def mmss(t): return f"{int(t//60)}:{t%60:04.1f}"
rows = []
for k, s in enumerate(SCENES):
    t0, t1 = S[k], S[k + 1]; th = TH / f"s{s['id']}.jpg"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t0 + (t1 - t0) * 0.6:.2f}", "-i", str(VID), "-frames:v", "1", "-vf", "scale=640:-1", str(th)], check=True)
    rows.append(f"""<tr><td class="n">{s['id']}<div class="tc">{mmss(t0)}–{mmss(t1)}<br>{t1 - t0:.1f} s</div></td>
<td class="th"><img src="{th.resolve().as_uri()}"><div class="st">{s['title']}</div></td><td>{SEE[s['id']]}</td><td class="snd">{SOUND[s['id']]}</td>
<td class="vo">“{html.escape(s['narration'])}”</td></tr>""")
credits = (ROOT / "KokoShield_Video_Photo_Credits.txt").read_text(encoding="utf-8").split("\n")
import re
entries = []
for i, line in enumerate(credits):
    if re.match(r'^\s*\d+\. "', line):
        author = credits[i + 1].split(":", 1)[1].strip(); lic = credits[i + 2].split(":", 1)[1].strip().split("  ")[0]
        entries.append(f"{line.strip()} — {author}, {lic}")
cred_html = "<br>".join(html.escape(e) for e in entries)
doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>KokoShield Pitch Video Layout</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
@page{{size:A4 landscape;margin:11mm}}
body{{font-family:'Noto Sans','Segoe UI',sans-serif;color:#1f2421;font-size:8pt;line-height:1.36;margin:0}}
h1{{font-size:18pt;margin:0 0 2pt;color:#2B654F}} h2{{font-size:11pt;margin:10pt 0 4pt}}
.meta{{color:#5f6b65;margin-bottom:6pt}}
.facts{{display:grid;grid-template-columns:repeat(6,1fr);gap:5pt;margin:6pt 0 8pt}}
.facts div{{background:#eef3ef;border-top:3px solid #2B654F;padding:4pt 6pt;font-size:7.6pt}} .facts b{{display:block;font-size:9.6pt;color:#2B654F}}
table{{width:100%;border-collapse:collapse}} th{{background:#2B654F;color:#fff;text-align:left;padding:4pt 5pt;font-size:7.8pt}}
td{{border-bottom:1px solid #d7e0db;padding:4.5pt 5pt;vertical-align:top}} tr{{break-inside:avoid}}
td.n{{width:6%;font-size:14pt;font-weight:700;color:#2B654F}} .tc{{font-size:7.2pt;font-weight:400;color:#5f6b65;margin-top:2pt}}
td.th{{width:21%}} td.th img{{width:100%;border:1px solid #d7e0db;display:block}} .st{{font-weight:700;font-size:8pt;margin-top:2pt}}
td.snd{{width:17%;color:#33403a}} td.vo{{width:27%;font-style:italic}}
.cols{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12pt}} ul{{margin:2pt 0 0;padding-left:13pt}} li{{margin-bottom:2pt}}
code{{background:#eef3ef;padding:0 3pt;font-size:7.6pt}} a{{color:#2B654F}} .cred{{font-size:7.2pt;color:#33403a;columns:2;column-gap:16pt}}
</style></head><body>
<h1>KokoShield Pitch Video: Layout and Script (v4, real images)</h1>
<div class="meta">GSC 2026–27 Ignite · Two-minute project overview · Real photos, the real Field Desk prototype, the drone survey concept · Universiti Malaya</div>
<div class="facts">
<div><b>{mmss(S[-1])}</b>Total length (limit 2:00)</div><div><b>9 scenes</b>Brand wipe between each; captions on screen and as .srt</div>
<div><b>Real photos</b>14 free-licensed Wikimedia Commons photos, each credited on screen</div><div><b>Real prototype</b>Field Desk screens with live clicks; app’s own map for the drone and race</div>
<div><b>Drone survey</b>New concept: borrowed UM drone maps blocks and spots standing water</div><div><b>Sound</b>AI voice “Ava”, synthesised music and effects synced to every event</div></div>
<table><tr><th>Scene / time</th><th>Frame</th><th>What is on screen</th><th>Sound</th><th>Narration</th></tr>{''.join(rows)}</table>
<h2>Finishing and reusing it</h2>
<div class="cols">
<div><b>1. Optional: your own voices</b><ul><li>Record one take per scene reading the script above. Save as <code>video/v4/audio/s1.wav</code> … <code>s9.wav</code>.</li>
<li>Run <code>python voice_v4.py --recordings</code>. Scene lengths follow your takes; keep the total under 2:00.</li></ul></div>
<div><b>2. Rebuild</b><ul><li><code>python make_sound_v4.py</code> then <code>python sound_v4.py</code> remixes music and effects under the voice.</li>
<li><code>python capture_v4.py</code> (about 8 minutes) renders the MP4 again.</li></ul></div>
<div><b>3. Interactive page</b><ul><li>The 3D story page stays a separate demo: <a href="{LINK}">{LINK}</a> (private until shared).</li>
<li>It does not yet include the drone; ask to add it if you will demo it live.</li></ul></div></div>
<h2>Honesty notes</h2>
<div>The photos show cocoa farming in other countries and were not taken on the pilot farm. The drone photo shows another operator’s flight, labelled as illustrative. The drone survey, route race and counts are a concept and demo simulation on the app’s demo farm. The Field Node is a CAD concept. The voice is AI-generated.</div>
<h2>Photo credits (Wikimedia Commons)</h2><div class="cred">{cred_html}</div>
<div style="font-size:7.2pt;color:#5f6b65;margin-top:4pt">Full titles, licence links and source pages: KokoShield_Video_Photo_Credits.txt</div>
</body></html>"""
pathlib.Path("layout_v4.html").write_text(doc, encoding="utf-8")
print("layout_v4.html written", mmss(S[-1]))
