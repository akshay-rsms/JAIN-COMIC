#!/usr/bin/env python3
"""Generate the 3 Chapter-4 'Special Power' side images with Nano Banana."""
import pathlib
import gen_art as g
from google import genai
from google.genai import types

IMG = pathlib.Path("pages/img")
client = genai.Client(api_key=g.load_key())

CH4 = {
 "ch4-ai":   "A young Indian college student cheering with both fists raised, thrilled and happy, glowing AI and tech app icons floating around them, dynamic comic energy, bright.",
 "ch4-cred": "A clean modern Indian university campus building with contemporary architecture and green landscaping on a bright sunny day, aspirational, wide establishing shot.",
 "ch4-learn":"A young Indian student learning online at a laptop wearing headphones, floating play-button, video-course and certificate icons around them, cheerful and focused.",
}
for k, desc in CH4.items():
    g.gen(client, types, g.STYLE + " " + desc, out=IMG / f"{k}.png")
print("CH4 DONE")
