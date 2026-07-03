#!/usr/bin/env python3
"""Generate a pop-art (Lichtenstein-style) hero portrait for Chapter 1."""
import pathlib
import gen_art as g
from google import genai
from google.genai import types

IMG = pathlib.Path("pages/img")
client = genai.Client(api_key=g.load_key())
prompt = (
 "Pop-art comic book style portrait, vintage 1960s comic (Roy Lichtenstein style): "
 "a wholesome, modest young Indian woman college student with a happily surprised, hopeful, "
 "wide-eyed expression looking up, simple modest kurti, neat tied-back hair. "
 "Bold thick black ink outlines, Ben-Day halftone dot shading, limited flat retro colours "
 "(warm Indian skin tone, orange halftone background, navy, cream). Decent and respectful, "
 "no glamour, no heavy makeup, no cleavage. Head and shoulders, clean composition. Square."
)
g.gen(client, types, prompt, out=IMG / "hero-pop.png")
print("HERO DONE")
