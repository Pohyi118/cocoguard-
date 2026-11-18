Flow keyframes cut from prototype/assets/farm_aerial_source.png (1536x1024).
shot1_last_farm_16x9.png  = crop (x0,y0,x1,y1) = (0,80,1536,944). Last frame of shot 1.
  Overlay mapping: video_px = (src_x, src_y - 80) * (W/1536). Zone polygons in prototype coords shift up 80 px.
shot3_first_stream.png    = crop (560,270,1360,720) scaled x1.6 to 1280x720. First frame of shot 3.
Both frames are AI-generated imagery: label "illustrative farm, not the pilot site".
shot1_first_oblique.jpeg  = Nano Banana still (ref: shot1_last_farm_16x9.png), first frame of shot 1.
  Flow refuses a clip with a last frame and no first frame, hence this still.

Clips (Omni 1.1 Flash, 8 s, 720p, 24 fps) in ../flow_clips:
shot1_descent_to_aerial.mp4  oblique misty view descends/tilts to top-down; near-still from 6.4 s.
  Final frame matches shot1_last_farm_16x9.png (mean abs diff 9.6/255); draw the zone overlay from ~6.5 s.
  Mid-move the blocks read as a tidier grid and ease into the real shapes; no hard morph.
shot3_stream_drainage.mp4    starts on shot3_first_stream.png, travels down the stream past the crop
  into invented farm; brown water and pools by the block edge. Cutaway only, NOT overlay-aligned.

Batch 2 (2026-11-17), all checked frame by frame:
farmer1_after_storm.mp4    8 s  ~14 s beat. Pak_Farmer walks out beside the shed, stops, looks across blocks.
farmer2_he_goes.mp4        8 s  "He goes" ~52 s. Walks straight away down a cocoa row through puddles.
pod_black_pod_closeup.mp4  4 s  ~78 s. Brown rot spreading from the tip (ref: 13_black_pod.jpg). First take rejected (crater-like lesion).
farmer3_find_photo.mp4     8 s  ~80 s. Frames the pod with his phone, frowns, nods. Hands steady.
drone_closeup_flyaway.mp4  8 s  ~38.7 s "borrowed drone". Hovers, then flies away toward hills.
drone_topdown_pass.mp4     8 s  top-down, camera locked; drone crosses left to right over the top blocks and the stream. Made manually in Flow 2026-11-18 (first frame drone_topdown_first.jpeg). Background static, drone shape stable.
Farmer is fictional and AI-generated: label on screen + credits file.
