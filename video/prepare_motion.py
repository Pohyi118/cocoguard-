"""Rebuild the narration track, subtitles and 3D-page timeline from audio/s1.wav ... s8.wav.
Run this after replacing the placeholder voice with your own recordings, then run capture3d.py."""
import re, json, wave, base64, subprocess, pathlib, imageio_ffmpeg
from scenes import SCENES

FF = imageio_ffmpeg.get_ffmpeg_exe(); LEAD, TAIL = 0.6, 0.9
ROOT = pathlib.Path("C:/Users/User/Documents/GSC")

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"

starts, srt, caps, n = [0.0], [], [], 1
inputs, filt = [], []
for k, sc in enumerate(SCENES):
    i = sc["id"]; w = wave.open(f"audio/s{i}.wav"); a = w.getnframes() / w.getframerate(); w.close()
    d = round(LEAD + a + TAIL, 2); t0 = starts[-1]
    inputs += ["-i", f"audio/s{i}.wav"]
    filt.append(f"[{k}:a]adelay={int(LEAD * 1000)}:all=1,apad,atrim=0:{d},aresample=48000,aformat=channel_layouts=stereo[a{k}]")
    sents = [x.strip() for x in re.split(r'(?<=[.?!])\s+', sc["narration"]) if x.strip()]
    total = sum(len(x) for x in sents); cur = t0 + LEAD
    for x in sents:
        du = a * len(x) / total
        srt.append(f"{n}\n{ts(cur)} --> {ts(cur + du)}\n{x}\n"); caps.append([round(cur, 2), round(cur + du, 2), x]); n += 1; cur += du
    starts.append(round(t0 + d, 2))

filt.append("".join(f"[a{k}]" for k in range(len(SCENES))) + f"concat=n={len(SCENES)}:v=0:a=1[out]")
subprocess.run([FF, "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]",
                "-c:a", "aac", "-b:a", "160k", str(ROOT / "KokoShield_3D/assets/narration.m4a")], check=True)
pathlib.Path("subs.srt").write_text("\n".join(srt), encoding="utf-8")
(ROOT / "KokoShield_Pitch_Video_Subtitles.srt").write_text("\n".join(srt), encoding="utf-8")
glb = base64.b64encode((ROOT / "build/kit/CAD/KokoShield_Field_Node.glb").read_bytes()).decode()
(ROOT / "KokoShield_3D/assets/data.js").write_text(
    "window.KS_STARTS=" + json.dumps(starts) + ";\nwindow.KS_CAPS=" + json.dumps(caps, ensure_ascii=False) + ";\nwindow.KS_GLB=\"" + glb + "\";\n", encoding="utf-8")
print("scene starts:", starts, f"total {starts[-1]:.1f}s")
