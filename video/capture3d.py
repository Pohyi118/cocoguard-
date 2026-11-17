"""Capture every frame of the 3D motion page (video mode) and encode with narration + subtitles."""
import subprocess, time, imageio_ffmpeg
from playwright.sync_api import sync_playwright
FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS = 30
URL = "http://127.0.0.1:8765/index.html?mode=video"
TMP = "C:/Users/User/Documents/GSC/video/motion_noaudio.mp4"
import socket, sys
srv = None
if socket.socket().connect_ex(("127.0.0.1", 8765)) != 0:   # start a local server for the 3D page if none is running
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1"],
                           cwd="C:/Users/User/Documents/GSC/KokoShield_3D", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--enable-webgl", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(URL); pg.wait_for_function("window.KS_READY !== undefined", timeout=60000); pg.evaluate("window.KS_READY")
    end = pg.evaluate("window.KS_STARTS[8]"); n = int(end * FPS)
    enc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                            "-vf", "scale=in_range=full:out_range=limited:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", TMP], stdin=subprocess.PIPE)
    t0 = time.time()
    for i in range(n):
        pg.evaluate(f"window.renderAt({i / FPS})")
        enc.stdin.write(pg.screenshot(type="jpeg", quality=92))
        if i % 300 == 0: print(f"frame {i}/{n}  {time.time() - t0:.0f}s", flush=True)
    enc.stdin.close(); enc.wait(); b.close()
OUT = "C:/Users/User/Documents/GSC/KokoShield_Pitch_Video.mp4"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", TMP, "-i", "C:/Users/User/Documents/GSC/KokoShield_3D/assets/soundtrack.m4a",
                "-i", "C:/Users/User/Documents/GSC/video/subs_v3.srt", "-map", "0:v", "-map", "1:a", "-map", "2", "-c:v", "copy", "-c:a", "copy",
                "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-t", f"{end:.2f}", "-movflags", "+faststart", OUT], check=True)
if srv: srv.terminate()
print("done", OUT, f"{time.time() - t0:.0f}s")
