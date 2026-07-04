#!/usr/bin/env python3
"""
JAIN ONLINE — Comic Story landing-page generator (v2).
One pop-art comic template (faithful to comic style.pdf + App.pdf mobile) from a per-story JSON.

7 chapters: Origin · Setting the Target · Program Universe · Special Power ·
            Character Evolution · Meet Sensei · Final Showdown
+ mobile hamburger menu (navy comic overlay), fully responsive, no query strip.

Usage:
    py -3.12 build.py            # builds every stories/*.json into pages/<id>.html
    py -3.12 build.py fees-roi   # build a single story by id
"""
import json, sys, html, pathlib, math, base64

ROOT = pathlib.Path(__file__).parent
STORIES = ROOT / "stories"
PAGES = ROOT / "pages"; PAGES.mkdir(exist_ok=True)
IMG = PAGES / "img"

def _cloud_uri(fill="#fff", lobes=14, inner=0.90):
    """rounded comic speech-cloud shape as an SVG data URI (soft scalloped edge, black outline)."""
    cx, cy, rx, ry = 100, 62, 96, 58
    pts = []
    for i in range(lobes * 2):
        ang = math.pi * i / lobes
        r = 1.0 if i % 2 == 0 else inner
        pts.append(f"{cx + rx*r*math.cos(ang):.1f},{cy + ry*r*math.sin(ang):.1f}")
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 124">'
           f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#000" '
           'stroke-width="4" stroke-linejoin="round"/></svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

CLOUD_WHITE = _cloud_uri("#fff")
CLOUD_GOLD  = _cloud_uri("#f5b301")

def _burst_tail_uri(fill="#fff", spikes=15, inner=0.80, tail_i=10, tail_len=1.85):
    """spiky comic speech-BURST with a pointed tail (bottom-left) as an SVG data URI."""
    cx, cy, rx, ry = 100, 70, 96, 58
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        r = tail_len if i == tail_i else (1.0 if i % 2 == 0 else inner)
        pts.append(f"{cx + rx*r*math.cos(ang):.1f},{cy + ry*r*math.sin(ang):.1f}")
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 185">'
           f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#000" '
           'stroke-width="4" stroke-linejoin="round"/></svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

BURST_WHITE = _burst_tail_uri("#fff")

def _burst_up_uri(fill="#fff", spikes=15, inner=0.80, tail_i=22, tail_len=1.7):
    """spiky comic speech-burst with the pointed tail at the TOP (points up to the speaker)."""
    cx, cy, rx, ry = 100, 112, 96, 56
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        r = tail_len if i == tail_i else (1.0 if i % 2 == 0 else inner)
        pts.append(f"{cx + rx*r*math.cos(ang):.1f},{cy + ry*r*math.sin(ang):.1f}")
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 185" preserveAspectRatio="none">'
           f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#000" '
           'stroke-width="3" stroke-linejoin="round"/></svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
BURST_WHITE_UP = _burst_up_uri("#fff")

def _burst_down_uri(fill="#fff", spikes=16, inner=0.82, tail_i=8, tail_len=1.42):
    """naturally-proportioned WIDE comic speech-burst, tail at the bottom-centre (points down).
    viewBox aspect (285:150 ~ 1.9) matches the bubble box so it fills without distorting spikes."""
    cx, cy, rx, ry = 142, 62, 134, 56
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        r = tail_len if i == tail_i else (1.0 if i % 2 == 0 else inner)
        pts.append(f"{cx + rx*r*math.cos(ang):.1f},{cy + ry*r*math.sin(ang):.1f}")
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 285 150" preserveAspectRatio="none">'
           f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#000" '
           'stroke-width="2.6" stroke-linejoin="round"/></svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
BURST_WHITE_DOWN = _burst_down_uri("#fff")

# pop-art decoration SVGs (from brand assets)
STAR_SVG = ('<svg viewBox="0 0 43 42" fill="none" xmlns="http://www.w3.org/2000/svg">'
  '<path d="M19.1317 5.33203L25.0437 17.3095L38.2619 19.23L28.696 28.5541L30.9541 41.7207L19.1317 35.5046L7.30779 41.7207L9.56581 28.5541L0 19.23L13.2198 17.3095L19.1317 5.33203Z" fill="#231244"/>'
  '<path d="M21.581 1.71875L27.4914 13.6978L40.7113 15.6183L31.1453 24.9424L33.4034 38.1074L21.581 31.8914L9.7571 38.1074L12.0151 24.9424L2.44922 15.6183L15.6691 13.6978L21.581 1.71875Z" fill="white" stroke="#231244" stroke-width="1.52057" stroke-miterlimit="10"/></svg>')
BOLT_SVG = ('<svg viewBox="0 0 142 111" fill="none" xmlns="http://www.w3.org/2000/svg">'
  '<path d="M140.584 69.1563L63.1316 37.1348L73.5092 66.0528L0.420576 56.4363L0 110.101L93.0556 88.8433L93.5213 69.4688L140.584 69.1563Z" fill="#35110B"/>'
  '<path d="M140.585 69.1564L82.6688 8.57615L80.4813 39.2215L17.5055 0.900391L11.9902 56.0924L89.1549 67.9658L90.4364 47.4079L140.585 69.1564Z" fill="#E8B84B" stroke="#4C1C12" stroke-width="1.80119" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>'
  '<path d="M11.9902 56.0918L22.2075 79.7423L89.3197 77.0963L89.1549 67.9652L11.9902 56.0918Z" fill="#FFA02E" stroke="#4C1C12" stroke-width="1.80119" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>'
  '<path d="M140.586 69.1566L89.5703 61.3215L90.4376 47.4082L140.586 69.1566Z" fill="#FFA02E" stroke="#4C1C12" stroke-width="1.80119" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# small gold spark icon for the AI-tool chips (icon + label)
SPARK_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.2 6.8H21l-5.4 4 2.1 6.8L12 15.6 '
             '6.3 19.6l2.1-6.8L3 8.8h6.8z" fill="#f5b301" stroke="#000" stroke-width="1.4" stroke-linejoin="round"/></svg>')
# real brand marks for the "Powered by" row
MS_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="1" y="1" width="10" height="10" fill="#F25022"/>'
           '<rect x="13" y="1" width="10" height="10" fill="#7FBA00"/><rect x="1" y="13" width="10" height="10" fill="#00A4EF"/>'
           '<rect x="13" y="13" width="10" height="10" fill="#FFB900"/></svg>')
GOOGLE_MARK = ('<b style="color:#4285F4">G</b><b style="color:#EA4335">o</b><b style="color:#FBBC05">o</b>'
               '<b style="color:#4285F4">g</b><b style="color:#34A853">l</b><b style="color:#EA4335">e</b>')

