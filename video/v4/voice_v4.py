"""Natural voice-over for v4 (Edge neural voice 'Ava'). Scene lengths follow the speech, and one shared speaking
rate is raised (max +16%) until the whole video fits in 119.6 s. Use --recordings to use the team's own
audio/s1.wav ... s9.wav instead (scene lengths then follow those takes).
Outputs: audio/s*.wav, voice_track_v4.wav, timeline.json (scene starts + captions), subs_v4.srt"""
import asyncio, json, re, sys, wave, subprocess, pathlib
import numpy as np, edge_tts, imageio_ffmpeg
from scenes_v4 import SCENES

FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000; VOICE = "en-US-AvaNeural"
LEAD, TAIL, LIMIT = 0.45, 0.6, 119.6
A = pathlib.Path("audio"); A.mkdir(exist_ok=True)
USE_REC = "--recordings" in sys.argv

async def tts(text, rate):
    com = edge_tts.Communicate(text, VOICE, rate=f"{rate:+d}%", boundary="SentenceBoundary")
    audio, sents = b"", []
    async for ch in com.stream():
        if ch["type"] == "audio": audio += ch["data"]
        elif ch["type"] in ("SentenceBoundary", "WordBoundary"): sents.append((ch["offset"] / 1e7, ch["duration"] / 1e7, ch["text"].strip()))
    return audio, sents

def load(path):
    out = str(path) + ".48k.wav"
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), out], check=True)
    w = wave.open(out); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; w.close()
    nz = np.nonzero(np.abs(x) > 0.006)[0]
    return x[max(0, nz[0] - int(0.03 * SR)): nz[-1] + int(0.08 * SR)] if len(nz) else x

def split_sents(text): return [z.strip() for z in re.split(r'(?<=[.?!;:])\s+', text) if z.strip()]

rate = 6
for attempt in range(6):
    clips = []
    for sc in SCENES:
        i = sc["id"]
        if USE_REC:
            x = load(A / f"s{i}.wav"); d = len(x) / SR; tot = sum(len(z) for z in split_sents(sc["narration"])); acc = 0; sents = []
            for z in split_sents(sc["narration"]): sents.append((acc / tot * d, len(z) / tot * d, z)); acc += len(z)
        else:
            audio, sents = asyncio.run(tts(sc["narration"], rate)); (A / f"s{i}.mp3").write_bytes(audio); x = load(A / f"s{i}.mp3")
        clips.append((x, sents))
    total = sum(LEAD + len(x) / SR + TAIL for x, _ in clips)
    print(f"rate {rate:+d}%  total {total:.1f}s")
    if total <= LIMIT or USE_REC or rate >= 16: break
    rate = min(16, rate + max(2, int(np.ceil((total / LIMIT - 1) * 100 * 1.15))))

starts, caps, track = [0.0], [], np.zeros(int(130 * SR), np.float32)
for (x, sents), sc in zip(clips, SCENES):
    t0 = starts[-1]; s0 = t0 + LEAD
    track[int(s0 * SR): int(s0 * SR) + len(x)] += x
    for off, du, txt in sents: caps.append([round(s0 + off, 2), round(s0 + off + du, 2), txt])
    if not USE_REC:
        w = wave.open(str(A / f"s{sc['id']}.wav"), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    starts.append(round(t0 + LEAD + len(x) / SR + TAIL, 2))
    print(f"scene {sc['id']}: {starts[-2]:6.2f} -> {starts[-1]:6.2f}  speech {len(x)/SR:5.2f}s")
for a, b in zip(caps, caps[1:]): a[1] = round(min(b[0] - 0.05, a[1] + 0.6), 2)
END = starts[-1]; track = track[: int(END * SR)]; track *= 0.89 / max(1e-6, np.max(np.abs(track)))
w = wave.open("voice_track_v4.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(track, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
json.dump({"starts": starts, "caps": caps, "names": [s["title"] for s in SCENES]}, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False)
def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"
pathlib.Path("subs_v4.srt").write_text("\n".join(f"{n}\n{ts(a)} --> {ts(b)}\n{t}\n" for n, (a, b, t) in enumerate(caps, 1)), encoding="utf-8")
print(f"END {END:.2f}s, {len(caps)} captions")
