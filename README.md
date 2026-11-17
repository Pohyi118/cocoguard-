# KokoShield — GSC 2026–27 Ignite

Weather-guided black pod scouting for smallholder cocoa farms.
Universiti Malaya team: Leow Shen En, Chong Pohyi, Choong Zhuo Lin, Lee Jia Shern, Teoh Xi Xian.
Track: Adaptation & Resilience / Food Resilience.

## Deliverables

| File | What it is |
|---|---|
| `KokoShield_GSC_Ignite_Proposal_v2.pdf` | The proposal (29 pages). The prototype kit (browser app, Bubble embed, Field Node CAD) is attached inside the PDF. |
| `KokoShield_Pitch_Video.mp4` | Two-minute pitch film (1:58.7): four acts, real photos, the real Field Desk app, the Field Node CAD model in 3D, drone survey concept, music and effects. |
| `KokoShield_Pitch_Video_Layout.pdf` | Storyboard: every beat with timing, visuals, sound and narration. |
| `KokoShield_Video_Photo_Credits.txt` | Licences and sources for every photo used in the video. |
| `KokoShield_Interactive/` | Interactive version of the pitch: play the story, explore the farm map, fly the drone survey, plan a scouting round. Open `index.html` in Chrome or Edge. |
| `KokoShield_GSC_Ignite_Proposal.pdf` | Original proposal before revision. |

## How the pieces were built

- `build/` — proposal source (`proposal.html`), figure images and the scripts that patch and renumber it. Print to PDF with headless Edge; see `add_drone.py` for the last edit.
- `video/v5/` — the current pitch video pipeline: `voice_v5.py` (narration) → `make_sound_v5.py` + `sound_v5.py` (score and effects) → `capture_v5.py` (render). `stage/real.html` is the composition; `stage/node3d.html` renders the Field Node CAD model.
- `video/v4/`, `video/` — earlier pipelines (real-image cut, 3D farm cut, slides cut).
- `KokoShield_3D/` — the earlier three.js animated farm (superseded, kept for reference).

Large intermediates (old video versions, WAV mixes, render frames, the extracted prototype kit) are not in the repo; see `.gitignore`.

## Honesty notes

The farm map, route race, counts and drone survey are a demo simulation on the prototype's demo farm. The Field Node is a CAD concept, not yet built. Photos are free-licensed Wikimedia Commons images of cocoa farming elsewhere, not the pilot farm. The narration voice is AI-generated.
