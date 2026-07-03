#!/usr/bin/env python3
"""Generate 5 DISTINCT Chapter-3 elective program-card portraits with Nano Banana (different person each)."""
import pathlib
import gen_art as g
from google import genai
from google.genai import types

IMG = pathlib.Path("pages/img")
client = genai.Client(api_key=g.load_key())

CARDS = {
 "finance":  "A confident young Indian man, BBA Finance student, modest smart-casual shirt, with floating charts, gold coins and a calculator around him. Cheerful, wholesome.",
 "marketing":"A creative young Indian woman, BBA Marketing student, modest kurti, with a megaphone, brand logos and idea light-bulbs around her. Bright, wholesome.",
 "hr":       "A warm young Indian woman wearing glasses, BBA Human Resources student, modest salwar-kameez, with people, handshake and teamwork icons around her. Friendly, wholesome.",
 "digital":  "A trendy but modest young Indian man, BBA Digital Marketing student, casual shirt, with social-media, hashtag and analytics icons around him. Youthful, wholesome.",
 "datasci":  "A smart young Indian woman, BBA Data Science and AI student, modest top, with code brackets, graphs and glowing AI icons around her. Curious, wholesome.",
}
for k, desc in CARDS.items():
    g.gen(client, types, g.STYLE + " Comic program-card portrait, head and shoulders. " + desc,
          out=IMG / f"prog-{k}.png")
print("PROGCARDS DONE")
