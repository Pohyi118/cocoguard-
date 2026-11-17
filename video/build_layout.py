"""Video layout / storyboard for the KokoShield pitch video (v3: 3D motion, natural voice, music and effects).
Writes video/layout.html; print it to PDF with Edge. Thumbnails come from the finished MP4 at mid-scene."""
import json, re, html, pathlib, subprocess, imageio_ffmpeg
from scenes import SCENES

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = pathlib.Path("C:/Users/User/Documents/GSC")
VID = ROOT / "KokoShield_Pitch_Video.mp4"
S = json.loads(re.search(r"KS_STARTS=(\[.*?\]);", (ROOT / "KokoShield_3D/assets/data.js").read_text(encoding="utf-8")).group(1))
TH = pathlib.Path("frames"); TH.mkdir(exist_ok=True)
LINK = "https://claude.ai/artifact/2tEKvFyTkykWYMHAH7ot2T"

MOTION = {
    1: "Aerial fly-in over the 3D cocoa farm (blocks A–H). Rain starts and lightning flashes. A 30-minute clock fills, the gauge climbs from 0 to 48 mm past the 30 mm trigger, and “?” markers pop over every block. Words of each headline rise in one by one.",
    2: "Brand wipe, then the camera dives under the canopy. Healthy pods turn black with pulsing red rings. Stat cards count up: 30% → 20–30%, three country chips spring in, an 86% donut fills.",
    3: "Rain clears. The competitor map draws itself: axes, then each tool pops in, the empty top-right corner pulses, and KokoShield springs into it.",
    4: "The team’s Field Node CAD model explodes apart and sends a data pulse. The camera rises, blocks recolour by priority, stops 1–4 spring up, the route draws itself and the phone app slides in.",
    5: "The scout reaches block A and found pods glow green. The phone shows the scout log with tap ripples; statuses flip Pending → Confirmed or Ruled out.",
    6: "Top-down route race: two scouts walk at once against a 30-minute clock while find counters tick (demo simulation: 7 vs 2). “Missed by usual round” flags, then the pilot facts check in.",
    7: "Wide drifting shot. Impact cards slide up, money flows sponsor → KokoShield → growers, and farm dots fill from 20 to 60.",
    8: "Golden-hour pull-back over the whole farm with confirmed pods glowing; title and team names, then a closing chime.",
}
SOUND = {
    1: "Rain and two thunder rolls, clock ticks, soft pops, a trigger chime. Music: low, tense minor pad.",
    2: "Rain, rising tick runs on the count-ups, pops for each card and chip.",
    3: "Pops for each tool, a shimmer on the empty corner, a thud and chime as KokoShield lands. Music builds with a riser.",
    4: "Music lifts into a hopeful major theme. Mechanical click, data blips, a rising sweep as the route draws.",
    5: "Bright dings for each confirmed case, a soft thud for the one ruled out.",
    6: "Start beeps, clock ticks, bright dings for ranked finds, duller ones for the usual round, a finish bell, two low buzzes for the misses. Light shaker joins the beat.",
    7: "Whooshes, gentle blips along the money flow, quick ticks as farms fill, a chime.",
    8: "Warm title chime, music resolves and fades.",
}
WHO = {1: "Teoh Xi Xian", 2: "Leow Shen En", 3: "Lee Jia Shern", 4: "Chong Pohyi", 5: "Chong Pohyi", 6: "Choong Zhuo Lin", 7: "Lee Jia Shern", 8: "Teoh Xi Xian"}
def mmss(t): return f"{int(t//60)}:{t%60:04.1f}"

rows = []
for k, s in enumerate(SCENES):
    t0, t1 = S[k], S[k + 1]; mid = t0 + (t1 - t0) * 0.62; th = TH / f"motion{s['id']}.jpg"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{mid:.2f}", "-i", str(VID), "-frames:v", "1", "-vf", "scale=640:-1", str(th)], check=True)
    rows.append(f"""<tr><td class="n">{s['id']}<div class="tc">{mmss(t0)}–{mmss(t1)}<br>{t1 - t0:.1f} s<br>speech ≤ {t1 - t0 - 1.1:.1f} s</div></td>
<td class="th"><img src="{th.resolve().as_uri()}"><div class="st">{s['title']}</div></td>
<td class="os">{MOTION[s['id']]}</td><td class="snd">{SOUND[s['id']]}</td>
<td class="vo">“{html.escape(s['narration'])}”<div class="who">Suggested team voice: {WHO[s['id']]}</div></td></tr>""")

doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>KokoShield Pitch Video Layout</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
@page{{size:A4 landscape;margin:11mm}}
body{{font-family:'Noto Sans','Segoe UI',sans-serif;color:#1f2421;font-size:8.1pt;line-height:1.38;margin:0}}
h1{{font-size:18pt;margin:0 0 2pt;color:#2B654F}} h2{{font-size:11pt;margin:10pt 0 4pt}}
.meta{{color:#5f6b65;margin-bottom:6pt}}
.facts{{display:grid;grid-template-columns:repeat(6,1fr);gap:5pt;margin:6pt 0 8pt}}
.facts div{{background:#eef3ef;border-top:3px solid #2B654F;padding:4pt 6pt;font-size:7.6pt}}
.facts b{{display:block;font-size:9.6pt;color:#2B654F}}
table{{width:100%;border-collapse:collapse}}
th{{background:#2B654F;color:#fff;text-align:left;padding:4pt 5pt;font-size:7.8pt}}
td{{border-bottom:1px solid #d7e0db;padding:4.5pt 5pt;vertical-align:top}} tr{{break-inside:avoid}}
td.n{{width:7%;font-size:14pt;font-weight:700;color:#2B654F}} .tc{{font-size:7.2pt;font-weight:400;color:#5f6b65;margin-top:2pt}}
td.th{{width:21%}} td.th img{{width:100%;border:1px solid #d7e0db;display:block}} .st{{font-weight:700;font-size:8pt;margin-top:2pt}}
td.os{{width:25%}} td.snd{{width:17%;color:#33403a}} td.vo{{width:30%;font-style:italic}} .who{{font-style:normal;color:#2B654F;font-weight:600;font-size:7.2pt;margin-top:3pt}}
.cols{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12pt}} ul{{margin:2pt 0 0;padding-left:13pt}} li{{margin-bottom:2pt}}
code{{background:#eef3ef;padding:0 3pt;font-size:7.6pt}} a{{color:#2B654F}}
</style></head><body>
<h1>KokoShield Pitch Video: Layout and Script (v3)</h1>
<div class="meta">GSC 2026–27 Ignite · Two-minute project overview · 3D motion, natural voice, music and sound effects · Universiti Malaya</div>
<div class="facts">
<div><b>{mmss(S[-1])}</b>Total length (limit 2:00)</div>
<div><b>8 animated scenes</b>Brand wipe between each; captions on screen and as .srt</div>
<div><b>3D farm</b>Rain, lightning, pods, scouts, route race, the team’s Field Node CAD</div>
<div><b>Natural AI voice</b>Microsoft Edge neural voice “Ava”, timed to each scene</div>
<div><b>Music + effects</b>Composed and synthesised in code, synced to on-screen events, dipping under speech</div>
<div><b>Interactive twin</b>Story player, Explore 3D and a “Your turn” challenge</div>
</div>
<table>
<tr><th>Scene / time</th><th>Frame</th><th>What moves on screen</th><th>Sound</th><th>Narration (voice-over script)</th></tr>
{''.join(rows)}
</table>
<h2>Music arc</h2>
<div>Scenes 1–3 sit on a low, tense B-minor pad with sparse marimba under the rain. A riser builds into scene 4, where the solution appears and the music lifts into a hopeful D-major theme with bass and a soft kick. A light shaker drives the scene 6 race, and the score resolves and fades on the closing shot. Music dips about 60% whenever someone speaks.</div>
<h2>Finishing and reusing it</h2>
<div class="cols">
<div><b>1. Optional: your own voices</b><ul>
<li>The AI voice is ready to submit. Real team voices can still feel more personal to judges.</li>
<li>Record one take per scene, reading the script above. Each take must fit its “speech ≤” time.</li>
<li>Save the takes as <code>video/audio/s1.wav</code> … <code>s8.wav</code>.</li></ul></div>
<div><b>2. Rebuild</b><ul>
<li>In the <code>video</code> folder run <code>python voice.py --recordings</code> (or <code>python voice.py</code> for the AI voice).</li>
<li>Then <code>python sound.py</code> to remix music and effects under the new voice.</li>
<li>Then <code>python capture3d.py</code> (about 12 minutes) to render the MP4 again.</li></ul></div>
<div><b>3. Interactive page</b><ul>
<li>Private link: <a href="{LINK}">{LINK}</a>. Share it from the page’s Share menu so others can open it.</li>
<li>Local copy: <code>KokoShield_3D/index.html</code> in Chrome or Edge (internet needed for the 3D library).</li>
<li>Good for the Build-phase live demo: Play the story, Explore 3D to click blocks, or Your turn to plan a route.</li></ul></div>
</div>
<h2>Honesty notes</h2>
<div>The farm, rainfall, pod counts, route race and challenge results are a demo simulation based on the prototype’s preset findings (7 vs 2), labelled on screen. Field results will come from the pilot. The Field Node is shown as a CAD concept. The voice is AI-generated.</div>
</body></html>"""
pathlib.Path("layout.html").write_text(doc, encoding="utf-8")
print("layout.html written, total", mmss(S[-1]))