# real brand SVG logos (fetched into pages/img/logos/); concept-skills fall back to the spark icon
TOOL_LOGOS = {"Power BI": "powerbi", "Python": "python", "MS Copilot": "copilot",
              "Excel": "excel", "Tableau": "tableau"}
def tool_icon(x):
    slug = TOOL_LOGOS.get(x)
    return f'<img class="lg" src="img/logos/{slug}.svg" alt="">' if slug else SPARK_SVG

def cred_html(x):
    if x == "Google":    return '<span class="cr brand"><img class="lg" src="img/logos/google.svg" alt="">Google</span>'
    if x == "Microsoft": return '<span class="cr brand"><img class="lg" src="img/logos/microsoft.svg" alt="">Microsoft</span>'
    return f'<span class="cr">{x}</span>'

def e(s):
    return html.escape(str(s), quote=True)

def img_url(name):
    """relative url if the asset exists (tries .jpg then the given ext), else None"""
    stem = name.rsplit(".", 1)[0]
    for ext in (".jpg", ".png"):
        if (IMG / (stem + ext)).exists():
            return f"img/{stem}{ext}"
    return None

# ---------------------------------------------------------------- shared JAIN content (same on every page)
NAV = [("01","The Origin","#ch1"),("02","Setting the Target","#ch2"),
       ("03","The Program Universe","#ch3"),("04","Special Power","#ch4"),
       ("05","Character Evolution","#ch5"),("06","Meet Sensei","#ch6")]

PROGRAMS = [
  ("01","finance","BBA in Finance","3-Year UG · ₹45,000/year","45k","Numbers are my superpower!"),
  ("02","marketing","BBA in Marketing","3-Year UG · ₹45,000/year","45k","I'll build brands people love!"),
  ("03","hr","BBA in Human Resource Mgmt","3-Year UG · ₹45,000/year","45k","People are my strength!"),
  ("04","digital","BBA in Digital Marketing","3-Year UG · ₹50,000/year","50k","I'll go viral, the smart way!"),
  ("05","datasci","BBA in Data Science & AI","3-Year UG · ₹50,000/year","50k","I'll make data talk!"),
]

AI_TOOLS = ["Prompt Engineering","Power BI","Python","MS Copilot","Microsoft Fabric","Generative AI",
            "Financial Modelling","Data Analytics","Business Analytics","Excel","Tableau","Design Thinking"]
CREDENTIALS = ["Google","Microsoft","Industry Experts"]
LINKEDIN_CHIPS = ["Weekend Live Classes","Batch Owner Support","Virtual Labs","Sunday Social Network"]

SENSEI_CHIPS = ["What's the BBA fee?","Can I pay in EMI?",
                "Am I eligible after 12th?","Which BBA elective suits me?"]

# ---- Chapter 6 live chat ----
# Paste the Sensei chat EMBED URL here (from your boss / the Sensei dev) to go live on ALL pages.
# Leave blank ("") to keep showing the static chat mock-up.
# NOTE: Sensei must (1) be served over HTTPS and (2) allow being iframed on your landing-page
# domain (its Content-Security-Policy 'frame-ancestors' must include your domain).
SENSEI_EMBED_URL = ""

# footer social links (label, href, inline-svg path)
SOCIAL = [
 ("X","https://twitter.com/jainonline","M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"),
 ("Facebook","https://facebook.com/jainonline","M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.9h2.54V9.85c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.23.2 2.23.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.88h2.78l-.44 2.9h-2.34V22c4.78-.79 8.44-4.94 8.44-9.94z"),
 ("Instagram","https://instagram.com/jainonline","M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07zm0 3.34A6.5 6.5 0 1 0 18.5 12 6.5 6.5 0 0 0 12 5.5zm0 10.72A4.22 4.22 0 1 1 16.22 12 4.22 4.22 0 0 1 12 16.22zm6.76-10.9a1.52 1.52 0 1 1-1.52-1.52 1.52 1.52 0 0 1 1.52 1.52z"),
 ("LinkedIn","https://linkedin.com/company/jainonline","M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.55V9h3.57v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"),
 ("YouTube","https://youtube.com/@jainonline","M23.5 6.2a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.51A3.02 3.02 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3.02 3.02 0 0 0 2.12 2.14c1.88.51 9.38.51 9.38.51s7.5 0 9.38-.51a3.02 3.02 0 0 0 2.12-2.14A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8zM9.55 15.57V8.43L15.82 12z"),
]

# ---------------------------------------------------------------- CSS
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
/* DISCIPLINED PALETTE — only 4 colours: one blue (navy), one yellow (gold), white, black.
   The old accent vars (red/purple/blue/green) are remapped onto navy/black so nothing off-brand can appear. */
