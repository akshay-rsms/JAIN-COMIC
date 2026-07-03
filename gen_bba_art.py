#!/usr/bin/env python3
"""Generate Webtoon art for the 6 new BBA stories with Nano Banana.
Per story: master character sheet -> crop face -> hero + 4 panels (face ref, single
character, NO baked-in text). Trims white borders, saves optimized JPGs into pages/img/.
Run: py -3.12 gen_bba_art.py            (all 6)
     py -3.12 gen_bba_art.py bba-aviation   (one)
"""
import sys, json, time, io, pathlib
from PIL import Image, ImageChops
from google import genai
from google.genai import types

ROOT = pathlib.Path(__file__).parent
STORIES = ROOT / "stories"
IMG = ROOT / "pages" / "img"; IMG.mkdir(parents=True, exist_ok=True)
MODEL = "gemini-2.5-flash-image"

STYLE = ("Modern clean webtoon / digital-comic illustration, crisp clean linework, soft cel shading with gentle "
         "gradients, vibrant but tasteful colours, expressive friendly faces. Palette leaning warm gold #f5b301 and "
         "navy #1a237e on a warm cream #fdf3da setting, warm natural Indian skin tones. Wholesome, respectful, "
         "professional tone for a university education brand. Realistic natural body proportions, modest decent attire.")
NOTEXT = ("ABSOLUTELY NO text, letters, words, numbers, captions, signage, logos, watermarks or interface text anywhere "
          "in the image; any screen shows only simple abstract glyphs, and any paper/letter is blank. Square composition, "
          "leave a little clean headroom.")
HERO_ONE = "Show exactly ONE person in the frame; do not duplicate the character. " + NOTEXT

CHAR = {
 "bba-online-home": "RIYA: a modest Indian teenage girl, 18, from a small town, long dark hair in a neat braid or ponytail, wearing a simple decent salwar-kameez or kurti, warm brown skin, bright hopeful friendly face. Match the reference face.",
 "bba-course-fees": "SNEHA: a modest Indian teenage girl, 18, shoulder-length dark hair, wearing a simple decent kurti, warm brown skin, thoughtful then hopeful expression. Match the reference face.",
 "bba-admission": "NEHA: a modest Indian teenage girl, 18, fresh out of class 12, neat dark hair, simple decent kurti, warm brown skin, curious hopeful face. Match the reference face.",
 "bba-course": "ISHAAN: a modest Indian teenage boy, 18, neat short dark hair, a simple casual collared shirt, warm brown skin, curious confident friendly face. Match the reference face.",
 "bba-aviation": "FARHAN: a modest Indian teenage boy, 18, neat short dark hair, a simple casual collared shirt, warm brown skin, dreamy aspirational friendly face. Match the reference face.",
 "bba-digital-marketing": "KABIR: a modest Indian teenage boy, 18, neat dark hair, a decent trendy casual shirt, warm brown skin, creative energetic friendly face. Match the reference face.",
}

def key():
    for l in (ROOT/".env.local").read_text().splitlines():
        if l.startswith("GEMINI_API_KEY"): return l.split("=",1)[1].strip()
    raise SystemExit("no GEMINI_API_KEY")
client = genai.Client(api_key=key())

def trim_save(data, dst, quality=90):
    im = Image.open(io.BytesIO(data)).convert("RGB")
    bg = Image.new("RGB", im.size, (255,255,255))
    diff = ImageChops.difference(im, bg)
    bbox = ImageChops.add(diff, diff, 2.0, -40).getbbox()
    if bbox: im = im.crop(bbox)
    im.save(dst, "JPEG", quality=quality, optimize=True)
    return im

def gen(prompt, ref=None, tries=4):
    contents = [prompt]
    if ref is not None: contents.append(types.Part.from_bytes(data=ref, mime_type="image/png"))
    for a in range(tries):
        try:
            resp = client.models.generate_content(model=MODEL, contents=contents)
            for part in resp.candidates[0].content.parts:
                if getattr(part, "inline_data", None) and part.inline_data.data:
                    return part.inline_data.data
            print("   no image in response, retry")
        except Exception as ex:
            print(f"   retry {a+1}: {str(ex)[:110]}"); time.sleep(5*(a+1))
    return None

def face_ref(master_png_bytes):
    im = Image.open(io.BytesIO(master_png_bytes)).convert("RGB")
    w,h = im.size
    crop = im.crop((int(w*0.42), int(h*0.05), w, h))  # foreground bust
    buf = io.BytesIO(); crop.save(buf, "PNG"); return buf.getvalue()

def do_story(sid):
    s = json.loads((STORIES/f"{sid}.json").read_text(encoding="utf-8"))
    ch = CHAR[sid]
    print(f"\n=== {sid} ===")
    # 1) master character sheet
    mp = f"Character reference sheet, front view. {STYLE} {ch} {s['hero']['art_prompt']} {NOTEXT}"
    mb = gen(mp)
    if not mb:
        print("   FAILED master"); return
    (IMG/f"{sid}-master.png").write_bytes(mb)
    ref = face_ref(mb)
    print("   master + face ref ready")
    # 2) hero (single character)
    hb = gen(f"{STYLE} {ch} {s['hero']['art_prompt']} {HERO_ONE}", ref=ref)
    if hb: trim_save(hb, IMG/f"{sid}-hero.jpg"); print("   hero saved")
    # 3) panels
    for p in s["panels"]:
        pb = gen(f"{STYLE} {ch} {p['img_prompt']} {NOTEXT}", ref=ref)
        if pb: trim_save(pb, IMG/f"{sid}-p{p['n']}.jpg"); print(f"   panel {p['n']} saved")

if __name__ == "__main__":
    targets = sys.argv[1:] or list(CHAR.keys())
    for sid in targets:
        do_story(sid)
    print("\nDone. Now: py -3.12 build.py")
