#!/usr/bin/env python3
"""Package built pages into fully self-contained share/*.html (Bangers font embedded,
every img/ inlined as a data URI, 0 external requests, 0 raw non-ASCII).
Run: py -3.12 pack_all.py            (all pages)
     py -3.12 pack_all.py bba-aviation
"""
import re, sys, base64, pathlib, mimetypes
ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "pages"; IMG = PAGES / "img"; SHARE = ROOT / "share"; SHARE.mkdir(exist_ok=True)
FONT = pathlib.Path(r"C:\Users\User\AppData\Local\Temp\claude\C--Users-User\bd388a54-b6f8-40e3-9a14-52c06f539fb1\scratchpad\bangers-full.ttf")

# id -> share filename (keep the already-published fees name stable)
NAME = {
  "bba-fees-reveal": "JAIN-BBA-01-Fees.html",
  "bba-online": "JAIN-BBA-Online.html",
}
def share_name(sid):
    if sid in NAME: return NAME[sid]
    return "JAIN-" + sid.replace("bba-", "BBA-").title().replace("Bba", "BBA") + ".html"

def datauri(fn):
    mime = mimetypes.guess_type(fn)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode((IMG/fn).read_bytes()).decode()

def pack(sid):
    src = (PAGES/f"{sid}.html").read_text(encoding="utf-8")
    bang = base64.b64encode(FONT.read_bytes()).decode()
    face = ("<style>@font-face{font-family:'Bangers';font-style:normal;font-weight:400;font-display:swap;"
            "src:url(data:font/ttf;base64,"+bang+") format('truetype')}</style>")
    src = re.sub(r'<link href="https://fonts\.googleapis[^>]*>', face, src)
    src = re.sub(r'<link[^>]*fonts\.googleapis[^>]*>', '', src)
    src = re.sub(r"(src=)(['\"])img/([^'\"]+)\2", lambda m: f"{m.group(1)}{m.group(2)}{datauri(m.group(3))}{m.group(2)}", src)
    src = re.sub(r"(url\()(['\"]?)img/([^)'\"]+)\2\)", lambda m: f"{m.group(1)}{m.group(2)}{datauri(m.group(3))}{m.group(2)})", src)
    src = re.sub(r'href="img/([^"]+)"', lambda m: f'href="{datauri(m.group(1))}"', src)
    leftover = re.findall(r'img/[A-Za-z0-9_.-]+', src)
    assert not leftover, f"{sid}: unresolved {set(leftover)}"
    assert 'fonts.googleapis' not in src, f"{sid}: font link remains"
    assert sum(1 for c in src if ord(c) > 127) == 0, f"{sid}: non-ascii present"
    out = SHARE/share_name(sid)
    out.write_text(src, encoding="utf-8")
    print(f"  {sid:24} -> share/{out.name}  ({len(src)//1024} KB)")

if __name__ == "__main__":
    ids = sys.argv[1:] or [p.stem for p in sorted(PAGES.glob("*.html")) if p.stem.startswith("bba")]
    for sid in ids: pack(sid)
    print(f"\nPackaged {len(ids)} page(s) into {SHARE}")
