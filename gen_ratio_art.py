#!/usr/bin/env python3
"""Regenerate all BBA hero + panel art at the PLACEHOLDER aspect ratios so images fill
their boxes with no awkward crop: hero = 4:3 (landscape banner), panels = 3:2.
Reuses each story's existing master character sheet as a face reference for consistency
(generates a master only if missing). No baked-in text. Saves optimized JPGs.
Run: py -3.12 gen_ratio_art.py            (all)
     py -3.12 gen_ratio_art.py bba-finance
"""
import sys, json, time, io, pathlib
from PIL import Image, ImageChops
from google import genai
from google.genai import types

ROOT = pathlib.Path(__file__).parent
STORIES = ROOT / "stories"
IMG = ROOT / "pages" / "img"
MODEL = "gemini-2.5-flash-image"
HERO_AR, PANEL_AR = "4:3", "3:2"
HERO_R, PANEL_R = 4/3, 3/2

STYLE = ("Modern clean webtoon / digital-comic illustration, crisp clean linework, soft cel shading with gentle "
         "gradients, vibrant but tasteful colours, expressive friendly faces. Palette leaning warm gold #f5b301 and "
         "navy #1a237e on a warm cream #fdf3da setting, warm natural Indian skin tones. Wholesome, respectful, "
         "professional tone for a university education brand. Realistic natural body proportions, modest decent attire. "
         "Compose for a wide landscape banner frame: place the person's face and upper body CENTERED in the frame "
         "(never in a corner), and keep the TOP-RIGHT area of the image relatively clear and simple so an overlaid "
         "speech bubble placed there will not cover the face.")
NOTEXT = ("Do NOT render any text, letters, words, numbers, captions, signage, logos or watermark anywhere in the image. "
          "VERY IMPORTANT: any laptop, computer, tablet or phone screen must be BLANK, showing only a soft solid-colour "
          "glow and AT MOST one tiny simple icon (a plain round coin or a few chart bars) - NEVER any words, letters or "
          "numbers on the screen. Any paper or letter is completely blank. Fill the whole frame edge to edge, no border.")
HERO_ONE = "Show exactly ONE person; do not duplicate the character. " + NOTEXT

CHAR = {
 "bba-fees-reveal": "AARAV: modest Indian teenage boy, 18, neat short dark hair, a light-blue collared shirt under a navy sweater-vest, warm brown skin, cheerful hopeful face. Match the reference face.",
 "bba-online": "ADITYA: cheerful modest Indian teenage boy, 18, neat short black hair, a simple casual checked shirt, warm brown skin, friendly face. Match the reference face.",
 "bba-course": "ISHAAN: modest Indian teenage boy, 18, neat short dark hair, a simple casual collared shirt, warm brown skin, curious confident friendly face. Match the reference face.",
 "bba-course-fees": "SNEHA: modest Indian teenage girl, 18, shoulder-length dark hair, a simple decent kurti, warm brown skin, thoughtful then hopeful expression. Match the reference face.",
 "bba-online-home": "RIYA: modest Indian teenage girl, 18, long dark hair in a neat braid, a simple decent salwar-kameez or kurti with dupatta, warm brown skin, bright hopeful friendly face. Match the reference face.",
 "bba-admission": "NEHA: modest Indian teenage girl, 18, neat dark hair, a simple decent kurti, warm brown skin, curious hopeful face. Match the reference face.",
 "bba-finance": "ROHAN: modest Indian teenage boy, 18, neat short dark hair, a smart-casual collared shirt, warm brown skin, sharp confident friendly face. Match the reference face.",
 "bba-digital-marketing": "KABIR: modest Indian teenage boy, 18, neat dark hair, a decent trendy casual shirt, warm brown skin, creative energetic friendly face. Match the reference face.",
}

def key():
    for l in (ROOT/".env.local").read_text().splitlines():
        if l.startswith("GEMINI_API_KEY"): return l.split("=",1)[1].strip()
    raise SystemExit("no GEMINI_API_KEY")
client = genai.Client(api_key=key())

def fit_ratio(im, r, top_bias=0.38):
    """crop to exact ratio r (w/h); vertical crop biased toward the top to keep faces."""
    w,h = im.size
    if w/h > r:  # too wide -> crop sides (centered)
        nw = int(h*r); x = (w-nw)//2; im = im.crop((x,0,x+nw,h))
    else:        # too tall -> crop height, biased to top
        nh = int(w/r); y = int((h-nh)*top_bias); im = im.crop((0,y,w,y+nh))
    return im

def process(data, dst, r):
    im = Image.open(io.BytesIO(data)).convert("RGB")
    bg = Image.new("RGB", im.size, (255,255,255))
    diff = ImageChops.difference(im, bg)
    bbox = ImageChops.add(diff, diff, 2.0, -40).getbbox()
    if bbox: im = im.crop(bbox)          # trim any stray white border
    im = fit_ratio(im, r)                # lock to exact placeholder ratio
    im.save(dst, "JPEG", quality=90, optimize=True)

def gen(prompt, ar, ref=None, tries=4):
    contents = [prompt]
    if ref is not None: contents.append(types.Part.from_bytes(data=ref, mime_type="image/png"))
    cfg = types.GenerateContentConfig(response_modalities=["IMAGE"],
                                      image_config=types.ImageConfig(aspect_ratio=ar))
    for a in range(tries):
        try:
            resp = client.models.generate_content(model=MODEL, contents=contents, config=cfg)
            for part in resp.candidates[0].content.parts:
                if getattr(part, "inline_data", None) and part.inline_data.data:
                    return part.inline_data.data
            print("   no image, retry")
        except Exception as ex:
            print(f"   retry {a+1}: {str(ex)[:110]}"); time.sleep(5*(a+1))
    return None

def face_ref(sid):
    mp = IMG/f"{sid}-master.png"
    if not mp.exists():
        mb = gen(f"Character reference sheet, front view. {STYLE} {CHAR[sid]} {NOTEXT}", "1:1")
        if not mb: return None
        mp.write_bytes(mb)
    im = Image.open(io.BytesIO(mp.read_bytes())).convert("RGB")
    w,h = im.size
    crop = im.crop((int(w*0.42), int(h*0.05), w, h))
    buf = io.BytesIO(); crop.save(buf, "PNG"); return buf.getvalue()

def do_story(sid):
    s = json.loads((STORIES/f"{sid}.json").read_text(encoding="utf-8"))
    print(f"\n=== {sid} ===")
    ref = face_ref(sid)
    hb = gen(f"{STYLE} {CHAR[sid]} {s['hero']['art_prompt']} {HERO_ONE}", HERO_AR, ref=ref)
    if hb: process(hb, IMG/f"{sid}-hero.jpg", HERO_R); print("   hero 4:3 saved")
    for p in s["panels"]:
        pb = gen(f"{STYLE} {CHAR[sid]} {p['img_prompt']} {NOTEXT}", PANEL_AR, ref=ref)
        if pb: process(pb, IMG/f"{sid}-p{p['n']}.jpg", PANEL_R); print(f"   panel {p['n']} 3:2 saved")

if __name__ == "__main__":
    ids = sys.argv[1:] or list(CHAR.keys())
    for sid in ids: do_story(sid)
    print("\nDone. Now: py -3.12 build.py")
