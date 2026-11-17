"""Render every frame of stage/real.html and encode with the v4 soundtrack and captions."""
import sys, time, socket, subprocess, json, imageio_ffmpeg
from playwright.sync_api import sync_playwright
FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS = 30
ROOT = "C:/Users/User/Documents/GSC/video/v4"
srv = None
if socket.socket().connect_ex(("127.0.0.1", 8766)) != 0:
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8766", "--bind", "127.0.0.1"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.5)
END = json.load(open(ROOT + "/timeline.json", encoding="utf-8"))["starts"][-1]; n = int(END * FPS)
TMP = ROOT + "/v4_noaudio.mp4"
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto("http://127.0.0.1:8766/stage/real.html"); pg.wait_for_function("window.KS_READY !== undefined"); pg.evaluate("window.KS_READY")
    enc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                            "-vf", "scale=in_range=full:out_range=limited:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", TMP], stdin=subprocess.PIPE)
    t0 = time.time()
    for i in range(n):
        pg.evaluate(f"window.renderAt({i / FPS})"); enc.stdin.write(pg.screenshot(type="jpeg", quality=92))
        if i % 600 == 0: print(f"frame {i}/{n} {time.time() - t0:.0f}s", flush=True)
    enc.stdin.close(); enc.wait(); b.close()
OUT = "C:/Users/User/Documents/GSC/KokoShield_Pitch_Video.mp4"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", TMP, "-i", ROOT + "/soundtrack_v4.m4a", "-i", ROOT + "/subs_v4.srt", "-map", "0:v", "-map", "1:a", "-map", "2",
                "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-t", f"{END:.2f}", "-movflags", "+faststart", OUT], check=True)
if srv: srv.terminate()
print("done", OUT, f"{time.time() - t0:.0f}s")
