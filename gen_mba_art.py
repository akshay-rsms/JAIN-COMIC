#!/usr/bin/env python3
"""Generate Webtoon art for the 20 MBA stories with Nano Banana (gemini-2.5-flash-image).
Per story: master character sheet -> crop face -> 4:3 hero + 3:2 panels (face ref, single
character, centered, NO baked-in text). Also builds the 5 shared MBA Chapter-3 program
cards (prog-mba-*.jpg, 4:3). MBA persona = Indian working professionals in their late 20s.
Run: py -3.12 gen_mba_art.py                 (all 20 stories)
     py -3.12 gen_mba_art.py mba-finance     (one story)
     py -3.12 gen_mba_art.py progcards        (only the Ch3 MBA program cards)
"""
import sys, json, time, io, pathlib
from PIL import Image, ImageChops
from google import genai
from google.genai import types

ROOT = pathlib.Path(__file__).parent
STORIES = ROOT / "stories"
IMG = ROOT / "pages" / "img"; IMG.mkdir(parents=True, exist_ok=True)
MODEL = "gemini-2.5-flash-image"
HERO_AR, PANEL_AR = "4:3", "3:2"
HERO_R, PANEL_R = 4/3, 3/2

STYLE = ("Modern clean webtoon / digital-comic illustration, crisp clean linework, soft cel shading with gentle "
         "gradients, vibrant but tasteful colours, expressive friendly faces. Palette leaning warm gold #f5b301 and "
         "navy #1a237e on a warm cream #fdf3da setting, warm natural Indian skin tones. Wholesome, respectful, "
         "professional tone for a university education brand. Realistic natural adult body proportions, modest decent "
         "professional attire. Compose for a wide landscape banner frame: place the person's face and upper body "
         "CENTERED in the frame (never in a corner), and keep the TOP-RIGHT area of the image relatively clear and "
         "simple so an overlaid speech bubble placed there will not cover the face.")
NOTEXT = ("Do NOT render any text, letters, words, numbers, captions, signage, logos or watermark anywhere in the image. "
          "VERY IMPORTANT: any laptop, computer, tablet or phone screen must be BLANK, showing only a soft solid-colour "
          "glow and AT MOST one tiny simple icon (a plain round coin or a few chart bars) - NEVER any words, letters or "
          "numbers on the screen. Any paper, certificate or letter is completely blank. Fill the whole frame edge to "
          "edge, no border.")
HERO_ONE = "Show exactly ONE person; do not duplicate the character. " + NOTEXT

# per-story protagonist (matches make_mba_stories.py). Adults, late 20s, professional attire.
CHAR = {
 "mba-course": "ARJUN: an Indian working professional man, 27, neat short dark hair, smart business-casual shirt, warm brown skin, capable confident friendly face. Match the reference face.",
 "mba-online": "PRIYA: an Indian working professional woman, 28, shoulder-length dark hair, smart-casual professional top or kurti, warm brown skin, ambitious warm friendly face. Match the reference face.",
 "mba-online-home": "MEERA: an Indian woman, 29, from a smaller town, long dark hair neatly tied, a simple decent kurta, warm brown skin, hopeful determined friendly face. Match the reference face.",
 "mba-course-fees": "RAHUL: an Indian working professional man, 28, neat short dark hair, smart-casual collared shirt, warm brown skin, thoughtful then relieved face. Match the reference face.",
 "mba-fees-reveal": "SNEHA: an Indian working professional woman, 27, shoulder-length dark hair, smart-casual professional blouse, warm brown skin, calm reassured face. Match the reference face.",
 "mba-admission": "KARTHIK: an Indian graduate man, 26, neat short dark hair, smart-casual shirt, warm brown skin, curious hopeful face. Match the reference face.",
 "mba-hr": "DIVYA: an Indian working professional woman, 28, neat dark hair, business-casual blazer or blouse, warm brown skin, warm approachable confident face. Match the reference face.",
 "mba-finance": "ADITYA: an Indian working professional man, 28, neat short dark hair, business-casual shirt, warm brown skin, sharp confident friendly face. Match the reference face.",
 "mba-healthcare": "ANANYA: an Indian healthcare professional woman, 29, neat tied dark hair, smart professional attire (a neat blouse, subtle healthcare feel, no logos), warm brown skin, caring confident face. Match the reference face.",
 "mba-marketing": "ROHAN: an Indian working professional man, 28, neat dark hair, smart-casual shirt, warm brown skin, energetic creative confident face. Match the reference face.",
 "mba-data-science": "NEHA: an Indian working professional woman, 28, shoulder-length dark hair, smart-casual professional top, warm brown skin, focused analytical friendly face. Match the reference face.",
 "mba-logistics": "VIKRAM: an Indian working professional man, 29, neat short dark hair, a smart-casual shirt with a professional capable look, warm brown skin, steady confident face. Match the reference face.",
 "mba-operations": "SANJAY: an Indian working professional man, 29, neat short dark hair, business-casual shirt, warm brown skin, sharp practical confident face. Match the reference face.",
 "mba-it": "ARUN: an Indian tech professional man, 28, neat dark hair, smart-casual shirt, warm brown skin, clever confident friendly face. Match the reference face.",
 "mba-project-management": "DEEPAK: an Indian working professional man, 29, neat short dark hair, business-casual shirt, warm brown skin, organised confident face. Match the reference face.",
 "mba-digital-marketing": "KABIR: an Indian working professional man, 27, neat dark hair, a decent trendy smart-casual shirt, warm brown skin, creative energetic face. Match the reference face.",
 "mba-international-business": "ISHA: an Indian working professional woman, 28, neat dark hair, smart professional blazer, warm brown skin, poised global-minded confident face. Match the reference face.",
 "mba-international-finance": "VARUN: an Indian working professional man, 28, neat short dark hair, smart professional shirt, warm brown skin, sharp global-minded confident face. Match the reference face.",
 "mba-entrepreneurship": "NIKHIL: an Indian young founder man, 28, neat dark hair, smart-casual shirt, warm brown skin, driven energetic confident face. Match the reference face.",
 "mba-strategy-leadership": "AISHA: an Indian senior professional woman, 30, neat dark hair, smart professional blazer, warm brown skin, poised authoritative warm face. Match the reference face.",
}

