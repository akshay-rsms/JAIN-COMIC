#!/usr/bin/env bash
# Regenerate Ch2 panels (consistent Aarav via existing master) + Ch4 side images, then optimize to JPG.
cd "$(dirname "$0")"
echo "=== Ch2 panels (panels-only, reuse master) ==="
py -3.12 gen_art.py --only bba-fees-reveal --panels-only
echo "=== Ch4 side images ==="
py -3.12 gen_ch4.py
echo "=== Optimize new PNGs -> JPG ==="
py -3.12 - <<'PY'
from PIL import Image
import pathlib
IMG = pathlib.Path("pages/img")
names = ["bba-fees-reveal-p1","bba-fees-reveal-p2","bba-fees-reveal-p3","bba-fees-reveal-p4",
         "ch4-ai","ch4-cred","ch4-learn"]
for n in names:
    p = IMG / (n + ".png")
    if not p.exists():
        print("MISSING", p.name); continue
    im = Image.open(p).convert("RGB")
    w,h = im.size; m = max(w,h)
    if m > 1024:
        im = im.resize((int(w*1024/m), int(h*1024/m)), Image.LANCZOS)
    j = IMG / (n + ".jpg")
    im.save(j, "JPEG", quality=82, optimize=True)
    p.unlink()  # remove PNG so build picks the fresh JPG
    print("optimized", j.name, j.stat().st_size//1024, "KB")
print("OPTIMIZE DONE")
PY
echo "ALL IMAGE WORK DONE"
