#!/usr/bin/env python3
"""Style exploration: same hero scene (Story #01 online MBA) in 5 different art styles."""
import pathlib
import gen_art as g
from google import genai
from google.genai import types

IMG = pathlib.Path("style-explore"); IMG.mkdir(exist_ok=True)
client = genai.Client(api_key=g.load_key())

SCENE = ("a cheerful, wholesome young Indian working professional, about 28, in modest smart-casual office attire, "
         "at a laptop in a bright modern room, face full of relief and hope as he realises he can do an affordable "
         "online MBA while keeping his job. Warm, aspirational, positive mood. Colour palette leaning navy blue and "
         "warm gold. Respectful and decent, no glamour, no text or watermark. Square composition.")

STYLES = {
 "1-comic-graphic-novel": "Modern Indian comic-book / graphic-novel illustration, clean bold black ink linework, "
   "flat cel shading, subtle halftone texture, vivid gold and navy palette. " + SCENE,
 "2-popart-halftone": "Vintage 1960s pop-art comic in the Roy Lichtenstein style, thick black outlines, Ben-Day "
   "halftone dot shading, limited flat retro colours. " + SCENE,
 "3-flat-vector": "Clean modern FLAT VECTOR illustration, simple geometric shapes, minimal corporate ed-tech style, "
   "soft flat colours, gentle long shadows, no outlines. " + SCENE,
 "4-3d-render": "Friendly stylised 3D character render, Pixar-like, soft global illumination, rounded shapes, "
   "polished and premium. " + SCENE,
 "5-semi-realistic": "Semi-realistic warm digital painting, cinematic soft lighting, painterly brushwork, "
   "aspirational and premium editorial feel. " + SCENE,
}
for k, p in STYLES.items():
    g.gen(client, types, p, out=IMG / f"{k}.png")
print("STYLES DONE")
