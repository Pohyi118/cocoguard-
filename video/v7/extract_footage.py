"""Cut the approved Pexels clips into 30 fps 1920x1080 JPEG sequences under stage/assets/vid/<segment>/."""
import subprocess, pathlib, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe(); HERE = pathlib.Path(__file__).parent
SEG = {  # segment: (clip, start s, duration s)
    "rain1": ("rain_plantation", 0.0, 5.0), "rainleaf": ("rain_leaves", 2.0, 5.2), "ghana": ("farmer_ghana", 0.0, 6.6),
    "orchard_a": ("walk_orchard", 0.0, 11.6), "leafbg": ("rain_leaves", 8.0, 11.6), "aerialbg": ("aerial_farm", 0.0, 16.2),
    "orchard_b": ("walk_orchard", 14.0, 10.6), "path_a": ("walk_path", 0.0, 10.6), "podbg": ("cacao_pod", 0.0, 8.6),
    "aerial_v": ("aerial_farm", 18.0, 4.8), "path_end": ("walk_path", 11.0, 16.0)}
for name, (clip, ss, dur) in SEG.items():
    d = HERE / "stage/assets/vid" / name; d.mkdir(parents=True, exist_ok=True)
    for f in d.glob("*.jpg"): f.unlink()
    subprocess.run([FF, "-loglevel", "error", "-ss", str(ss), "-t", str(dur), "-i", str(HERE / "footage" / f"{clip}.mp4"),
                    "-vf", "fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080", "-q:v", "3", str(d / "f%04d.jpg")], check=True)
    print(name, len(list(d.glob("*.jpg"))))
