#!/usr/bin/env python3
"""Serially generate ONLY missing panel/hero images (rate-limit friendly), then rebuild all pages."""
import json, pathlib, time, subprocess, sys
import gen_art as g

IMG = pathlib.Path("pages/img")
tasks = []
for f in sorted(pathlib.Path("stories").glob("*.json")):
    s = json.loads(f.read_text(encoding="utf-8"))
    sid = s["id"]; seed = g.SEED.get(sid,1); ch = g.CHAR.get(sid,"")
    items = [("hero", f"{g.STYLE} {ch} {s['hero']['art_prompt']}")]
    items += [(f"p{p['n']}", f"{g.STYLE} {ch} {p['img_prompt']}") for p in s["panels"]]
    for name, prompt in items:
        out = IMG/f"{sid}-{name}.png"
        if not out.exists():
            tasks.append((prompt, seed, out))

print(f"missing: {len(tasks)}", flush=True)
for i,(prompt,seed,out) in enumerate(tasks,1):
    ok=False
    for attempt in range(6):               # patient retry for 429s
        if g.pollinations(prompt, seed, out, tries=1):
            ok=True; break
        time.sleep(12*(attempt+1))
    print(f"[{i}/{len(tasks)}] {'OK' if ok else 'FAIL'} {out.name}", flush=True)
    time.sleep(8)                           # gentle spacing between requests

print("rebuilding pages...", flush=True)
subprocess.run([sys.executable, "build.py"])
print("ALL DONE", flush=True)
