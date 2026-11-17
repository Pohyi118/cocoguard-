# KokoShield — GSC 2026–27 Ignite

Weather-guided black pod scouting for smallholder cocoa farms.
Universiti Malaya team: Leow Shen En, Chong Pohyi, Choong Zhuo Lin, Lee Jia Shern, Teoh Xi Xian.
Track: Adaptation & Resilience / Food Resilience.

## Deliverables

| File | What it is |
|---|---|
| `KokoShield_GSC_Ignite_Proposal_v3.pdf` | The proposal (20 pages): product first, one Built / Tested / Pending table, real prototype screenshots. The prototype HTML and Field Node CAD files are attached inside the PDF. |
| `KokoShield_GSC_Ignite_Proposal_v2.pdf` | The previous 29-page proposal. |
| `KokoShield_Pitch_Video.mp4` | Two-minute pitch film (1:59): four acts, real stock footage and photos, real footage of the Field Desk prototype (`prototype/`) on laptop and phone, the Field Node CAD model in 3D, drone survey concept, music and effects. |
| `KokoShield_Pitch_Video_Layout.pdf` | Storyboard: every beat with timing, visuals, sound and narration. |
| `KokoShield_Video_Photo_Credits.txt` | Licences and sources for every photo used in the video. |
| `KokoShield_Interactive/` | Interactive version of the pitch: play the story, explore the farm map, fly the drone survey, plan a scouting round. Open `index.html` in Chrome or Edge. |
| `KokoShield_GSC_Ignite_Proposal.pdf` | Original proposal before revision. |

## How the pieces were built

- `build/v3/` — proposal v3 source: `capture_app.py` (real screenshots of `prototype/`), `charts.py` and `make_v3.py` (writes `proposal_v3.html`), `check_v3.py` (overflow check). Print with headless Edge, then attach the prototype and CAD zip.
- `build/` — the v2 proposal source (`proposal.html`) and its patch scripts.
- `video/v7/` — the current pitch video pipeline: `fetch_footage.py` + `extract_footage.py` (Pexels footage), `record_proto.py` (prototype footage), `patch_v7.py` + `build_page.py` (composition), then `voice_v5.py` → `restretch.py` → `make_sound_v5.py` + `sound_v5.py` → `capture_v5.py`.
- `video/v6/` — the previous pipeline (prototype footage, no stock footage)
- `video/v5/` — the previous pipeline: `voice_v5.py` (narration) → `make_sound_v5.py` + `sound_v5.py` (score and effects) → `capture_v5.py` (render). `stage/real.html` is the composition; `stage/node3d.html` renders the Field Node CAD model.
- `video/v4/`, `video/` — earlier pipelines (real-image cut, 3D farm cut, slides cut).
- `KokoShield_3D/` — the earlier three.js animated farm (superseded, kept for reference).

Large intermediates (old video versions, WAV mixes, render frames, the extracted prototype kit) are not in the repo; see `.gitignore`.

## Honesty notes

The farm map, route race, counts and drone survey are a demo simulation on the prototype's demo farm. The Field Node is a CAD concept, not yet built. Photos are free-licensed Wikimedia Commons images of cocoa farming elsewhere, not the pilot farm. The narration voice is AI-generated.
