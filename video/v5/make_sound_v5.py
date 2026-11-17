import pathlib
src = pathlib.Path("../sound.py").read_text(encoding="utf-8")
inst = src[src.index("def sm(x)"): src.index("# ---------------- score ----------------")]
sfxlib = src[src.index("# ---------------- SFX library ----------------"): src.index("def at(t, sig, g, pan=0.0)")]
mix = src[src.index("# ---------------- mix with ducking ----------------"):]
mix = (mix.replace('wave.open("voice_track.wav")', 'wave.open("voice_track_v5.wav")').replace('np.savez_compressed("mixparts.npz"', 'np.savez_compressed("mixparts_v5.npz"')
          .replace('wave.open("soundtrack.wav", "wb")', 'wave.open("soundtrack_v5.wav", "wb")')
          .replace('subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack.wav", "-c:a", "aac", "-b:a", "192k", str(ROOT / "KokoShield_3D/assets/soundtrack.m4a")], check=True)',
                   'subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack_v5.wav", "-c:a", "aac", "-b:a", "192k", "soundtrack_v5.m4a"], check=True)')
          .replace("music_gain = (0.42 * (1 - 0.60 * duck))", "music_gain = (0.48 * (1 - 0.58 * duck))"))
assert "soundtrack_v5.m4a" in mix
head = '''"""Soundtrack for the v5 cinematic video: four-act score, rain and SFX synced to on-screen events, ducked under the voice."""
import json, wave, subprocess
import numpy as np, imageio_ffmpeg
SR = 48000; FF = imageio_ffmpeg.get_ffmpeg_exe()
_tl = json.load(open("timeline.json", encoding="utf-8")); S = _tl["starts"]; END = _tl["end"]; N = int(END * SR)
rng = np.random.default_rng(11); T = np.arange(N) / SR
'''
out = head + inst + pathlib.Path("parts/score5.py").read_text(encoding="utf-8") + sfxlib + pathlib.Path("parts/extra_sfx.py").read_text(encoding="utf-8") + pathlib.Path("parts/cues5.py").read_text(encoding="utf-8") + mix
pathlib.Path("sound_v5.py").write_text(out, encoding="utf-8"); print("sound_v5.py written")