# Chapter-3 MBA program cards (shared across all MBA pages). 4:3, no face-ref needed.
PROGCARDS = {
 "prog-mba-finance": "A confident Indian working professional man in his late 20s in business-casual, upper body, at a tidy desk with an open laptop showing a simple abstract upward line; conveys MBA in Finance.",
 "prog-mba-marketing": "A cheerful Indian working professional man in his late 20s in smart-casual, upper body, mid-gesture presenting a bright brand idea; conveys MBA in Marketing, energetic and creative.",
 "prog-mba-hr": "A warm friendly Indian working professional woman in her late 20s in business-casual, upper body, welcoming open posture and kind smile; conveys MBA in Human Resource Management.",
 "prog-mba-datasci": "A focused Indian working professional woman in her late 20s in smart-casual, upper body, at a laptop showing a simple abstract bar chart; curious and analytical; conveys MBA in Data Science and Analytics.",
 "prog-mba-operations": "A capable Indian working professional man in his late 20s in business-casual, upper body, beside a clean simple process board; conveys MBA in Operations Management, practical and confident.",
}

def key():
    for l in (ROOT/".env.local").read_text().splitlines():
        if l.startswith("GEMINI_API_KEY"): return l.split("=",1)[1].strip()
    raise SystemExit("no GEMINI_API_KEY")
client = genai.Client(api_key=key())

def fit_ratio(im, r, top_bias=0.32):
    w,h = im.size
    if w/h > r:
        nw = int(h*r); x=(w-nw)//2; im=im.crop((x,0,x+nw,h))
    else:
        nh = int(w/r); y=int((h-nh)*top_bias); im=im.crop((0,y,w,y+nh))
    return im

def process(data, dst, r):
    im = Image.open(io.BytesIO(data)).convert("RGB")
    bg = Image.new("RGB", im.size, (255,255,255))
    diff = ImageChops.difference(im, bg)
    bbox = ImageChops.add(diff, diff, 2.0, -40).getbbox()
    if bbox: im = im.crop(bbox)
    im = fit_ratio(im, r)
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
        mb = gen(f"Character reference sheet, front view, plain background. {STYLE} {CHAR[sid]} {NOTEXT}", "1:1")
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
    if ref is None: print("   FAILED master"); return
    hb = gen(f"{STYLE} {CHAR[sid]} {s['hero']['art_prompt']} {HERO_ONE}", HERO_AR, ref=ref)
    if hb: process(hb, IMG/f"{sid}-hero.jpg", HERO_R); print("   hero 4:3 saved")
    for p in s["panels"]:
        pb = gen(f"{STYLE} {CHAR[sid]} {p['img_prompt']} {NOTEXT}", PANEL_AR, ref=ref)
        if pb: process(pb, IMG/f"{sid}-p{p['n']}.jpg", PANEL_R); print(f"   panel {p['n']} 3:2 saved")

def do_progcards():
    print("\n=== MBA Chapter-3 program cards ===")
    for name, scene in PROGCARDS.items():
        d = gen(f"{STYLE} {scene} {NOTEXT}", "4:3")
        if d: process(d, IMG/f"{name}.jpg", 4/3); print(f"   {name}.jpg saved")

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["progcards"]:
        do_progcards()
    else:
        ids = args or list(CHAR.keys())
        for sid in ids: do_story(sid)
        if not args:  # full run also builds the shared Ch3 cards
            do_progcards()
    print("\nDone. Now rebuild: py -3.12 build.py <ids>")
