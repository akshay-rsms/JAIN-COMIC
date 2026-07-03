#!/usr/bin/env python3
"""
Generate comic art for the JAIN ONLINE story pages with Nano Banana (Gemini image model).

Character consistency = the whiteboard's "master image -> ref image" workflow:
  1) generate ONE master character sheet per story
  2) generate every panel + hero PASSING THE MASTER AS A REFERENCE so the face/outfit/style hold.

Usage:
  py -3.12 gen_art.py --pack                 # write PROMPT_PACK.md (no API, no billing needed)
  py -3.12 gen_art.py                         # generate ALL stories  (needs billing on the key)
  py -3.12 gen_art.py --only fees-roi         # generate one story
  py -3.12 gen_art.py --only fees-roi --panels-only   # skip master/hero, just panels

Requires .env.local with GEMINI_API_KEY=...  (billing enabled for image models).
Saves to pages/img/<id>-master.png, <id>-hero.png, <id>-p<n>.png
"""
import sys, json, time, pathlib

ROOT = pathlib.Path(__file__).parent
STORIES = ROOT / "stories"
IMG = ROOT / "pages" / "img"; IMG.mkdir(parents=True, exist_ok=True)
MODEL = "gemini-2.5-flash-image"   # Nano Banana

# one shared art direction so every page looks like the same comic universe.
# WHOLESOME + culturally-appropriate for an Indian education brand (no pin-up / glamour).
STYLE = ("Modern clean webtoon / digital-comic illustration, crisp clean linework, soft cel shading with gentle "
         "gradients, vibrant but tasteful colours, expressive friendly faces. Palette leaning warm gold #f5b301 and "
         "navy #1a237e with warm natural Indian skin tones. Wholesome, respectful, professional tone for a university "
         "education brand. Realistic natural body proportions, modest decent attire (simple shirt / kurta / "
         "salwar-kameez / office wear), everyday Indian students and working professionals in a modern Indian "
         "setting. STRICTLY: fully clothed, modest, no glamour, no cleavage, no heavy makeup. No text, letters, "
         "words, speech bubbles or watermark. Square composition, leave a little headroom for an overlaid caption.")

# fixed character descriptors per story -> reused verbatim in every prompt for consistency
CHAR = {
  "bba-fees-reveal": "Consistent character AARAV: modest Indian teenage boy age 18 (fresh out of class 12), neat short black hair, simple casual shirt, warm brown skin, bright cheerful hopeful look, a young first-year college aspirant.",
  "bba-online": "Consistent character ADITYA: a cheerful modest Indian teenage boy, 18, neat short black hair, simple casual checked shirt, warm friendly face, a first-year college aspirant who helps run his family's small neighbourhood shop.",
}
# stable seed per story so the look stays coherent across its panels
SEED = {"bba-fees-reveal":111, "bba-online":121}

def pollinations(prompt, seed, out, tries=3):
    import urllib.request, urllib.parse
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width=1024&height=1024&nologo=true&model=flux&seed={seed}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(tries):
        try:
            data = urllib.request.urlopen(req, timeout=180).read()
            if len(data) < 3000:
                raise RuntimeError("tiny response")
            out.write_bytes(data)
            print(f"  saved {out.name} ({len(data)//1024} KB)")
            return True
        except Exception as ex:
            print(f"  retry {attempt+1}/{tries}: {str(ex)[:100]}")
            time.sleep(4*(attempt+1))
    print(f"  FAILED {out.name}")
    return False

