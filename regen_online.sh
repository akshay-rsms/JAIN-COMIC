#!/usr/bin/env bash
cd "$(dirname "$0")"
py -3.12 gen_art.py --only bba-online
py -3.12 - <<'PY'
from PIL import Image, ImageChops
import pathlib
IMG=pathlib.Path("pages/img")
def trim(im):
    im=im.convert("RGB"); bg=Image.new("RGB",im.size,(255,255,255))
    d=ImageChops.difference(im,bg); d=ImageChops.add(d,d,2.0,-28); bb=d.getbbox()
    return im.crop(bb) if bb else im
for n in ["bba-online-hero","bba-online-p1","bba-online-p2","bba-online-p3","bba-online-p4"]:
    p=IMG/(n+".png")
    if not p.exists(): print("MISS",n); continue
    im=trim(Image.open(p)); w,h=im.size; m=max(w,h)
    if m>1024: im=im.resize((int(w*1024/m),int(h*1024/m)),Image.LANCZOS)
    j=IMG/(n+".jpg"); im.save(j,"JPEG",quality=84,optimize=True); p.unlink()
    print("opt",j.name,j.stat().st_size//1024,"KB")
print("ONLINE IMAGES DONE")
PY
echo ALL_DONE
