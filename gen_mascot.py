#!/usr/bin/env python3
"""Generate 4 brand-mascot concepts for JAIN Online (webtoon style, navy + gold)."""
import pathlib
import gen_art as g
from google import genai
from google.genai import types

IMG = pathlib.Path("mascot"); IMG.mkdir(exist_ok=True)
client = genai.Client(api_key=g.load_key())

COMMON = ("Friendly BRAND MASCOT for an Indian online university (JAIN Online). Modern clean webtoon / vector-comic "
          "style, simple bold shapes, big friendly eyes, cheerful and approachable, wholesome. Colour scheme navy "
          "blue and warm gold only. Front-facing, full-body, centred on a plain flat off-white background. Iconic and "
          "simple enough to work small in a website header. Absolutely no text, letters, words or watermark. ")

CONCEPTS = {
 "1-owl-grad": COMMON + "A cute wise owl wearing a small graduation cap, navy feathers with a gold chest and gold ring eyes.",
 "2-gold-star": COMMON + "A cheerful five-pointed GOLD STAR character with a smiling face, little arms and legs, wearing a tiny graduation cap, clean navy outline. A 'star student' mascot.",
 "3-elephant-scholar": COMMON + "A cute friendly baby elephant scholar, soft navy-grey body with gold accents, wearing a small graduation cap, gentle and smart expression, holding a little book.",
 "4-peacock-scholar": COMMON + "A cute stylised peacock scholar with navy and gold plumage, wearing a small graduation cap, elegant yet friendly and simple.",
}
for k, p in CONCEPTS.items():
    g.gen(client, types, p, out=IMG / f"{k}.png")
print("MASCOT DONE")
