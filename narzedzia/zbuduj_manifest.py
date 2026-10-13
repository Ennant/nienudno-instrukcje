#!/usr/bin/env python3
"""Buduje manifest.json dla aplikacji Nienudno Robotyka z zawartości folderu instrukcje/.

Zasady (żeby instruktor nie musiał nic konfigurować):
  * instrukcje/<Kategoria>/<Tytuł>.pdf  – kategoria = nazwa folderu, tytuł = nazwa pliku,
  * numer na początku nazwy ustala kolejność i jest ukrywany ("02 Wiatrak.pdf" -> "Wiatrak"),
  * podkreślenia zamieniane są na spacje,
  * pliki w podfolderach głębiej trafiają do kategorii z pierwszego poziomu.
"""
import hashlib, json, os, re, sys, urllib.parse, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "instrukcje")
NUM = re.compile(r"^\s*(\d{1,3})[\s._\-)]+")


def clean(name):
    name = NUM.sub("", name)
    name = name.replace("_", " ").strip()
    return re.sub(r"\s+", " ", name)


def order_key(name):
    m = NUM.match(name)
    return (int(m.group(1)) if m else 10_000, name.lower())


def slug(s):
    s = unicodedata.normalize("NFKD", s.replace("ł", "l").replace("Ł", "L"))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60] or "plik"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build():
    items, ids = [], set()
    if os.path.isdir(SRC):
        for cat in sorted((d for d in os.listdir(SRC) if os.path.isdir(os.path.join(SRC, d)) and not d.startswith(".")), key=order_key):
            files = []
            for dirpath, _, fnames in os.walk(os.path.join(SRC, cat)):
                for f in fnames:
                    if f.lower().endswith(".pdf"):
                        files.append(os.path.join(dirpath, f))
            files.sort(key=lambda p: [order_key(x) for x in os.path.relpath(p, SRC).split(os.sep)])
            for path in files:
                rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
                title = clean(os.path.splitext(os.path.basename(path))[0])
                base = f"{slug(clean(cat))}-{slug(title)}"[:80]
                iid, n = base, 2
                while iid in ids:
                    iid, n = f"{base}-{n}", n + 1
                ids.add(iid)
                items.append({
                    "id": iid,
                    "title": title,
                    "category": clean(cat),
                    "url": "/".join(urllib.parse.quote(part) for part in rel.split("/")),
                    "sha256": sha256(path),
                    "size": os.path.getsize(path),
                })
    manifest = {"version": 1, "instructions": items}
    rel_file = os.path.join(ROOT, "aplikacja", "release.json")
    if os.path.exists(rel_file):
        with open(rel_file, encoding="utf-8") as f:
            r = json.load(f)
        apk = os.path.join(ROOT, "aplikacja", r["file"])
        if os.path.exists(apk):
            manifest["app"] = {
                "versionCode": int(r["versionCode"]),
                "versionName": str(r["versionName"]),
                "url": "aplikacja/" + urllib.parse.quote(r["file"]),
                "sha256": sha256(apk),
            }
    return manifest


if __name__ == "__main__":
    m = build()
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
    cats = {}
    for it in m["instructions"]:
        cats[it["category"]] = cats.get(it["category"], 0) + 1
    print(f"{len(m['instructions'])} instrukcji w {len(cats)} kategoriach: {cats}; aplikacja: {m.get('app', {}).get('versionName', '-')}")
