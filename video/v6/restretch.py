"""Insert silent holds before each scene's voice (for visuals to breathe) and an end-card tail.
Run right after voice_v5.py. Rewrites voice_track_v5.wav, timeline.json, subs_v5.srt and stage/data_v5.js."""
import json, wave, pathlib
import numpy as np
SR = 48000
HOLD = {1: 5.0, 2: 1.0, 3: 4.0, 4: 0.8, 5: 1.0, 6: 2.6, 7: 2.6, 8: 1.6, 9: 1.0}
TAIL = 5.6
NAMES = ["Storm", "Thirty minutes", "Activation", "The route", "Field Node", "The race", "The find", "Vision", "The ask"]
tl = json.load(open("timeline.json", encoding="utf-8")); S = tl["starts"]; caps = tl["caps"]
w = wave.open("voice_track_v5.wav"); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; w.close()
segs, off = [], 0.0
for i in range(9): off += HOLD[i + 1]; segs.append((S[i], S[i + 1], S[i] + off))
END = round(segs[-1][2] + (segs[-1][1] - segs[-1][0]) + TAIL, 2)
assert END <= 119.6, END
out = np.zeros(int(END * SR), np.float32)
for o0, o1, n0 in segs:
    a, b, c = int(o0 * SR), int(o1 * SR), int(n0 * SR); seg = v[a:b]; out[c:c + len(seg)] = seg
nc = []
for a, b, t in caps:
    for o0, o1, n0 in segs:
        if o0 - 0.01 <= a < o1: nc.append([round(a - o0 + n0, 2), round(b - o0 + n0, 2), t]); break
w = wave.open("voice_track_v5.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
starts = [0.0] + [round(segs[i][2] + (segs[i][1] - segs[i][0]), 2) for i in range(8)] + [END]
new = {"starts": starts, "voice_at": [round(n0, 2) for _, _, n0 in segs], "caps": nc, "names": NAMES, "end": END}
json.dump(new, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False)
def ts(t):
    m, s = divmod(t, 60); return f"00:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
open("subs_v5.srt", "w", encoding="utf-8").write("\n".join(f"{n}\n{ts(a)} --> {ts(b)}\n{t}\n" for n, (a, b, t) in enumerate(nc, 1)))
d = pathlib.Path("stage/data_v5.js").read_text(encoding="utf-8"); K = json.loads(d[d.index("=") + 1:].rstrip().rstrip(";"))
new["credits"] = K["credits"]
pathlib.Path("stage/data_v5.js").write_text("window.KS5=" + json.dumps(new, ensure_ascii=False) + ";\n", encoding="utf-8")
print("starts", starts); print("voice_at", new["voice_at"]); print("END", END)
for c in nc: print(c)
