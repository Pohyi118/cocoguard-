"""Builds sound_v4.py from the v3 instrument/SFX library plus v4 timing, score and cues, then you run sound_v4.py."""
import pathlib
src = pathlib.Path("../sound.py").read_text(encoding="utf-8")
inst = src[src.index("def sm(x)"): src.index("# ---------------- score ----------------")]
sfxlib = src[src.index("# ---------------- SFX library ----------------"): src.index("def at(t, sig, g, pan=0.0)")]
mix = src[src.index("# ---------------- mix with ducking ----------------"):]
mix = (mix.replace('w = wave.open("voice_track.wav")', 'w = wave.open("voice_track_v4.wav")')
          .replace('np.savez_compressed("mixparts.npz"', 'np.savez_compressed("mixparts_v4.npz"')
          .replace('w = wave.open("soundtrack.wav", "wb")', 'w = wave.open("soundtrack_v4.wav", "wb")')
          .replace('subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack.wav", "-c:a", "aac", "-b:a", "192k", str(ROOT / "KokoShield_3D/assets/soundtrack.m4a")], check=True)',
                   'subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack_v4.wav", "-c:a", "aac", "-b:a", "192k", "soundtrack_v4.m4a"], check=True)'))
assert "voice_track_v4" in mix and "soundtrack_v4.m4a" in mix
head = pathlib.Path("parts/head.py").read_text(encoding="utf-8")
score = pathlib.Path("parts/score.py").read_text(encoding="utf-8")
extra = pathlib.Path("parts/extra_sfx.py").read_text(encoding="utf-8")
cues = pathlib.Path("parts/cues.py").read_text(encoding="utf-8")
pathlib.Path("sound_v4.py").write_text(head + inst + score + sfxlib + extra + cues + mix, encoding="utf-8")
print("sound_v4.py written")
