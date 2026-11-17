"""Download the approved Pexels clips (Pexels License) and record credits."""
import json, urllib.request, pathlib, time
UA = {"User-Agent": "ImageSearchScript/1.0 (educational research; python urllib)"}
CLIPS = [  # (local name, pexels file, title, creator, page)
 ("rain_plantation", "34411622/14577736_1920_1080_60fps.mp4", "Lush tropical banana plantation in rain", "Nothing Ahead", "lush-tropical-banana-plantation-in-rain-34411622"),
 ("rain_leaves", "32089669/13678860_1920_1080_24fps.mp4", "Tropical rainfall on banana leaves in slow motion", "Srinivas Kashyap", "tropical-rainfall-on-banana-leaves-in-slow-motion-32089669"),
 ("cacao_pod", "8505961/8505961-hd_1920_1080_30fps.mp4", "A cacao fruit on a tree", "Frank Meriño", "a-cacao-fruit-on-a-tree-8505961"),
 ("pod_open", "3995569/3995569-hd_1920_1080_30fps.mp4", "Chocolate fruit, Philippines", "Joey D.", "chocolate-fruit-tasty-philippines-3995569"),
 ("farmer_ghana", "31283621/13359004_1920_1080_50fps.mp4", "Rural cocoa farmer drying beans in Ghana", "Zeal Creative Studios", "rural-cocoa-farmer-drying-beans-in-ghana-31283621"),
 ("walk_rows", "13325421/13325421-hd_1920_1080_30fps.mp4", "Walking in a rubber tree plantation", "naratip sretan", "walking-in-a-rubber-tree-plantation-13325421"),
 ("walk_orchard", "5018897/5018897-hd_1920_1080_30fps.mp4", "Man walking on a mango farm", "Prodèép Nëpalënsis", "man-walking-on-a-mango-farm-5018897"),
 ("walk_harvest", "36681147/15550237_1080_1920_30fps.mp4", "Rural farmer carrying harvest in tropical setting", "Souhityo Das", "rural-farmer-carrying-harvest-in-tropical-setting-36681147"),
 ("aerial_farm", "15678785/15678785-hd_1920_1080_24fps.mp4", "An aerial view of a farm with trees and houses", "Serg Alesenko", "an-aerial-view-of-a-farm-with-trees-and-houses-15678785"),
 ("farmers_work", "12540973/12540973-hd_1080_1920_24fps.mp4", "A couple of farmers harvesting crops by hand", "Asad Photo Maldives", "a-couple-of-farmers-harvesting-crops-by-hand-12540973"),
 ("walk_path", "17190661/17190661-hd_1920_1080_24fps.mp4", "A person walking down a dirt path in a field", "Ucundinamarca Virtual", "a-person-walking-down-a-dirt-path-in-a-field-17190661"),
]
out = pathlib.Path("footage"); cred = []
for name, f, title, who, page in CLIPS:
    dst = out / f"{name}.mp4"
    if not dst.exists():
        with urllib.request.urlopen(urllib.request.Request("https://videos.pexels.com/video-files/" + f, headers=UA), timeout=120) as r: dst.write_bytes(r.read())
        time.sleep(0.5)
    print(f"{dst.stat().st_size/1e6:6.1f} MB {dst.name}")
    cred.append(dict(file=dst.name, title=title, author=who, license="Pexels License", source="https://www.pexels.com/video/" + page + "/"))
json.dump(cred, open("footage/credits.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
