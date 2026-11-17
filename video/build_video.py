"""Assemble the pitch video: each scene image with a gentle zoom and fades, narration with a short
lead-in, soft subtitles, plus a standalone SRT. Output: GSC/KokoShield_Pitch_Video.mp4."""
import re, subprocess, wave, pathlib, imageio_ffmpeg
from scenes import SCENES

FF = imageio_ffmpeg.get_ffmpeg_exe()
LEAD, TAIL, FPS = 0.6, 0.9, 30
seg_dir = pathlib.Path("segments"); seg_dir.mkdir(exist_ok=True)

def run(args):
    r = subprocess.run([FF, "-y", "-loglevel", "error", *args], capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"

srt, t0, n = [], 0.0, 1
for sc in SCENES:
    i = sc["id"]
    w = wave.open(f"audio/s{i}.wav"); a = w.getnframes() / w.getframerate(); w.close()
    d = round(LEAD + a + TAIL, 2); frames = int(d * FPS)
    vf = (f"scale=3840:2160,zoompan=z='min(1+0.035*on/{frames},1.035)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d={frames}:s=1920x1080:fps={FPS},fade=t=in:st=0:d=0.35,fade=t=out:st={d-0.35:.2f}:d=0.35,format=yuv420p")
    run(["-loop", "1", "-framerate", str(FPS), "-i", f"frames/scene{i}.png", "-i", f"audio/s{i}.wav",
         "-filter_complex", f"[0:v]{vf}[v];[1:a]adelay={int(LEAD*1000)}:all=1,apad,atrim=0:{d},aresample=48000,aformat=channel_layouts=stereo[a]",
         "-map", "[v]", "-map", "[a]", "-t", str(d), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "aac", "-b:a", "160k", str(seg_dir / f"seg{i}.mp4")])
    # subtitles: split narration into sentences, time by character share of the audio span
    sents = [x.strip() for x in re.split(r'(?<=[.?!])\s+', sc["narration"]) if x.strip()]
    total = sum(len(x) for x in sents); cur = t0 + LEAD
    for x in sents:
        dur = a * len(x) / total
        srt.append(f"{n}\n{ts(cur)} --> {ts(cur + dur)}\n{x}\n"); n += 1; cur += dur
    print(f"scene {i}: {d:.1f}s  ({t0:.1f}-{t0+d:.1f})"); t0 += d

pathlib.Path("subs.srt").write_text("\n".join(srt), encoding="utf-8")
pathlib.Path("list.txt").write_text("".join(f"file 'segments/seg{s['id']}.mp4'\n" for s in SCENES))
out = "C:/Users/User/Documents/GSC/KokoShield_Pitch_Video.mp4"
run(["-f", "concat", "-safe", "0", "-i", "list.txt", "-i", "subs.srt", "-map", "0", "-map", "1",
     "-c", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-movflags", "+faststart", out])
pathlib.Path("C:/Users/User/Documents/GSC/KokoShield_Pitch_Video_Subtitles.srt").write_text("\n".join(srt), encoding="utf-8")
print(f"total {t0:.1f}s -> {out}")
