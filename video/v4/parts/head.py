"""Soundtrack for the v4 (real-image) video: synthesised score, rain and SFX synced to on-screen events, ducked under the voice."""
import json, wave, subprocess
import numpy as np, imageio_ffmpeg
SR = 48000; FF = imageio_ffmpeg.get_ffmpeg_exe()
S = json.load(open("timeline.json", encoding="utf-8"))["starts"]
END = S[-1]; N = int(END * SR)
rng = np.random.default_rng(11)
T = np.arange(N) / SR