:root{--navy:#1a237e;--ink:#111;--gold:#f5b301;--gold2:#f5b301;--paper:#fdf3da;
  --red:#1a237e;--purple:#111111;--blue:#1a237e;--green:#1a237e}
html{scroll-behavior:smooth;overflow-x:clip}
body{font-family:'Inter',system-ui,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--paper);line-height:1.5;overflow-x:clip}
.display,h1,h2,h3,.chip,.bangers{font-family:'Bangers','Anton','Arial Black',Impact,sans-serif;letter-spacing:.02em;font-weight:400}
.wrap{max-width:1280px;margin:0 auto;padding:0 16px}
.halftone{background-image:radial-gradient(var(--dot,#0001) 1.4px,transparent 1.5px);background-size:9px 9px}
img{max-width:100%}
/* ---------- header ---------- */
header.bar{background:var(--navy);color:#fff;position:sticky;top:0;z-index:60;border-bottom:4px solid #000}
.bar .wrap{display:flex;align-items:center;justify-content:space-between;height:60px}
.logo{display:inline-flex;align-items:center;text-decoration:none}
.logo .chip{background:#fff;border:3px solid #000;box-shadow:3px 3px 0 #000;padding:5px 10px;display:flex;align-items:center}
.logo .chip img{height:30px;display:block}
.navcta{background:var(--gold);color:#111;border:3px solid #000;padding:8px 15px;font-family:'Bangers',sans-serif;
  font-size:17px;text-decoration:none;box-shadow:3px 3px 0 #000;display:none}
.hamburger{display:inline-flex;flex-direction:column;gap:5px;background:none;border:0;cursor:pointer;padding:8px;margin-left:12px}
.hamburger span{width:26px;height:3px;background:#fff;display:block;border-radius:2px}
.navtoggle{position:absolute;opacity:0;pointer-events:none}
/* ---------- nav overlay (navy comic, like the SVG) ---------- */
.overlay{position:fixed;inset:0;z-index:80;background:var(--navy);border:4px solid #000;
  transform:translateX(100%);transition:transform .28s ease;display:flex;flex-direction:column;
  padding:28px 22px 26px;overflow-y:auto}
.navtoggle:checked ~ .overlay{transform:translateX(0)}
.overlay .ohead{display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid #ffffff26;padding-bottom:14px;margin-bottom:6px}
.overlay .ohead .ttl{font-family:'Bangers',sans-serif;color:#ffebc8;font-size:30px}
.overlay .close{font-size:34px;color:#fff;background:none;border:0;cursor:pointer;line-height:1;padding:0 6px}
.overlay a.item{display:flex;align-items:center;gap:14px;text-decoration:none;color:#fff;
  padding:16px 4px;border-bottom:1px solid #ffffff1f}
.overlay a.item .n{font-family:'Bangers',sans-serif;color:var(--gold2);font-size:24px;min-width:34px}
.overlay a.item .l{font-family:'Bangers',sans-serif;font-size:22px;letter-spacing:.5px;color:#fff}
.overlay a.item:hover .l{color:var(--gold)}
.overlay .octa{margin-top:auto;background:var(--gold2);color:#111;border:3px solid #000;text-align:center;
  font-family:'Bangers',sans-serif;font-size:22px;padding:14px;text-decoration:none;box-shadow:4px 4px 0 #000}
/* ---------- chapter labels ---------- */
.chapter{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:30px 0 12px}
.chapter .tag{background:var(--gold);color:#000;font-family:'Bangers',sans-serif;font-size:18px;padding:6px 16px;letter-spacing:.5px;border:2px solid #000;box-shadow:3px 3px 0 #000}
.chapter .pg{background:#fff;border:3px solid #000;font-family:'Bangers',sans-serif;padding:4px 10px;font-size:14px;white-space:nowrap}
/* each chapter enclosed as a comic 'page' */
.cpage{border:3px solid #000;background:var(--paper);padding:8px 20px 24px;margin:24px 0;box-shadow:8px 8px 0 rgba(0,0,0,.13)}
.cpage>.chapter:first-child{margin-top:14px}
/* ---------- hero ---------- */
.frame{border:4px solid #000;background:#fff;position:relative;overflow:hidden;box-shadow:6px 6px 0 #0002}
.hero{border:5px solid #000;background:#fff;position:relative;overflow:hidden;box-shadow:8px 8px 0 #0002}
.hero .grid{display:grid;grid-template-columns:1fr 1fr}
.hero .copy{padding:48px 34px;display:flex;flex-direction:column;justify-content:flex-start}
.eyebrow{display:inline-block;align-self:flex-start;background:#000;color:var(--gold);font-family:'Bangers',sans-serif;font-size:13px;padding:4px 11px;margin-bottom:12px;letter-spacing:.6px}
.hero h1{font-size:54px;line-height:.92;margin:6px 0 14px;text-transform:uppercase;text-wrap:balance}
.hero h1 .hl{color:var(--gold);-webkit-text-stroke:2px #000}
.hero p.sub{font-size:16px;max-width:46ch;color:#222;margin-bottom:22px}
.hero .btnrow{margin-top:auto}
.btnrow{display:flex;gap:12px;flex-wrap:wrap}
.btn{font-family:'Bangers',sans-serif;font-size:19px;padding:12px 20px;border:3px solid #000;text-decoration:none;box-shadow:4px 4px 0 #000;cursor:pointer;display:inline-block;text-align:center;transition:transform .12s ease,box-shadow .12s ease}
.btn.gold{background:var(--gold);color:#111;animation:ctaGlow 1.7s ease-in-out infinite}
.btn.ghost{background:#fff;color:#111}
.btn:hover{transform:translate(-3px,-3px);box-shadow:7px 7px 0 #000}
.btn.gold:hover{animation:ctaWiggle .4s ease-in-out}
.btn:active{transform:translate(3px,3px);box-shadow:1px 1px 0 #000}
@keyframes ctaGlow{0%,100%{filter:drop-shadow(0 0 0 rgba(245,179,1,0))}50%{filter:drop-shadow(0 0 10px rgba(245,179,1,.9))}}
@keyframes ctaWiggle{0%,100%{transform:translate(-3px,-3px) rotate(0)}25%{transform:translate(-3px,-3px) rotate(-1.5deg)}75%{transform:translate(-3px,-3px) rotate(1.5deg)}}
/* consistent hover for the other CTA-style buttons */
.navcta,.pcard .view,.overlay .octa,.sensei .inrow .send,.askbar{transition:transform .12s ease,box-shadow .12s ease,background .12s ease}
.navcta:hover,.overlay .octa:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 #000}
.navcta{animation:ctaGlow 1.7s ease-in-out infinite}
.pcard .view:hover{transform:translate(-2px,-2px);box-shadow:4px 4px 0 #000;background:#111;color:var(--gold)}
.sensei .inrow .send:hover{background:#111;color:var(--gold)}
.sensei .inrow .send:hover svg{fill:var(--gold)}
.askbar:hover{background:#111;letter-spacing:.5px}
.hero .art{position:relative;border-left:5px solid #000;min-height:440px;background:var(--navy);background-size:cover;background-position:50% 30%}
.burst{position:absolute;font-family:'Bangers',sans-serif;color:#fff;-webkit-text-stroke:2px #000;font-size:38px;transform:rotate(-10deg)}
.prompt{position:absolute;left:10px;right:10px;font-size:10px;color:#9a7b00;background:#fff8e0;border:1px dashed #caa64a;padding:5px 7px;z-index:2;line-height:1.3}
.prompt b{color:#7a5e00}
/* stats */
.statbar{background:var(--gold);border:4px solid #000;margin-top:-2px;display:grid;grid-template-columns:repeat(4,1fr)}
.stat{text-align:center;padding:14px 8px;border-right:2px solid #0002}
.stat:last-child{border-right:0}
.stat b{font-family:'Bangers',sans-serif;font-size:26px;display:block;line-height:1}
.stat span{font-size:11px;text-transform:uppercase;letter-spacing:.5px;font-weight:700}
.askbar{display:block;background:#000;color:var(--gold);text-align:center;font-family:'Bangers',sans-serif;
  font-size:20px;padding:12px;border:4px solid #000;border-top:0;text-decoration:none}
/* ---------- story panels (Ch2) ---------- */
.panels{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.panel{min-height:380px}
.panel .art-ph{position:absolute;inset:0;background:repeating-linear-gradient(45deg,#fff,#fff 16px,#faf3df 16px,#faf3df 32px);background-size:cover;background-position:center}
.panel .num{position:absolute;top:0;left:0;background:#000;color:var(--gold);font-family:'Bangers',sans-serif;font-size:17px;padding:2px 9px;z-index:3}
.panel .pprompt{position:absolute;top:32px;left:9px;right:9px;font-size:10px;color:#9a7b00;background:#fff8e0;border:1px dashed #caa64a;padding:5px 7px;z-index:2;line-height:1.3}
.narr{position:absolute;left:9px;bottom:9px;max-width:calc(100% - 90px);background:var(--gold);border:3px solid #000;
  padding:10px 14px;font-size:13px;line-height:1.32;font-weight:700;color:#000;text-align:left;z-index:4;
  box-shadow:3px 3px 0 rgba(0,0,0,.28)}
.bubble{position:absolute;right:6px;top:4px;width:250px;max-width:calc(100% - 14px);min-height:158px;background:url('__BURSTW__') no-repeat;background-size:100% 100%;
  padding:32px 58px 66px;font-size:12px;line-height:1.3;font-weight:700;color:#000;text-align:center;z-index:5;
  display:flex;align-items:center;justify-content:center;filter:drop-shadow(3px 3px 0 rgba(0,0,0,.22))}
.lesson{border:4px solid #000;background:var(--navy);color:#fff;padding:22px 26px;margin-top:14px;box-shadow:6px 6px 0 #0002}
.lesson h3{font-size:26px;color:var(--gold);margin-bottom:12px;text-transform:uppercase}
.lesson ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.lesson li{display:flex;gap:9px;font-size:14px;align-items:flex-start}
.lesson li .k{font-family:'Bangers',sans-serif;color:var(--gold);font-size:19px;line-height:1}
/* ---------- Ch3 Program Universe ---------- */
.tabs{display:flex;gap:0;border:4px solid #000;background:#fff;margin-bottom:14px;overflow:hidden}
.tabs button{flex:1;font-family:'Bangers',sans-serif;font-size:16px;padding:11px 6px;background:#fff;border:0;border-right:3px solid #000;cursor:pointer;color:#111}
.tabs button:last-child{border-right:0}
.tabs button.active{background:var(--gold)}
.cardscroll{display:flex;align-items:flex-start;gap:14px;overflow-x:auto;padding-bottom:8px;scroll-snap-type:x mandatory}
.pcard{flex:0 0 300px;scroll-snap-align:start;border:4px solid #000;background:#fff;box-shadow:5px 5px 0 #0002;display:flex;flex-direction:column}
.pcard .thumb{height:230px;border-bottom:4px solid #000;background:var(--gold);position:relative;background-size:cover;background-position:center top}
.pcard .thumb .num{position:absolute;top:0;right:0;background:#000;color:var(--gold);font-family:'Bangers',sans-serif;padding:2px 9px;font-size:16px}
.pcard .thumb .bubble2{position:absolute;left:8px;bottom:8px;right:8px;background:#fff;border:2px solid #000;border-radius:10px;padding:5px 8px;font-size:11px;font-weight:600}
.pcard .pbody{padding:14px;display:flex;flex-direction:column;gap:8px;flex:1}
.pcard h3{font-family:'Bangers',sans-serif;font-size:19px;line-height:1.05}
.pcard .meta{font-size:12px;color:#444;font-weight:600}
.pcard .view{margin-top:auto;font-family:'Bangers',sans-serif;background:var(--gold);border:3px solid #000;padding:8px;text-align:center;font-size:15px;text-decoration:none;color:#111}
/* ---------- Ch4 Special Power ---------- */
.power{border:4px solid #000;color:#fff;margin-bottom:16px;box-shadow:6px 6px 0 #0002;position:relative;display:grid;grid-template-columns:210px 1fr;overflow:hidden}
.power.p1{background:var(--navy)}.power.p2{background:#111}.power.p3{background:var(--navy)}
.power .pimg{border-right:4px solid #000;background:#0a0f2c center/cover no-repeat;min-height:270px}
.power .pbodyc{padding:30px 30px;display:flex;flex-direction:column;justify-content:center}
.power .lab{position:absolute;top:0;right:0;background:#fff;color:#111;border-left:3px solid #000;border-bottom:3px solid #000;font-family:'Bangers',sans-serif;font-size:13px;padding:3px 12px;z-index:2}
.power h3{font-size:26px;margin-bottom:6px;text-transform:uppercase}
.power p{font-size:14px;opacity:.95;margin-bottom:14px;max-width:60ch}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips .c{background:#ffffff1a;border:2px solid #fff;border-radius:20px;padding:5px 12px 5px 8px;font-size:12.5px;font-weight:600;display:inline-flex;align-items:center;gap:6px}
.chips .c svg{width:15px;height:15px;flex:0 0 auto}
.chips .c img.lg{width:17px;height:17px;object-fit:contain;flex:0 0 auto;display:block}
.creds .cr.brand img.lg{width:20px;height:20px;object-fit:contain;display:block}
.creds{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.creds .cr{background:#fff;color:#111;font-family:'Bangers',sans-serif;font-size:20px;padding:8px 16px;border:2px solid #000;display:inline-flex;align-items:center}
.creds .cr.brand{font-family:'Inter',sans-serif;font-weight:800;font-size:16px;gap:8px}
.creds .cr.brand svg{width:20px;height:20px}
.creds .cr.ggl{font-family:'Inter','Arial',sans-serif;font-weight:800;font-size:19px;letter-spacing:-.5px}
.poweredby{font-size:11px;text-transform:uppercase;letter-spacing:1px;opacity:.85;margin-right:6px;align-self:center}
/* ---------- collapsible chip groups (mobile 'show all') ---------- */
.col-chk{display:none}
.col-more{display:none}
.qchips{display:flex;flex-wrap:wrap;gap:8px}
.qcol{flex:1;min-width:0}
/* ---------- Ch5 Character Evolution (4 story cards) ---------- */
.evos{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.evo{border:3px solid #000;background:#fff;overflow:hidden;box-shadow:5px 5px 0 #0002;display:flex;flex-direction:column;min-height:370px}
.evo .top{padding:9px 12px;color:#fff;display:flex;justify-content:space-between;align-items:center;background:var(--navy);border-bottom:3px solid #000}
.evo.alt .top{background:#111}
.evo .top .sid{font-size:10px;font-weight:800;letter-spacing:1px}
.evo .metric{font-family:'Bangers',sans-serif;font-size:19px;color:var(--gold);white-space:nowrap}
.evo .body{padding:15px 14px 16px;display:flex;flex-direction:column;gap:13px;flex:1}
.evo .nm{display:flex;justify-content:space-between;align-items:center;gap:6px}
.evo .nm .who{font-family:'Bangers',sans-serif;font-size:18px;line-height:1}
.evo .badge{background:var(--gold);color:#111;border:2px solid #000;font-family:'Bangers',sans-serif;font-size:10.5px;padding:2px 7px;white-space:nowrap}
.evo .rolebox{border:2px solid #000;padding:8px 10px}
.evo .rolebox .r{display:flex;justify-content:space-between;align-items:baseline;gap:6px}
.evo .rolebox .rr{font-weight:800;font-size:12px}
.evo .rolebox .rs{font-family:'Bangers',sans-serif;font-size:15px;color:var(--navy)}
.evo .rolebox .tag{display:inline-flex;align-items:center;gap:5px;margin-top:7px;background:var(--navy);color:#fff;font-size:9px;font-weight:700;letter-spacing:.5px;padding:3px 7px}
.evo .rolebox .tag img{height:12px;display:block;background:#fff;border-radius:50%}
.evo .qbubble{background:var(--paper);border:2px solid #000;border-radius:12px;padding:9px 11px;font-size:11.5px;font-style:italic;color:#222;box-shadow:2px 2px 0 #0002;margin-top:auto}
.facts{border:4px solid #000;background:#111;color:#fff;padding:18px 20px;margin-top:16px;box-shadow:6px 6px 0 #0002}
.facts h3{font-size:22px;color:var(--gold);margin-bottom:10px;text-transform:uppercase}
.facts .frow{display:grid;grid-template-columns:1fr 1fr;gap:2px 24px}
.facts .row{display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #ffffff26;font-size:13.5px}
.facts .row b{font-family:'Bangers',sans-serif;font-size:18px;color:var(--gold);min-width:84px}
/* ---------- Ch6 Meet Sensei (gold header, cream body) ---------- */
.sensei{border:4px solid #000;background:var(--paper);color:#111;overflow:hidden;box-shadow:6px 6px 0 #0002}
.sensei .shead{padding:12px 18px;display:flex;align-items:center;gap:12px;border-bottom:4px solid #000;background:var(--gold)}
.sensei .avatar{width:38px;height:38px;background:#111;display:flex;align-items:center;justify-content:center;font-family:'Bangers',sans-serif;color:var(--gold);font-size:20px;border:2px solid #000}
.sensei .shead .nm{font-family:'Bangers',sans-serif;font-size:20px;color:#111;line-height:1}
.sensei .shead .sub{font-size:10.5px;color:#5a4a00;font-weight:800;letter-spacing:.6px;text-transform:uppercase}
.sensei .shead .on{font-size:11px;color:#0b7a30;margin-left:auto;font-weight:800}
.sensei .chatbody{padding:20px 18px;display:flex;flex-direction:column;gap:12px;min-height:120px}
.sensei .mrow{display:flex;gap:10px;align-items:flex-start}
.sensei .mavatar{width:30px;height:30px;background:var(--gold);border:2px solid #000;display:flex;align-items:center;justify-content:center;font-family:'Bangers',sans-serif;color:#111;font-size:15px;flex:0 0 auto}
.sensei .msg{background:#fff;border:2px solid #000;border-radius:14px;padding:11px 14px;font-size:13.5px;max-width:80%;box-shadow:3px 3px 0 #0002;color:#111;line-height:1.5}
.sensei .qrow{padding:14px 18px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;border-top:2px solid #0001}
.sensei .qlabel{font-family:'Bangers',sans-serif;font-size:15px;color:#111;letter-spacing:.5px}
.sensei .qrow button{background:#fff;color:#111;border:2px solid #000;border-radius:6px;padding:7px 12px;font-size:12px;font-weight:700;cursor:pointer;box-shadow:2px 2px 0 #0002}
.sensei .qrow button:hover{background:var(--gold)}
.sensei .inrow{display:flex;gap:0;border-top:4px solid #000}
.sensei .inrow input{flex:1;background:#fff;border:0;color:#111;padding:14px 16px;font-size:14px}
.sensei .inrow .send{background:var(--gold);color:#111;border:0;border-left:4px solid #000;font-family:'Bangers',sans-serif;font-size:16px;padding:0 22px;cursor:pointer;display:flex;align-items:center;gap:7px}
.sensei .inrow .send svg{width:16px;height:16px;fill:#111}
.sensei .sensei-frame{display:block;width:100%;height:600px;border:0;background:var(--paper)}
@media(max-width:780px){.sensei .sensei-frame{height:520px}}
/* ---------- Ch7 Final ---------- */
.final{border:5px solid #000;background:#000;color:#fff;position:relative;overflow:hidden}
.final .fgrid{display:grid;grid-template-columns:1.05fr .95fr;align-items:center;gap:10px}
.final .fcopy{padding:60px 34px}
.final .fart{padding:16px 22px 16px 0}
.final .fart img{width:100%;height:auto;display:block}
.final h2{font-size:46px;color:#fff;text-transform:uppercase;line-height:.95;text-wrap:balance}
.final h2 .hl{color:var(--gold)}
.final p{margin:14px 0 22px;font-size:16px;max-width:48ch;color:#eee}
footer{background:var(--navy);color:#e7e8f5;margin-top:28px;border-top:5px solid #000}
footer .fcol{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:30px 40px;max-width:1280px;margin:0 auto;padding:36px 22px 28px}
footer .fleft{flex:1 1 300px;display:flex;flex-direction:column;gap:16px;align-items:flex-start}
footer .flogo{background:#fff;border:3px solid #000;box-shadow:4px 4px 0 #000;padding:7px 11px;display:inline-flex}
footer .flogo img{height:30px;display:block}
footer .fbul{list-style:disc;padding-left:20px;color:#c4c6e6;font-size:13.5px;line-height:1.8;max-width:46ch}
footer .fask{position:relative;flex:0 1 470px;background:#fff;color:#111;border:3px solid #000;box-shadow:8px 8px 0 rgba(0,0,0,.4);padding:22px 24px}
footer .fask .qmark{position:absolute;top:-30px;right:16px;font-family:'Bangers',sans-serif;font-size:66px;line-height:1;color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke;text-shadow:3px 3px 0 rgba(0,0,0,.28);transform:rotate(6deg)}
footer .fask h3{font-family:'Bangers',sans-serif;font-size:25px;letter-spacing:.5px;margin-bottom:8px;color:#111}
footer .fask p{font-size:13.5px;color:#333;line-height:1.55;margin-bottom:16px;max-width:52ch}
footer .fask .btn{font-size:16px;padding:10px 16px}
footer .copywrap{border-top:2px dashed #ffffff40;margin:0 22px}
footer .copyline2{max-width:1280px;margin:0 auto;padding:15px 0;text-align:center;font-size:12.5px;color:#c9cbe6}
/* ---------- responsive ---------- */
@media(min-width:781px){.navcta{display:inline-block}.overlay{max-width:420px;left:auto;right:0;border-left:6px solid #000}}
@media(max-width:780px){
  /* wider chapters, no comic page-frame on mobile (more usable width, less bulk) */
  .wrap{padding:0 7px}
  .cpage{border:0;box-shadow:none;background:transparent;padding:0;margin:14px 0}
  .cpage>.chapter:first-child{margin-top:20px}
  .hero .grid{grid-template-columns:1fr}.hero .art{min-height:250px;border-left:0;border-top:5px solid #000}
  .hero h1{font-size:34px;overflow-wrap:break-word;word-break:break-word}.hero .copy{padding:24px 20px}.hero .btnrow{margin-top:20px}
  /* single-line, shorter button rows */
  .btnrow{flex-wrap:nowrap}.btnrow .btn{flex:1;padding:10px 8px;font-size:15px;box-shadow:3px 3px 0 #000;white-space:nowrap}
  .askbar{font-size:13px;padding:10px 8px;line-height:1.25}
  /* collapse chip groups to ~2 lines with a Show all toggle */
  .col-body{max-height:74px;overflow:hidden;transition:max-height .35s ease}
  .col-chk:checked ~ .col-body{max-height:900px}
  .col-more{display:inline-flex;align-items:center;margin-top:10px;font-family:'Bangers',sans-serif;font-size:13px;
    letter-spacing:.5px;color:inherit;background:transparent;border:2px solid currentColor;border-radius:20px;
    padding:3px 13px;cursor:pointer;opacity:.9}
  .col-more::after{content:'+ SHOW ALL'}
  .col-chk:checked ~ .col-more::after{content:'\\2212 SHOW LESS'}
  .sensei .chatbody{min-height:0;padding:14px 16px}
  .panels{grid-template-columns:1fr}
  /* MOBILE: comic overlay - yellow narration inside the image bottom (older style),
     white speech burst mostly ABOVE the image with only its tail dipping in. Tight gaps. */
  .panels{gap:0}
  .panel{position:relative;aspect-ratio:3/2;min-height:0;overflow:visible;margin:150px 0 0;display:block}
  .panel .art-ph{position:absolute;inset:0;width:auto}
  .panel .narr{position:absolute;left:8px;right:8px;bottom:8px;top:auto;width:auto;max-width:none;min-height:0;
    margin:0;filter:none;background-image:none;background:var(--gold);border:3px solid #000;
    box-shadow:3px 3px 0 rgba(0,0,0,.25);padding:8px 12px;font-size:12.5px;line-height:1.35;text-align:left}
  .panel .bubble{position:absolute;left:50%;top:-134px;transform:translateX(-50%);right:auto;bottom:auto;
    width:min(288px,90%);max-width:none;min-height:0;aspect-ratio:285/150;margin:0;z-index:6;
    background:url('__BURSTDN__') no-repeat center/100% 100%;border:0;border-radius:0;box-shadow:none;
    padding:24px 46px 40px;font-size:13px;line-height:1.32;text-align:center;
    display:flex;align-items:center;justify-content:center;filter:drop-shadow(3px 3px 0 rgba(0,0,0,.22))}
  .panel .bubble::before,.panel .bubble::after{display:none}
  .lesson ul{grid-template-columns:1fr}
  .evos{display:flex;grid-template-columns:none;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;padding-bottom:8px;-webkit-overflow-scrolling:touch}
  .evo{flex:0 0 82%;scroll-snap-align:start}
  .power{grid-template-columns:1fr}.power .pimg{min-height:0;aspect-ratio:3/4;border-right:0;border-bottom:4px solid #000;background-position:center top}
  .power .pbodyc{padding:18px 20px}
  .facts .frow{grid-template-columns:1fr}
  .final .fgrid{grid-template-columns:1fr}
  .final .fart{padding:0 22px 26px;max-width:440px;margin:0 auto}
  .final h2{font-size:32px}
  .stat b{font-size:21px}.stat span{font-size:9.5px}
}
@media(max-width:520px){.evos{grid-template-columns:1fr}}
@media(max-width:430px){.statbar{grid-template-columns:repeat(2,1fr)}.stat:nth-child(2){border-right:0}.stat{border-bottom:2px solid #0002}}
@media(prefers-reduced-motion:reduce){.overlay{transition:none}html{scroll-behavior:auto}.btn.gold,.navcta{animation:none}}
"""
CSS = CSS.replace("__CLOUDW__", CLOUD_WHITE).replace("__CLOUDG__", CLOUD_GOLD).replace("__BURSTW__", BURST_WHITE).replace("__BURSTUP__", BURST_WHITE_UP).replace("__BURSTDN__", BURST_WHITE_DOWN)

JS = """
(function(){
  var t=document.getElementById('navtoggle');
  function closeMenu(){ if(t) t.checked=false; }
  // close overlay when a nav link / close button is clicked
  document.querySelectorAll('.overlay a, #navclose').forEach(function(el){
    el.addEventListener('click',closeMenu);
  });
  // close on Escape
  document.addEventListener('keydown',function(ev){ if(ev.key==='Escape') closeMenu(); });
  // program tabs filter
  document.querySelectorAll('.tabs button').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.tabs button').forEach(function(x){x.classList.remove('active');});
      b.classList.add('active');
      var f=b.getAttribute('data-f');
      document.querySelectorAll('.pcard').forEach(function(c){
        c.style.display=(f==='all'||c.getAttribute('data-level')===f)?'flex':'none';
      });
    });
  });
  // sensei suggested questions -> fill input
  var inp=document.getElementById('senseiInput');
  document.querySelectorAll('.sensei .qrow button').forEach(function(b){
    b.addEventListener('click',function(){ if(inp){inp.value=b.textContent; inp.focus();} });
  });
})();
"""

# ---------------------------------------------------------------- partials
def collapse(inner, cid):
    """wrap a chip group so it clamps to ~2 lines on mobile with a Show all / Show less toggle."""
    return (f'<div class="collapse"><input type="checkbox" id="{cid}" class="col-chk">'
            f'{inner}<label for="{cid}" class="col-more"></label></div>')

def panel_html(p, sid):
    narr = e(p.get("narration","")); bub = e(p.get("dialogue",""))
    u = img_url(f"{sid}-p{p.get('n','')}.png")
    if u:
        art = f'<div class="art-ph" style="background-image:url(\'{u}\')"></div>'; prm = ""
    else:
        art = '<div class="art-ph"></div>'
        prm = f'<div class="pprompt"><b>AI ART:</b> {e(p.get("img_prompt",""))}</div>'
    return f"""<div class="frame panel halftone" style="--dot:#0000000d">{art}
      <div class="num">{e(p.get('n',''))}</div>{prm}
      {f'<div class="narr">{narr}</div>' if narr else ''}
      {f'<div class="bubble">{bub}</div>' if bub else ''}</div>"""

def program_cards():
    out=[]
    for num,key,title,meta,level,line in PROGRAMS:
        u = img_url(f"prog-{key}.png")
        thumb = f'background-image:url(\'{u}\')' if u else ''
        out.append(f"""<div class="pcard" data-level="{level}">
          <div class="thumb" style="{thumb}"><span class="num">{num}</span>
            <div class="bubble2">{e(line)}</div></div>
          <div class="pbody"><h3>{e(title)}</h3><div class="meta">{e(meta)}</div>
            <a class="view" href="#cta">VIEW PROGRAM &rarr;</a></div></div>""")
    return "\n".join(out)

def nav_overlay():
    items="".join(f'<a class="item" href="{href}"><span class="n">{n}</span><span class="l">{e(lab)}</span></a>'
                  for n,lab,href in NAV)
    return f"""<input type="checkbox" id="navtoggle" class="navtoggle" aria-hidden="true">
    <nav class="overlay" aria-label="Menu">
      <div class="ohead"><span class="ttl">MENU</span><button type="button" class="close" id="navclose" aria-label="Close menu">&times;</button></div>
      {items}
      <a class="octa" href="#cta">APPLY NOW &rarr;</a>
    </nav>"""

# ---------------------------------------------------------------- render
def render(s):
    panels = "\n".join(panel_html(p, s["id"]) for p in s["panels"])
    stats = "".join(f'<div class="stat"><b>{e(x["big"])}</b><span>{e(x["label"])}</span></div>' for x in s["statbar"])
    lesson_li = "".join(f'<li><span class="k">{i+1}</span><div>{e(pt)}</div></li>' for i,pt in enumerate(s["turn"]["points"]))
    tst = s["proof"].get("testimonials") or [s["proof"]["testimonial"]]
    fav = img_url("favicon.png") or ""
    def _evo(i, tt):
        cls = "evo" if i % 2 == 0 else "evo alt"
        logo = f'<img src="{fav}" alt="">' if fav else ""
        return (f'<div class="{cls}"><div class="top"><span class="sid">STORY.{i+1:02d}</span>'
                f'<span class="metric">{e(tt.get("metric",""))}</span></div>'
                f'<div class="body"><div class="nm"><span class="who">{e(tt.get("name",""))}</span>'
                f'<span class="badge">{e(tt.get("spec",""))}</span></div>'
                f'<div class="rolebox"><div class="r"><span class="rr">{e(tt.get("role",""))}</span>'
                f'<span class="rs">{e(tt.get("stat",""))}</span></div>'
                f'<span class="tag">{logo}JAIN ONLINE</span></div>'
                f'<div class="qbubble">"{e(tt.get("quote",""))}"</div></div></div>')
    evo_cards = "".join(_evo(i, tt) for i, tt in enumerate(tst))
    facts = "".join(f'<div class="row"><b>{e(f["k"])}</b><div>{e(f["v"])}</div></div>' for f in s["proof"]["facts"])
    p1img = img_url("ch4-ai.png") or ""
    p2img = img_url("ch4-cred.png") or ""
    p3img = img_url("ch4-learn.png") or ""
    cta_img = img_url("cta-pop.png") or ""
    fart = f'<div class="fart"><img src="{cta_img}" alt=""></div>' if cta_img else ""
    social = "".join(
        f'<a href="{h}" aria-label="{e(nm)}" target="_blank" rel="noopener">'
        f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{p}"/></svg></a>'
        for nm, h, p in SOCIAL)
    tools = "".join(f'<span class="c">{tool_icon(x)}{e(x)}</span>' for x in AI_TOOLS)
    creds = "".join(cred_html(x) for x in CREDENTIALS)
    li_chips = "".join(f'<span class="c">{e(x)}</span>' for x in LINKEDIN_CHIPS)
    qchips = "".join(f'<button type="button">{e(x)}</button>' for x in SENSEI_CHIPS)
    # Chapter 6: live iframe if SENSEI_EMBED_URL is set, else the static mock-up
    shead = ('<div class="shead"><div class="avatar">S</div>'
             '<div><div class="nm">Sensei</div><div class="sub">Career &amp; Admission Advisor</div></div>'
             '<span class="on">● ONLINE</span></div>')
    if SENSEI_EMBED_URL:
        src = SENSEI_EMBED_URL + (("&" if "?" in SENSEI_EMBED_URL else "?") + "source=" + e(s["id"]))
        sensei_section = (f'<section class="sensei">{shead}'
            f'<iframe class="sensei-frame" src="{src}" title="Chat with a JAIN advisor" '
            f'loading="lazy" allow="clipboard-write; microphone"></iframe></section>')
    else:
        sensei_section = (f'<section class="sensei">{shead}'
            '<div class="chatbody"><div class="mrow"><div class="mavatar">S</div>'
            '<div class="msg">🙏 Namaste! I\'m Sensei — your admission &amp; career advisor. Ask me anything '
            'about degrees, electives, fees or eligibility. No pressure — just clear, honest guidance.</div></div></div>'
            f'<div class="qrow"><span class="qlabel">TRY:</span>'
            + collapse(f'<div class="qchips col-body">{qchips}</div>', 'more-q').replace('class="collapse"','class="collapse qcol"')
            + '</div>'
            '<div class="inrow"><input id="senseiInput" placeholder="Ask Sensei anything about your career or degree…">'
            '<button class="send" type="button">SEND <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg></button></div>'
            '</section>')
    title = " ".join(x for x in [s['hero'].get('headline_pre',''),s['hero'].get('highlight',''),s['hero'].get('headline_post','')] if x).strip()
    hero_u = img_url(f"{s['id']}-hero.png") or ""
    hero_art = (f'<div class="art" style="background-image:url(\'{hero_u}\')">'
                f'<div class="burst" style="right:16px;bottom:16px">{e(s["hero"]["burst"])}</div></div>')

    return f"""<meta charset="utf-8">
<title>JAIN ONLINE - {e(s['program'])} {e(s['specialization'])} - {e(title)}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(s['hero']['sub'] or (title + ' - JAIN Online ' + s['program'] + ' ' + s['specialization']))}">
<link rel="icon" type="image/png" href="img/favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Bangers&family=Anton&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>

{nav_overlay()}
<header class="bar"><div class="wrap">
  <a class="logo" href="#ch1"><span class="chip"><img src="img/brand-color.png" alt="JAIN Online"></span></a>
  <div style="display:flex;align-items:center">
    <a class="navcta" href="#cta">ENQUIRE NOW</a>
    <label class="hamburger" for="navtoggle" role="button" aria-label="Open menu"><span></span><span></span><span></span></label>
  </div>
</div></header>

<main class="wrap">
  <section class="cpage">
  <!-- CH1 -->
  <div class="chapter" id="ch1"><div class="tag">CHAPTER ONE: {e(s['hero']['eyebrow'])}</div><div class="pg">PAGE 01</div></div>
  <section class="hero"><div class="grid">
    <div class="copy">
      <span class="eyebrow">{e(s['program'])} · {e(s['specialization'])}</span>
      <h1>{e(s['hero']['headline_pre'])} <span class="hl">{e(s['hero']['highlight'])}</span> {e(s['hero']['headline_post'])}</h1>
      {f'<p class="sub">{e(s["hero"]["sub"])}</p>' if s['hero'].get('sub') else ''}
      <div class="btnrow"><a class="btn gold" href="#cta">{e(s['hero']['cta1'])} &rarr;</a>
        <a class="btn ghost" href="#ch3">{e(s['hero']['cta2'])}</a></div>
    </div>{hero_art}
  </div></section>
  <div class="statbar">{stats}</div>
  <a class="askbar" href="#cta">READY TO FIND YOUR PATH? &nbsp; START YOUR APPLICATION &rarr;</a>

  </section>
  <section class="cpage">
  <!-- CH2 -->
  <div class="chapter" id="ch2"><div class="tag">CHAPTER TWO: SETTING THE TARGET</div><div class="pg">PAGE 02</div></div>
  <section class="panels">{panels}</section>
  <section class="lesson"><h3>{e(s['turn']['title'])}</h3><ul>{lesson_li}</ul></section>

  </section>
  <section class="cpage">
  <!-- CH3 -->
  <div class="chapter" id="ch3"><div class="tag">CHAPTER THREE: THE PROGRAM UNIVERSE</div><div class="pg">PAGE 03</div></div>
  <div class="tabs">
    <button class="active" data-f="all">All Electives</button>
    <button data-f="45k">₹45,000 / yr</button>
    <button data-f="50k">₹50,000 / yr</button>
  </div>
  <div class="cardscroll">{program_cards()}</div>

  </section>
  <section class="cpage">
  <!-- CH4 -->
  <div class="chapter" id="ch4"><div class="tag">CHAPTER FOUR: SPECIAL POWER</div><div class="pg">PAGE 04</div></div>
  <section class="power p1"><div class="lab">SPECIAL POWER 1</div>
    <div class="pimg" style="background-image:url('{p1img}')"></div>
    <div class="pbodyc"><h3>Master AI Tools from Semester 1</h3>
      <p>AI isn't an afterthought here — you apply real AI tools from your very first semester, in every subject.</p>
      {collapse(f'<div class="chips col-body">{tools}</div>', 'more-tools')}</div></section>
  <section class="power p2"><div class="lab">SPECIAL POWER 2</div>
    <div class="pimg" style="background-image:url('{p2img}')"></div>
    <div class="pbodyc"><h3>Micro-Credentials Included — No Extra Cost</h3>
      <p>Earn 2 credits per micro-credential alongside your BBA — Google AI Essentials, Power BI, Financial Modelling &amp; more, taught by industry experts.</p>
      <div class="creds"><span class="poweredby">Powered by</span>{creds}</div></div></section>
  <section class="power p3"><div class="lab">SPECIAL POWER 3</div>
    <div class="pimg" style="background-image:url('{p3img}')"></div>
    <div class="pbodyc"><h3>Learn Your Way, Fully Supported</h3>
      <p>Flexible online learning with weekend live classes, a dedicated batch owner, virtual labs and a Sunday Social network — support every step of the way.</p>
      {collapse(f'<div class="chips col-body">{li_chips}</div>', 'more-learn')}</div></section>

  </section>
  <section class="cpage">
  <!-- CH5 -->
  <div class="chapter" id="ch5"><div class="tag">CHAPTER FIVE: CHARACTER EVOLUTION</div><div class="pg">PAGE 05</div></div>
  <section class="evos">{evo_cards}</section>
  <section class="facts"><h3>The Real Numbers</h3><div class="frow">{facts}</div></section>

  </section>
  <section class="cpage">
  <!-- CH6 -->
  <div class="chapter" id="ch6"><div class="tag">CHAPTER SIX: MEET SENSEI</div><div class="pg">PAGE 06</div></div>
  {sensei_section}

  </section>
  <section class="cpage">
  <!-- CH7 -->
  <div class="chapter" id="cta"><div class="tag">CHAPTER SEVEN: FINAL SHOWDOWN</div><div class="pg">PAGE 07</div></div>
  <section class="final">
    <div class="fgrid">
      <div class="fcopy">
        <h2>{e(s['cta']['headline_pre'])} <span class="hl">{e(s['cta']['highlight'])}</span></h2>
        <p>{e(s['cta']['sub'])}</p>
        <div class="btnrow"><a class="btn gold" href="#">{e(s['cta']['button'])} &rarr;</a>
          <a class="btn ghost" href="#ch3">Explore Programs</a></div>
      </div>
      {fart}
    </div>
  </section>
  </section>
</main>
<footer>
  <div class="fcol">
    <div class="fleft">
      <span class="flogo"><img src="img/brand-color.png" alt="JAIN Online"></span>
      <ul class="fbul">
        <li>Accredited by NAAC with an A++ grade.</li>
        <li>UGC-Entitled programs designed for the modern learner.</li>
      </ul>
    </div>
    <div class="fask">
      <span class="qmark">?!</span>
      <h3>STILL HAVE QUESTIONS?</h3>
      <p>Chat with Sensei for instant answers on admissions, fees, eligibility, scholarships and more.</p>
      <a class="btn gold" href="#ch6">TALK TO A COUNSELLOR &rarr;</a>
    </div>
  </div>
  <div class="copywrap"><div class="copyline2">&copy; 2025 JAIN Online. All rights reserved. UGC-DEB Approved.</div></div>
</footer>
<script>{JS}</script>
"""

def sanitize(html):
    """Remove en/em dashes and convert every non-ASCII char to an HTML entity so the
    page renders identically on any device/charset (fixes mobile 'special characters').
    Safe: at this stage the HTML contains only base64/SVG (ASCII) plus text."""
    html = html.replace("—", "-").replace("–", "-")  # em/en dash -> hyphen
    return "".join(ch if ord(ch) < 128 else f"&#{ord(ch)};" for ch in html)

def build_one(path):
    s = json.loads(path.read_text(encoding="utf-8"))
    (PAGES / f"{s['id']}.html").write_text(sanitize(render(s)), encoding="utf-8")
    print(f"built pages/{s['id']}.html  ({len(s['panels'])} panels)")

if __name__ == "__main__":
    targets = sys.argv[1:]
    files = ([STORIES / f"{t}.json" for t in targets] if targets else sorted(STORIES.glob("*.json")))
    for f in files: build_one(f)
    print(f"\nDone. {len(files)} page(s) in {PAGES}")
