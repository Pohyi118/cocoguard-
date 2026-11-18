# KokoShield pitch video, v8

A film just under two minutes that follows one cocoa farmer through one storm. A Flow time-lapse of a pod growing from flower to ripe fruit and the storm open it, then real photos of black pod and the 20-30% loss figure. Then the farmer's question ("But where should he start?"), the KokoShield reveal, the clues it combines (drone, the 3D-printed Field Node, rain gauge, past outbreaks), the 30-minute plan, the walk and the find. After that comes a race on one map: the usual round, a rewind, then the KokoShield route, then a scoreboard, and the ending: the pilot in Tanjung Sepat on a map of Malaysia, and the logo.

The narration is written to be heard: plain words, short sentences, one question per beat (TED-Ed style).

## Files

| File | What it is |
|---|---|
| `work/KokoShield_v8_subs.mp4` | Main film, subtitles burned in (copied to the repo root as `KokoShield_Pitch_Video_Flow.mp4`) |
| `work/KokoShield_v8_clean.mp4` | Same film without subtitles |
| `work/KokoShield_v8_bed.mp4` | No voice, sound effects and ambience at -25 LUFS, for recording a human narration over it |
| `KokoShield_Pitch_v8.srt` | Subtitles (also at the repo root) |
| `credits_v6.txt` | Sources and credits for this cut (also at the repo root) |

## What is real and what is illustrative

- **App footage is real.** Every app shot is a full-screen recording of `prototype/KokoShield_Prototype.html` with its demo data. The race (`race/`) is drawn from the app's own Compare maps, routes and find times, and is labelled "Demo data from the KokoShield prototype".
- **The farm, farmer, storm and drone are AI-generated** with Google Flow and labelled on screen. The farm footage starts from or lands on the app's own aerial image, so the drone descent lands exactly on the app's map, and the race begins from the same view.
- **The Field Node** is rendered from the team's CAD model (`node/`) and labelled "concept prototype".
- **The black pod photos are real** (Scot Nelson, CC0, Wikimedia Commons).
- **The map** uses Natural Earth outlines (public domain).
- **The voice is AI-generated** (Edge `en-US-AndrewMultilingualNeural`, rate +4% overall, with the first two lines slowed (-12% and -22%) for a calmer opening).

## Rebuild

From `video/v8_flow`:

1. `python rec_v6.py` records the prototype clips into `rec/`.
2. `python voice_v6.py` voices `scenes_v6.py` and writes `timeline.json` with word times.
3. `python node/render_node.py` renders the Field Node frames. `python race/build_race2.py` renders `rec/race.mp4` (timed from `timeline.json`).
4. Once: `ffmpeg -i ../v5/flow_clips/shot1_descent_to_aerial.mp4 -vf reverse -an work/shot1_reversed.mp4` (the pull-back in the ending). Then `python compose_v7.py` renders `work/film_clean.mp4` and `work/film_subs.mp4`. Use `--sheet 12 52.5 80` to preview single frames.
5. `python sound_v7.py` places the CC0 sound effects (`sfx/`), ambience, birdsong, rain and thunder, and writes the mix (-16 LUFS) plus the -25 LUFS bed.
6. Mux each video with `work/mix.wav` (or `work/mix_bed.wav`) using ffmpeg with `-c:v copy`.

Every cut and overlay is tied to a spoken word (`wt(scene, "word")`), so a script change only needs steps 2 to 6. No background music, by choice: the story is carried by ambience and sound effects. The opening time-lapse is `video/v5/flow_clips/growth_timelapse_smooth.mp4` (built from the three `growth_*` clips, evenly paced and frame-blended). The Flow clips are in `video/v5/flow_clips` and `C:\Users\user\flow-mcp-out\KokoShield_v7` (healthy pod, storm).
