"""Download the approved shortlist (1920-px versions) into photos/ and write credits.json."""
import json, re, time, urllib.request, urllib.error, pathlib
UA = {"User-Agent": "ImageSearchScript/1.0 (educational research; python urllib)"}
items = json.load(open("shortlist.json", encoding="utf-8")); credits = []
for n, it in enumerate(items, 1):
    slug = re.sub(r"[^a-z0-9]+", "_", it["cat"].lower()).strip("_")
    dst = pathlib.Path("photos") / f"{n:02d}_{slug}.jpg"
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(it["thumb"], headers=UA), timeout=60) as r: data = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(15 * (attempt + 1))
    assert data[:3] == b"\xff\xd8\xff", f"not a JPEG: {it['title']}"
    dst.write_bytes(data); time.sleep(1.5)
    credits.append({"file": dst.name, "title": it["title"], "author": it["artist"], "license": it["lic"], "source": it["page"], "cat": it["cat"]})
    print(f"{dst.name:24s} {len(data)//1024:5d} KB  {it['lic']:13s} {it['title'][:60]}")
json.dump(credits, open("credits.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done", len(credits))