def generate_free(only=None):
    for f in sorted(STORIES.glob("*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        sid = s["id"]
        if only and sid != only:
            continue
        print(f"\n=== {sid} (free / Pollinations FLUX) ===")
        seed = SEED.get(sid, 1); ch = CHAR.get(sid, "")
        pollinations(f"{STYLE} {ch} {s['hero']['art_prompt']}", seed, IMG/f"{sid}-hero.png")
        for p in s["panels"]:
            pollinations(f"{STYLE} {ch} {p['img_prompt']}", seed, IMG/f"{sid}-p{p['n']}.png")
    print("\nDone. Now run: py -3.12 build.py")

def load_key():
    for l in (ROOT/".env.local").read_text().splitlines():
        if l.startswith("GEMINI_API_KEY"):
            return l.split("=",1)[1].strip()
    raise SystemExit("GEMINI_API_KEY not found in .env.local")

def master_prompt(s):
    return (f"Character reference sheet. {STYLE} "
            f"Full-body and face close-up of the protagonist of this story: "
            f"{s['hero']['art_prompt']} "
            f"Establish a memorable, consistent look (face, hairstyle, outfit, skin tone) "
            f"to be reused across every comic panel.")

# ---------------- prompt pack (no API) ----------------
def write_pack():
    lines = ["# JAIN ONLINE — Nano Banana Prompt Pack",
             "",
             "Shared art direction (prepend to every prompt, or set once as system style):",
             "", "```", STYLE, "```", ""]
    lines += ["**How to use (free, AI Studio web UI):**",
              "1. Open https://aistudio.google.com → pick an image-capable model (Nano Banana / Gemini image).",
              "2. For each story: generate the **master** first, then drag it in as a reference image for the hero + each panel (keeps the character consistent).",
              "3. Download each result and save it into `pages/img/` with the **exact filename** shown under each prompt.",
              "4. When done: `py -3.12 build.py`  → images appear automatically. (Master image is reference-only; it isn't placed on the page.)",
              ""]
    for f in sorted(STORIES.glob("*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        sid = s["id"]
        lines += [f"\n## {sid} — {s['intent']} ({s['program']} / {s['specialization']})", ""]
        lines += [f"**1. Master character** → save as `pages/img/{sid}-master.png` (reference only):", "",
                  "```", master_prompt(s), "```", ""]
        lines += [f"**2. Hero image** → save as `pages/img/{sid}-hero.png`:", "",
                  "```", STYLE + " " + s['hero']['art_prompt'], "```", ""]
        for p in s["panels"]:
            lines += [f"**Panel {p['n']}** → save as `pages/img/{sid}-p{p['n']}.png`:", "",
                      "```", STYLE + " " + p["img_prompt"], "```", ""]
    (ROOT/"PROMPT_PACK.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote", ROOT/"PROMPT_PACK.md")

# ---------------- API generation ----------------
def gen(client, types, prompt, refs=None, out=None, tries=4):
    contents = [prompt]
    for r in (refs or []):
        contents.append(types.Part.from_bytes(data=r, mime_type="image/png"))
    for attempt in range(tries):
        try:
            resp = client.models.generate_content(model=MODEL, contents=contents)
            for part in resp.candidates[0].content.parts:
                if getattr(part, "inline_data", None) and part.inline_data.data:
                    out.write_bytes(part.inline_data.data)
                    print(f"  saved {out.name} ({out.stat().st_size//1024} KB)")
                    return out.read_bytes()
            print(f"  no image in response for {out.name}")
            return None
        except Exception as ex:
            wait = 5 * (attempt + 1)
            print(f"  retry {attempt+1}/{tries} after error: {str(ex)[:120]} ... sleeping {wait}s")
            time.sleep(wait)
    print(f"  FAILED {out.name}")
    return None

def generate(only=None, panels_only=False):
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=load_key())
    for f in sorted(STORIES.glob("*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        if only and s["id"] != only:
            continue
        print(f"\n=== {s['id']} ===")
        master_bytes = None
        mp = IMG / f"{s['id']}-master.png"
        if not panels_only:
            master_bytes = gen(client, types, master_prompt(s), out=mp)
            gen(client, types, STYLE + " " + s["hero"]["art_prompt"],
                refs=[master_bytes] if master_bytes else None, out=IMG/f"{s['id']}-hero.png")
        elif mp.exists():
            master_bytes = mp.read_bytes()
        for p in s["panels"]:
            gen(client, types, STYLE + " " + p["img_prompt"],
                refs=[master_bytes] if master_bytes else None,
                out=IMG/f"{s['id']}-p{p['n']}.png")
    print("\nDone. Now run: py -3.12 build.py")

if __name__ == "__main__":
    a = sys.argv[1:]
    only = a[a.index("--only")+1] if "--only" in a else None
    if "--pack" in a:
        write_pack()
    elif "--free" in a:
        generate_free(only=only)
    else:
        only = a[a.index("--only")+1] if "--only" in a else None
        generate(only=only, panels_only=("--panels-only" in a))
