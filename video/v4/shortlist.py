"""Resolve 1920-px versions of the shortlisted Commons files and read their sizes with HEAD requests (no downloads)."""
import json, re, time, urllib.parse, urllib.request, urllib.error
UA = {"User-Agent": "ImageSearchScript/1.0 (educational research; python urllib)"}
TITLES = [
 ("hook/close", "Cacao farm, Can Tho (32240062548).jpg"), ("hook/close", "Cacao farm, Can Tho (45199902095).jpg"),
 ("hook/close", "Cacao farm, Can Tho (45387550274).jpg"), ("farm", "Cacao à kpalimé 01.jpg"), ("farm", "Cacao à kpalimé 02.jpg"),
 ("farm", "Theobroma cacao 334070567.jpg"), ("farm", "Theobroma cacao 334888137.jpg"),
 ("pods", "Cacao (Theobroma cacao) at Purbachal 01.jpg"), ("pods", "Cacao (Theobroma cacao) at Purbachal 02.jpg"),
 ("pods", "CIC Farm Hingurakgoda Sri Lanka.jpg"),
 ("black pod", "Cacao black pod rot 39572305384.jpg"), ("black pod", "Cacao black pod rot 39744592361.jpg"), ("black pod", "Cacao black pod rot 29064726523.jpg"),
 ("farmer", None), ("farmer", "Cocoa farmer David Kebu Jnr and his son Snider Kebu display cocoa pods from Kebu farm. (10686939125).jpg"),
 ("farmer", "Cocoa farmer Flora Kebu explains her farming process at Kebu farm. (10687145026).jpg"), ("market", "A cocoa farm in Ghana.jpg"),
 ("rain", "Leaf on the rain drops.jpg"), ("rain", "Rain Drops on Leaves (22147107412).jpg"),
 ("drone", "UAV-IQ Conducting Drone Biological Control Operations in California.jpg"), ("drone", "20180711-APHIS-DL-flying UAS (52552488412).jpg"),
]
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(20 * (attempt + 1))
    raise RuntimeError("rate limited")
# the USAID Indonesia title is long: find it by search
res = api({"action": "query", "format": "json", "list": "search", "srsearch": "farmer prunes a cocoa tree Deli Serdang", "srnamespace": 6, "srlimit": 3})
usaid = res["query"]["search"][0]["title"][5:]
TITLES[13] = ("farmer", usaid)
# fuzzy-resolve the other long titles too
def resolve(t):
    r = api({"action": "query", "format": "json", "list": "search", "srsearch": t[:60], "srnamespace": 6, "srlimit": 1})
    return r["query"]["search"][0]["title"][5:] if r["query"]["search"] else t
out = []
for cat, t in TITLES:
    time.sleep(3.5)
    d = api({"action": "query", "format": "json", "titles": "File:" + t, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1920})
    p = next(iter(d["query"]["pages"].values()))
    if "imageinfo" not in p:
        t = resolve(t); time.sleep(1.5)
        d = api({"action": "query", "format": "json", "titles": "File:" + t, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1920}); p = next(iter(d["query"]["pages"].values()))
    ii = p["imageinfo"][0]; md = ii["extmetadata"]
    thumb = ii.get("thumburl") or ii["url"]
    try:
        h = urllib.request.urlopen(urllib.request.Request(thumb, headers=UA, method="HEAD"), timeout=30); size = int(h.headers.get("Content-Length", 0))
    except Exception as e: size = -1
    out.append({"cat": cat, "title": t, "lic": md.get("LicenseShortName", {}).get("value", ""), "artist": re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip(),
                "thumb": thumb, "page": ii["descriptionurl"], "kb": round(size / 1024), "w": ii.get("thumbwidth"), "h": ii.get("thumbheight")})
    print(f"{cat:10s} | {t[:70]:70s} | {out[-1]['lic']:12s} | {out[-1]['artist'][:28]:28s} | {out[-1]['kb']} KB | {out[-1]['w']}x{out[-1]['h']}")
json.dump(out, open("shortlist.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total MB", round(sum(o["kb"] for o in out if o["kb"] > 0) / 1024, 1))
