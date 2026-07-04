#!/usr/bin/env python3
"""Regenerate the SHARED Chapter 3 (program cards) and Chapter 4 (special-power) images
in the SAME Webtoon theme as Chapter 2: warm cream/navy/gold, clean, modest, centered
subject, simple uncluttered background, NO text/logos/floating-icon halos.
Program cards -> 4:3 ; Power blocks -> 3:4 (portrait, to match the .pimg column).
Run: py -3.12 gen_ch34_art.py
"""
import sys, time, io, pathlib
from PIL import Image, ImageChops
from google import genai
from google.genai import types

ROOT = pathlib.Path(__file__).parent
IMG = ROOT / "pages" / "img"
MODEL = "gemini-2.5-flash-image"

STYLE = ("Modern clean webtoon / digital-comic illustration, crisp clean linework, soft cel shading with gentle "
         "gradients, vibrant but tasteful colours, expressive friendly faces. Palette leaning warm gold #f5b301 and "
         "navy #1a237e on a warm cream #fdf3da background, warm natural Indian skin tones. Wholesome, respectful, "
         "professional tone for a university education brand. Realistic natural body proportions, modest decent attire. "
         "Place the person centred in the frame with a simple, uncluttered warm background.")
NOTEXT = ("Do NOT render any text, letters, words, numbers, captions, signage, logos, brand marks, watermarks or "
          "floating-icon halos anywhere; any screen shows only a soft glow or a single simple abstract glyph, any "
          "paper/certificate is completely blank. Fill the whole frame edge to edge, no border.")

# name -> (aspect_ratio, ratio_float, prompt)
JOBS = {
 # ---- Chapter 3: program / elective cards (4:3) ----
 "prog-finance": ("4:3", 4/3, "A confident modest Indian male student in his late teens with a warm friendly smile, upper body, sitting at a tidy desk with an open laptop showing a simple abstract upward line and a small notebook beside him; conveys finance and business."),
 "prog-marketing": ("4:3", 4/3, "A cheerful modest Indian female student in her late teens, upper body, mid-gesture as if presenting a bright idea, holding a simple megaphone prop; conveys marketing and branding, energetic and creative."),
 "prog-hr": ("4:3", 4/3, "A warm, friendly modest Indian student in their late teens, upper body, with a welcoming open posture and kind smile; conveys people skills and human resources, approachable and supportive."),
 "prog-digital": ("4:3", 4/3, "A modern modest Indian male student in his late teens, upper body, holding a phone that shows a simple abstract rising trend; creative and confident; conveys digital marketing and social media."),
 "prog-datasci": ("4:3", 4/3, "A focused modest Indian female student in her late teens, upper body, at a laptop showing a simple abstract bar chart; curious and analytical; conveys data science and AI."),
 # ---- Chapter 4: special powers (4:3 landscape) ----
 "ch4-ai": ("4:3", 4/3, "A modest Indian student happily working on a laptop at a desk, applying modern tools, a subtle warm glow on the screen; confident and capable; wide landscape scene; conveys mastering AI tools from day one."),
 "ch4-cred": ("4:3", 4/3, "A proud modest Indian student at a desk holding up a completely blank framed certificate with a confident smile; wide landscape scene; conveys earning extra micro-credentials alongside the degree."),
 "ch4-learn": ("4:3", 4/3, "A modest Indian student attending a live online class on a laptop while wearing simple headphones, in a cosy warm home study corner; wide landscape scene; conveys flexible, well-supported online learning."),
}

def key():
    for l in (ROOT/".env.local").read_text().splitlines():
        if l.startswith("GEMINI_API_KEY"): return l.split("=",1)[1].strip()
    raise SystemExit("no GEMINI_API_KEY")
client = genai.Client(api_key=key())

def fit_ratio(im, r, top_bias=0.30):
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

def gen(prompt, ar, tries=4):
    cfg = types.GenerateContentConfig(response_modalities=["IMAGE"],
                                      image_config=types.ImageConfig(aspect_ratio=ar))
    for a in range(tries):
        try:
            resp = client.models.generate_content(model=MODEL, contents=[prompt], config=cfg)
            for part in resp.candidates[0].content.parts:
                if getattr(part,"inline_data",None) and part.inline_data.data:
                    return part.inline_data.data
            print("   no image, retry")
        except Exception as ex:
            print(f"   retry {a+1}: {str(ex)[:110]}"); time.sleep(5*(a+1))
    return None

if __name__ == "__main__":
    names = sys.argv[1:] or list(JOBS.keys())
    for n in names:
        ar, r, scene = JOBS[n]
        print(f"=== {n} ({ar}) ===")
        d = gen(f"{STYLE} {scene} {NOTEXT}", ar)
        if d: process(d, IMG/f"{n}.jpg", r); print(f"   saved {n}.jpg")
    print("\nDone. Now: py -3.12 build.py")
