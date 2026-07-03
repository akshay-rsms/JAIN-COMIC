#!/usr/bin/env python3
"""Style exploration round 2: 5 more distinct art directions for the same hero scene."""
import pathlib
import gen_art as g
from google import genai
from google.genai import types

IMG = pathlib.Path("style-explore"); IMG.mkdir(exist_ok=True)
client = genai.Client(api_key=g.load_key())

SCENE = ("a cheerful, wholesome young Indian working professional, about 28, in modest smart-casual attire, at a laptop "
         "in a bright room, face full of relief and hope realising he can do an affordable online MBA while keeping his "
         "job. Warm, aspirational, positive. Navy blue and warm gold palette. Respectful, no glamour, "
         "absolutely no text, letters, words or watermark. Square composition.")

STYLES = {
 "6-webtoon": "Modern Korean webtoon / digital comic style: crisp clean linework, soft cel shading with gentle "
   "gradients, vibrant youthful colours, expressive faces, made for sequential story panels. " + SCENE,
 "7-indian-folk-fusion": "Contemporary illustration fused with Indian folk-art motifs (Madhubani and Warli inspired "
   "patterns, decorative borders), culturally rooted yet modern, warm earthy palette with gold and indigo. " + SCENE,
 "8-riso-duotone": "Risograph print style, grainy textured DUOTONE using only navy blue and warm gold, limited "
   "palette, retro editorial poster feel, slight ink misregistration. " + SCENE,
 "9-ligne-claire": "Ligne claire clean-line comic style (Herge / Tintin inspired): uniform clean outlines, flat "
   "bright colours, minimal shading, tidy and timeless. " + SCENE,
 "10-papercut-collage": "Layered paper-cut collage illustration: tactile cut-paper shapes with soft drop shadows, "
   "warm textured paper, craft editorial feel. " + SCENE,
}
for k, p in STYLES.items():
    g.gen(client, types, p, out=IMG / f"{k}.png")
print("STYLES2 DONE")
