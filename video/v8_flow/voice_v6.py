"""Voice the v6 script with Edge neural TTS (en-US-AvaMultilingualNeural), one take per scene, keeping word times.
Scene length = lead + speech + tail. One shared rate is nudged faster until the film fits LIMIT seconds.
Outputs: audio/s<id>.wav (48 kHz mono), voice_v6.wav, timeline.json {starts, end, scenes:[{id,start,speech_at,words:[[t0,t1,word]]}]}"""
import asyncio, json, pathlib, subprocess, time, wave
import numpy as np, edge_tts, imageio_ffmpeg
from scenes_v6 import SCENES

FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000; VOICE = "en-US-AndrewMultilingualNeural"; LIMIT = 119.6
A = pathlib.Path("audio"); A.mkdir(exist_ok=True)


async def tts(text, rate):
    com = edge_tts.Communicate(text, VOICE, rate=f"{rate:+d}%", boundary="WordBoundary")
    audio, words = b"", []
    async for ch in com.stream():
        if ch["type"] == "audio": audio += ch["data"]
        elif ch["type"] == "WordBoundary": words.append([ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]])
    return audio, words


def voice(text, rate):
    for k in range(5):
        try: return asyncio.run(asyncio.wait_for(tts(text, rate), 30))
        except Exception as e: print("  retry", k, type(e).__name__); time.sleep(2 + 2 * k)
    raise RuntimeError("edge-tts failed")


def load(mp3):
    wav = mp3.with_suffix(".tmp.wav")
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-ar", str(SR), str(wav)], check=True)
    w = wave.open(str(wav)); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; w.close(); wav.unlink()
    nz = np.nonzero(np.abs(x) > 0.004)[0]; a = max(0, nz[0] - int(0.02 * SR))
    return x[a: nz[-1] + int(0.12 * SR)], a / SR


def save(path, x):
    w = wave.open(str(path), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()


rate = 0
while True:
    takes = []
    for sc in SCENES:
        audio, words = voice(sc["text"], rate + sc.get("dr", 0)); mp3 = A / f"s{sc['id']}.mp3"; mp3.write_bytes(audio)
        x, trim = load(mp3); takes.append((x, [[round(a - trim, 3), round(b - trim, 3), w] for a, b, w in words]))
    total = sum(sc["lead"] + len(x) / SR + sc["tail"] for sc, (x, _) in zip(SCENES, takes))
    print(f"rate {rate:+d}%: {total:.1f}s")
    if total <= LIMIT or rate >= 9: break
    rate += 2

starts, scenes, t = [], [], 0.0
track = np.zeros(int((total + 1) * SR), np.float32)
for sc, (x, words) in zip(SCENES, takes):
    s0 = t + sc["lead"]; track[int(s0 * SR): int(s0 * SR) + len(x)] += x; save(A / f"s{sc['id']}.wav", x)
    scenes.append(dict(id=sc["id"], title=sc["title"], start=round(t, 3), speech_at=round(s0, 3), speech_len=round(len(x) / SR, 3),
                       end=round(s0 + len(x) / SR + sc["tail"], 3), words=words))
    starts.append(round(t, 3)); t = s0 + len(x) / SR + sc["tail"]
    print(f"s{sc['id']} {sc['title']:<20} {scenes[-1]['start']:6.2f} -> {scenes[-1]['end']:6.2f}")
track = track[: int(t * SR)]; track *= 0.9 / np.max(np.abs(track)); save("voice_v6.wav", track)
json.dump(dict(voice=VOICE, rate=rate, starts=starts, end=round(t, 3), scenes=scenes), open("timeline.json", "w"), indent=1)
print(f"END {t:.2f}s")
