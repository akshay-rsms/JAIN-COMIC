#!/usr/bin/env python3
"""Generate Webtoon art for the 5 MCA stories + 5 shared MCA Chapter-3 cards with Nano Banana.
Per story: master -> face-ref -> 4:3 hero + 3:2 panels (single character, centered, NO baked-in
text). Persona = Indian graduates / young IT professionals ~22-27.
Run: py -3.12 gen_mca_art.py                (all 5 stories + cards)
     py -3.12 gen_mca_art.py mca-data-science
     py -3.12 gen_mca_art.py progcards
"""
import sys, json, time, io, pathlib
from PIL import Image, ImageChops
from google import genai
from google.genai import types

ROOT = pathlib.Path(__file__).parent
STORIES = ROOT / "stories"
IMG = ROOT / "pages" / "img"; IMG.mkdir(parents=True, exist_ok=True)
MODEL = "gemini-2.5-flash-image"
HERO_AR, PANEL_AR = "4:3", "3:2"; HERO_R, PANEL_R = 4/3, 3/2

STYLE = ("Modern clean webtoon / digital-comic illustration, crisp clean linework, soft cel shading with gentle "
         "gradients, vibrant but tasteful colours, expressive friendly faces. Palette leaning warm gold #f5b301 and "
         "navy #1a237e on a warm cream #fdf3da setting, warm natural Indian skin tones. Wholesome, respectful, "
         "professional tone for a university education brand. Realistic natural adult body proportions, modest decent "
         "attire. Compose for a wide landscape banner frame: place the person's face and upper body CENTERED in the "
         "frame (never in a corner), and keep the TOP-RIGHT area of the image relatively clear and simple so an "
         "overlaid speech bubble placed there will not cover the face.")
NOTEXT = ("Do NOT render any text, letters, words, numbers, captions, signage, logos or watermark anywhere in the image. "
          "VERY IMPORTANT: any laptop, computer, tablet or phone screen must be BLANK, showing only a soft solid-colour "
          "glow and AT MOST one tiny simple icon (a few chart bars or a plain shield) - NEVER any words, letters or "
          "numbers on the screen. Any paper is completely blank. Fill the whole frame edge to edge, no border.")
HERO_ONE = "Show exactly ONE person; do not duplicate the character. " + NOTEXT

CHAR = {
 "mca-course": "RAHUL: an Indian graduate man, 23, neat short dark hair, a casual collared shirt, warm brown skin, curious driven friendly face. Match the reference face.",
 "mca-online": "SNEHA: an Indian working IT woman, 24, shoulder-length dark hair, smart-casual professional top, warm brown skin, ambitious warm friendly face. Match the reference face.",
 "mca-course-fees": "ARJUN: an Indian graduate man, 23, neat short dark hair, smart-casual shirt, warm brown skin, thoughtful then relieved face. Match the reference face.",
 "mca-data-science": "NEHA: an Indian graduate woman, 24, shoulder-length dark hair, smart-casual professional top, warm brown skin, focused analytical friendly face. Match the reference face.",
 "mca-cyber-security": "KARTHIK: an Indian graduate man, 24, neat short dark hair, smart-casual shirt, warm brown skin, sharp focused confident face. Match the reference face.",
}
PROGCARDS = {
 "prog-mca-datasci": "A focused Indian young tech professional woman in her mid 20s in smart-casual, upper body, at a laptop showing a simple abstract bar chart; conveys MCA in Data Science.",
 "prog-mca-ai": "A confident Indian young tech professional man in his mid 20s in smart-casual, upper body, beside a soft glowing abstract neural-node shape; conveys MCA in Artificial Intelligence.",
 "prog-mca-cloud": "A capable Indian young tech professional man in his mid 20s in smart-casual, upper body, beside a soft simple cloud glyph; conveys MCA in Cloud Computing.",
 "prog-mca-cybersec": "A sharp Indian young tech professional man in his mid 20s in smart-casual, upper body, beside a simple glowing shield glyph; conveys MCA in Cyber Security.",
 "prog-mca-fullstack": "A cheerful Indian young tech professional woman in her mid 20s in smart-casual, upper body, at a laptop building a simple abstract app layout; conveys MCA in Full Stack Development.",
}

def key():
    for l in (ROOT/".env.local").read_text().splitlines():
        if l.startswith("GEMINI_API_KEY"): return l.split("=",1)[1].strip()
    raise SystemExit("no GEMINI_API_KEY")
client = genai.Client(api_key=key())

def fit_ratio(im, r, top_bias=0.32):
    w,h = im.size
    if w/h > r: nw=int(h*r); x=(w-nw)//2; im=im.crop((x,0,x+nw,h))
    else: nh=int(w/r); y=int((h-nh)*top_bias); im=im.crop((0,y,w,y+nh))
    return im

def process(data, dst, r):
    im = Image.open(io.BytesIO(data)).convert("RGB")
    bg = Image.new("RGB", im.size, (255,255,255))
    bbox = ImageChops.add(ImageChops.difference(im,bg), ImageChops.difference(im,bg), 2.0, -40).getbbox()
    if bbox: im = im.crop(bbox)
    fit_ratio(im, r).save(dst, "JPEG", quality=90, optimize=True)

def gen(prompt, ar, ref=None, tries=4):
    contents=[prompt]
    if ref is not None: contents.append(types.Part.from_bytes(data=ref, mime_type="image/png"))
    cfg=types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio=ar))
    for a in range(tries):
        try:
            resp=client.models.generate_content(model=MODEL, contents=contents, config=cfg)
            for part in resp.candidates[0].content.parts:
                if getattr(part,"inline_data",None) and part.inline_data.data: return part.inline_data.data
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
    im = Image.open(io.BytesIO(mp.read_bytes())).convert("RGB"); w,h=im.size
    buf=io.BytesIO(); im.crop((int(w*0.42),int(h*0.05),w,h)).save(buf,"PNG"); return buf.getvalue()

def do_story(sid):
    s = json.loads((STORIES/f"{sid}.json").read_text(encoding="utf-8"))
    print(f"\n=== {sid} ===")
    ref = face_ref(sid)
    if ref is None: print("   FAILED master"); return
    hb = gen(f"{STYLE} {CHAR[sid]} {s['hero']['art_prompt']} {HERO_ONE}", HERO_AR, ref=ref)
    if hb: process(hb, IMG/f"{sid}-hero.jpg", HERO_R); print("   hero 4:3 saved")
    for p in s["panels"]:
        pb = gen(f"{STYLE} {CHAR[sid]} {p['img_prompt']} {NOTEXT}", PANEL_AR, ref=ref)
        if pb: process(pb, IMG/f"{sid}-p{p['n']}.jpg", PANEL_R); print(f"   panel {p['n']} saved")

def do_progcards():
    print("\n=== MCA Chapter-3 program cards ===")
    for name, scene in PROGCARDS.items():
        d = gen(f"{STYLE} {scene} {NOTEXT}", "4:3")
        if d: process(d, IMG/f"{name}.jpg", 4/3); print(f"   {name}.jpg saved")

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["progcards"]:
        do_progcards()
    else:
        for sid in (args or list(CHAR.keys())): do_story(sid)
        if not args: do_progcards()
    print("\nDone. Now rebuild: py -3.12 build.py <ids>")
