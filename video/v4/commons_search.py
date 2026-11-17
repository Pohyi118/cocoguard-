"""Search Wikimedia Commons for free-licensed photos (metadata only, no file downloads)."""
import json, re, sys, time, urllib.parse, urllib.request, urllib.error
UA = {"User-Agent": "ImageSearchScript/1.0 (educational research; python urllib)"}
OK = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? \d)", re.I)
def q(term, n=40):
    params = {"action": "query", "format": "json", "generator": "search", "gsrsearch": f"{term} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": n,
              "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 1920}
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(15 * (attempt + 1))
    return {}
out = {}
for term in sys.argv[1:]:
    time.sleep(4); res = []
    for p in (q(term).get("query", {}).get("pages", {}) or {}).values():
        ii = p["imageinfo"][0]; md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if not OK.match(lic) or ii["width"] < 1400 or ii["mime"] not in ("image/jpeg", "image/png"): continue
        artist = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()[:60]
        desc = re.sub("<[^>]+>", "", md.get("ImageDescription", {}).get("value", "")).strip().replace("\n", " ")[:110]
        res.append({"title": p["title"], "w": ii["width"], "h": ii["height"], "orig_mb": round(ii["size"] / 1e6, 1), "lic": lic, "artist": artist,
                    "thumb": ii.get("thumburl"), "page": ii["descriptionurl"], "desc": desc})
    out[term] = res
    print(f"\n=== {term}: {len(res)} usable")
    for r in res[:12]: print(f"- {r['title'][5:80]} | {r['w']}x{r['h']} | {r['lic']} | {r['artist'][:30]} | {r['desc'][:80]}")
json.dump(out, open("commons_results.json", "a", encoding="utf-8"), ensure_ascii=False); open("commons_results.json", "a").write("\n")
