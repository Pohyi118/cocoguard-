"""Natural voice-over (Microsoft Edge neural TTS) fitted into the 3D timeline's fixed scene slots.
Writes audio/s1..s8.wav, video/voice_track.wav (aligned), subs_v3.srt and updates KS_CAPS in data.js."""
import asyncio, json, re, wave, subprocess, pathlib, shutil
import numpy as np, edge_tts, imageio_ffmpeg
from scenes import SCENES

FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000
VOICE = "en-US-AvaNeural"; LEAD, TAIL = 0.5, 0.6
ROOT = pathlib.Path("C:/Users/User/Documents/GSC")
data_js = (ROOT / "KokoShield_3D/assets/data.js").read_text(encoding="utf-8")
S = json.loads(re.search(r"KS_STARTS=(\[.*?\]);", data_js).group(1))
END = S[-1]
bk = pathlib.Path("audio/zira"); bk.mkdir(exist_ok=True)
for i in range(1, 9):
    src = pathlib.Path(f"audio/s{i}.wav")
    if src.exists() and not (bk / src.name).exists() and "--recordings" not in __import__('sys').argv: shutil.copy(src, bk / src.name)

async def tts(text, rate):
    com = edge_tts.Communicate(text, VOICE, rate=f"{rate:+d}%", boundary="SentenceBoundary")
    audio, sents = b"", []
    async for ch in com.stream():
        if ch["type"] == "audio": audio += ch["data"]
        elif ch["type"] in ("SentenceBoundary", "WordBoundary"): sents.append((ch["offset"] / 1e7, ch["duration"] / 1e7, ch["text"]))
    return audio, sents

def decode(mp3, wav):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", str(SR), wav], check=True)
    w = wave.open(wav); n = w.getnframes(); x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768; w.close()
    return x

track = np.zeros(int(END * SR) + SR, dtype=np.float32); caps = []
import sys
USE_REC = "--recordings" in sys.argv          # use the team's own audio/s1.wav ... s8.wav instead of the AI voice
for k, sc in enumerate(SCENES):
    i = sc["id"]; slot = S[k + 1] - S[k]; window = slot - LEAD - TAIL; rate = 4
    if USE_REC:
        x = decode(f"audio/s{i}.wav", f"audio/_s{i}_48k.wav")
        nz = np.nonzero(np.abs(x) > 0.01)[0]; x = x[max(0, nz[0] - int(0.05 * SR)): nz[-1] + int(0.08 * SR)] if len(nz) else x
        if len(x) / SR > window:                   # gently speed up (max 15%) if a take is too long for its slot
            f = min(1.15, len(x) / SR / window * 1.01)
            sf = f"audio/_s{i}_fit.wav"; pathlib.Path(f"audio/_s{i}_raw.wav").write_bytes(b"")
            w = wave.open(f"audio/_s{i}_raw.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
            x = decode(f"audio/_s{i}_raw.wav", sf) if f <= 1.0 else (subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"audio/_s{i}_raw.wav", "-filter:a", f"atempo={f:.3f}", sf], check=True), decode(sf, sf.replace("fit", "fit2")))[1]
            if len(x) / SR > window: print(f"WARNING scene {i}: recording is {len(x)/SR:.1f}s, slot allows {window:.1f}s; shorten the take")
        dur = len(x) / SR; start = S[k] + LEAD
        track[int(start * SR): int(start * SR) + len(x)] += x[: len(track) - int(start * SR)]
        sents = [z.strip() for z in re.split(r'(?<=[.?!])\s+', sc["narration"]) if z.strip()]; tot = sum(len(z) for z in sents); cur = start
        for z in sents: d = dur * len(z) / tot; caps.append([round(cur, 2), round(cur + d, 2), z]); cur += d
        print(f"scene {i}: slot {slot:.2f}s  recording {dur:.2f}s"); continue
    for attempt in range(4):
        audio, sents = asyncio.run(tts(sc["narration"], rate))
        pathlib.Path(f"audio/s{i}.mp3").write_bytes(audio)
        x = decode(f"audio/s{i}.mp3", f"audio/s{i}.wav")
        nz = np.nonzero(np.abs(x) > 0.004)[0]; x = x[: nz[-1] + int(0.08 * SR)] if len(nz) else x   # trim trailing silence
        dur = len(x) / SR
        if dur <= window or rate >= 28: break
        rate = min(28, int(np.ceil(((1 + rate / 100) * dur / window * 1.02 - 1) * 100)))
    start = S[k] + LEAD
    track[int(start * SR): int(start * SR) + len(x)] += x
    print(f"scene {i}: slot {slot:.2f}s  speech {dur:.2f}s  rate {rate:+d}%  ({len(sents)} sentences)")
    for off, du, txt in sents:
        caps.append([round(start + off, 2), round(start + off + du, 2), txt.strip()])

# keep captions on screen until the next one starts (max +0.6 s) so they don't flicker
for a, b in zip(caps, caps[1:]): a[1] = round(min(b[0] - 0.05, a[1] + 0.6), 2)
track = track[: int(END * SR)]
peak = np.max(np.abs(track)); track *= 0.89 / max(peak, 1e-6)
w = wave.open("voice_track.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(track, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"
srt = "\n".join(f"{n}\n{ts(a)} --> {ts(b)}\n{t}\n" for n, (a, b, t) in enumerate(caps, 1))
pathlib.Path("subs_v3.srt").write_text(srt, encoding="utf-8")
(ROOT / "KokoShield_Pitch_Video_Subtitles.srt").write_text(srt, encoding="utf-8")
data_js = re.sub(r"window\.KS_CAPS=.*?;\n", lambda m: "window.KS_CAPS=" + json.dumps(caps, ensure_ascii=False) + ";\n", data_js, count=1, flags=re.S)
(ROOT / "KokoShield_3D/assets/data.js").write_text(data_js, encoding="utf-8")
print(f"{len(caps)} captions, timeline {END}s")
