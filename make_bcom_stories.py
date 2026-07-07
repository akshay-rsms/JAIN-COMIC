#!/usr/bin/env python3
"""Generate the 5 B.Com story JSONs (3 intent + 2 specialisation) for JAIN Online.
Persona = commerce-minded students ~18-20 (fresh 12th) or early workers wanting a recognised
commerce degree. Fees verified live from PMS 2026-07-07: standard B.Com Rs 1,35,000 total
(Rs 45,000/yr) for the 3-yr program (ACCA-integrated track priced the same), reg Rs 2,500,
0% EMI ~Rs 3,750/mo. Brand-safe, correct English, complete 4-panel arc, no em dashes."""
import json, pathlib
STORIES = pathlib.Path(__file__).parent / "stories"; STORIES.mkdir(exist_ok=True)

BTN = "Get my B.Com plan"
def cta(pre, hl, sub="", button=BTN, burst="GO!"):
    return {"headline_pre": pre, "highlight": hl, "sub": sub, "button": button, "burst": burst}

FEE_LINE = "Rs 1,35,000 for the full 3-year B.Com (Rs 45,000/year)"
EMI_LINE = "0% interest EMI from about Rs 3,750/month, or an education loan"
REC_LINE = "UGC-entitled online B.Com, NAAC A++ accredited"
STATBAR = [{"big":"Rs 45,000","label":"per year"},{"big":"0% EMI","label":"pay monthly"},
           {"big":"100% ONLINE","label":"study anywhere"},{"big":"NAAC A++","label":"accredited"}]

STORIES_DATA = [
 {
  "id":"bcom-course","intent":"Generic / course overview","program":"B.Com",
  "specialization":"Online","target_query":"bcom course",
  "hero":{"eyebrow":"START YOUR COMMERCE JOURNEY","headline_pre":"YOUR B.COM,","highlight":"ONE CLEAR PATH.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore specialisations",
    "art_prompt":"Aarav, an 18 year old Indian commerce student in a simple casual collared shirt, confident and hopeful, choosing a commerce path on a laptop at home, bright aspirational mood.","burst":"LET'S GO!"},
  "statbar":[{"big":"SPECIALISATIONS","label":"choose your path"},{"big":"100% ONLINE","label":"study anywhere"},
    {"big":"Rs 45,000","label":"per year"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Aarav finished 12th and knew he liked commerce.","dialogue":"A B.Com, but which one?",
     "img_prompt":"Aarav, 18, thoughtful at a laptop imagining commerce career paths, curious, modern tidy home."},
    {"n":2,"narration":"Too many colleges and unclear options felt confusing.","dialogue":"This is overwhelming.",
     "img_prompt":"Aarav looking overwhelmed by many open browser options and brochures, rubbing his head, modest room."},
    {"n":3,"narration":"Then he found a clear, affordable online B.Com.","dialogue":"One simple path, finally!",
     "img_prompt":"Aarav smiling with clarity at a laptop showing a clean B.Com page with specialisations, warm bright home."},
    {"n":4,"narration":"He picked a specialisation and started with guidance.","dialogue":"My commerce journey begins!",
     "img_prompt":"Aarav confidently starting his first B.Com lesson on a laptop, notebook ready, focused and happy, warm light."}],
  "turn":{"title":"Why Start Your B.Com Here","points":[
    "Choose from career specialisations: Accounting & Finance, ACCA, Corporate Accounting and more.",
    "Study 100% online, anytime, from anywhere. No campus, no commute.",
    f"Just {FEE_LINE}, with 0% interest EMI or a discount on upfront payment.",
    "Real finance tools, included micro-credentials and mentor support from semester 1."]},
  "proof":{"testimonials":[
    {"name":"Aarav Nair","spec":"B.COM A&F","role":"1st-Year Student","metric":"CLEAR PATH","stat":"guided",
     "quote":"I knew I liked commerce but not the details. The clear specialisations made my choice easy."},
    {"name":"Tanvi Shah","spec":"B.COM ONLINE","role":"2nd-Year Student","metric":"MY PICK","stat":"my path",
     "quote":"Picking my specialisation meant the degree matched the finance career I actually wanted."},
    {"name":"Aditya Kumar","spec":"B.COM ACCA","role":"Final Year","metric":"GLOBAL","stat":"ACCA edge",
     "quote":"The ACCA-integrated option gave my B.Com a global edge without extra cost."},
    {"name":"Pooja Reddy","spec":"B.COM A&F","role":"Graduated","metric":"PLACED","stat":"recognised",
     "quote":"A recognised B.Com, learned online at my pace. It opened my first finance role."}],
    "facts":[{"k":"Choose","v":"Accounting & Finance, ACCA, Corporate Accounting and more"},
      {"k":"Mode","v":"100% online, learn anytime with weekend live classes"},
      {"k":"Fee","v":FEE_LINE},{"k":"Recognition","v":REC_LINE}]},
  "cta":cta("READY TO BEGIN","YOUR B.COM?"),
 },
 {
  "id":"bcom-online","intent":"Online / from home","program":"B.Com",
  "specialization":"Online","target_query":"online bcom course",
  "hero":{"eyebrow":"A REAL B.COM, FROM HOME","headline_pre":"A REAL B.COM,","highlight":"100% ONLINE.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore specialisations",
    "art_prompt":"Diya, a 19 year old Indian girl in a modest kurti, smiling as she studies commerce on a laptop at a tidy desk at home, bright hopeful daytime, warm and aspirational.","burst":"FROM HOME!"},
  "statbar":[{"big":"100% ONLINE","label":"study anywhere"},{"big":"NO RELOCATION","label":"stay at home"},
    {"big":"0% EMI","label":"pay monthly"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Diya's town had no college with a strong B.Com.","dialogue":"Do I have to move away?",
     "img_prompt":"Diya, 19, in a modest kurti at her window looking toward a faraway city, a brochure in hand, thoughtful hopeful, small-town home."},
    {"n":2,"narration":"Leaving home for a distant campus felt daunting.","dialogue":"So far from my family?",
     "img_prompt":"Diya looking torn while glancing between a packed bag and a family photo on the wall, warm modest room."},
    {"n":3,"narration":"Then she found a recognised B.Com she could do online.","dialogue":"College, from my own room!",
     "img_prompt":"Diya's face lighting up with relief at a laptop showing an online B.Com, warm glow, tidy home study corner."},
    {"n":4,"narration":"Now she studies at home, her degree on track.","dialogue":"No move, a full degree.",
     "img_prompt":"Diya happily attending an online class on her laptop at home, notebook beside her, proud family in the background, warm encouraging light."}],
  "turn":{"title":"Why An Online B.Com Just Works","points":[
    "Study 100% online, anytime, from your phone or laptop. No campus, no commute.",
    "The same UGC-entitled, NAAC A++ B.Com as on-campus, recognised everywhere.",
    f"Just {FEE_LINE}, with 0% interest EMI or a discount on upfront payment.",
    "Weekend live classes plus recordings, so learning fits around your life."]},
  "proof":{"testimonials":[
    {"name":"Diya Menon","spec":"B.COM ONLINE","role":"1st-Year Student","metric":"FROM HOME","stat":"no hostel",
     "quote":"There was no good college in my town. Studying online let me earn a real B.Com without leaving home."},
    {"name":"Sana Iqbal","spec":"B.COM A&F","role":"2nd-Year Student","metric":"0% EMI","stat":"Rs 3,750 / mo",
     "quote":"The monthly EMI fit my budget, and weekend classes fit my schedule. It just worked."},
    {"name":"Divya Rao","spec":"B.COM ACCA","role":"Final Year","metric":"RECOGNISED","stat":"UGC-entitled",
     "quote":"A recognised degree earned from home. My internship team accepted it without a second thought."},
    {"name":"Meena S","spec":"B.COM ONLINE","role":"Graduated","metric":"ON TIME","stat":"on my terms",
     "quote":"I studied around family responsibilities and still graduated on time. That flexibility changed everything."}],
    "facts":[{"k":"Mode","v":"100% online from home, weekend live classes"},
      {"k":"No relocation","v":"Same recognised B.Com, no hostel or commute"},
      {"k":"Fee","v":FEE_LINE},{"k":"Recognition","v":REC_LINE}]},
  "cta":cta("READY TO STUDY","FROM HOME?"),
 },
 {
  "id":"bcom-course-fees","intent":"Fees / affordability","program":"B.Com",
  "specialization":"Accounting and Finance","target_query":"bcom course fees",
  "hero":{"eyebrow":"THE FEE COMPARISON","headline_pre":"A RECOGNISED B.COM,","highlight":"JUST Rs 45,000/YR.",
    "headline_post":"","sub":"","cta1":"Get my fee + plan","cta2":"Explore specialisations",
    "art_prompt":"Rohan, an 18 year old Indian commerce student, happily surprised at a laptop showing an affordable B.Com fee after comparing colleges, bright hopeful mood, tidy home.","burst":"Rs 45K!"},
  "statbar":[{"big":"Rs 45,000","label":"per year"},{"big":"0% EMI","label":"pay monthly"},
    {"big":"DISCOUNT","label":"pay upfront"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Rohan compared B.Com fees, college after college.","dialogue":"Why is a degree so costly?",
     "img_prompt":"Rohan, 18, at a desk comparing several high college-fee figures in a notebook, concerned, papers around him, modest home."},
    {"n":2,"narration":"Most good options ran into several lakhs.","dialogue":"Is a real degree only for the rich?",
     "img_prompt":"Rohan looking discouraged at a laptop showing an expensive fee, chin in hand, soft disappointed expression, modest room."},
    {"n":3,"narration":"Then he found a recognised B.Com at Rs 45,000 a year.","dialogue":"Affordable and recognised?",
     "img_prompt":"Rohan's eyes widening with hope at a laptop showing a clear, affordable, recognised B.Com fee, warm glow of relief."},
    {"n":4,"narration":"He enrolled on a 0% EMI he could manage.","dialogue":"A real degree, no debt!",
     "img_prompt":"Rohan smiling proudly holding a blank enrollment confirmation at home, calm and confident, warm hopeful light. No cash or money shown."}],
  "turn":{"title":"Why This B.Com Fee Is A Steal","points":[
    f"Just {FEE_LINE}. A recognised commerce degree at a fair, honest price.",
    "Pay the full year upfront and get a discount, or split it into easy 0% interest EMI.",
    "0% interest EMI from about Rs 3,750/month, no extra cost.",
    "Only Rs 2,500 one-time registration. Clear fees, no hidden charges."]},
  "proof":{"testimonials":[
    {"name":"Rohan Pillai","spec":"B.COM A&F","role":"1st-Year Student","metric":"Rs 45K / yr","stat":"recognised",
     "quote":"I compared everywhere. A UGC-entitled B.Com at Rs 45,000 a year was the clear, honest choice."},
    {"name":"Arjun Das","spec":"B.COM · SEM 1","role":"1st-Year Student","metric":"0% EMI","stat":"Rs 3,750 / mo",
     "quote":"The 0% EMI meant no lump sum. I pay a small amount each month and my degree keeps going."},
    {"name":"Nisha Verma","spec":"B.COM ACCA","role":"Final Year","metric":"DISCOUNT","stat":"paid upfront",
     "quote":"We paid the year upfront and got a clear discount. A recognised degree at this price felt unreal."},
    {"name":"Vikram Rao","spec":"B.COM A&F","role":"Graduated","metric":"DEBT-FREE","stat":"Rs 0 loan",
     "quote":"I finished my B.Com without a single education loan. The monthly plan fit my budget perfectly."}],
    "facts":[{"k":"Fee","v":FEE_LINE},{"k":"Upfront","v":"Discount on one-time full payment"},
      {"k":"EMI","v":EMI_LINE},{"k":"Extras","v":"Rs 2,500 one-time registration. No hidden charges."}]},
  "cta":cta("READY TO START","FOR Rs 45K A YEAR?",button="Get my fee + plan"),
 },
 {
  "id":"bcom-accounting-finance","intent":"Specialisation / Accounting & Finance","program":"B.Com",
  "specialization":"Accounting and Finance","target_query":"bcom in accounting and finance",
  "hero":{"eyebrow":"FOR FUTURE FINANCE PROS","headline_pre":"A B.COM IN","highlight":"ACCOUNTING & FINANCE.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore specialisations",
    "art_prompt":"Sneha, an 18 year old Indian commerce student, confident and happy studying accounts and finance on a laptop, modern home, aspirational mood.","burst":"BALANCE!"},
  "statbar":STATBAR,
  "panels":[
    {"n":1,"narration":"Sneha loved balancing accounts and tracking money.","dialogue":"Numbers just make sense to me.",
     "img_prompt":"Sneha, 18, happily working on accounts in a ledger and laptop at home, curious and engaged, tidy room."},
    {"n":2,"narration":"But a finance career needed a real degree.","dialogue":"How do I turn this into a job?",
     "img_prompt":"Sneha looking thoughtful, wondering how to build a finance career, a laptop open in front of her, modest room."},
    {"n":3,"narration":"Then she found a B.Com in Accounting & Finance, online.","dialogue":"My finance career starts here!",
     "img_prompt":"Sneha's face lighting up with excitement at a laptop showing a B.Com in Accounting and Finance, warm hopeful glow."},
    {"n":4,"narration":"She enrolled and began mastering the craft.","dialogue":"From curious to qualified!",
     "img_prompt":"Sneha confidently starting her first accounting lesson on a laptop, notebook and calculator beside her, focused and happy, warm light."}],
  "turn":{"title":"Why A B.Com In Accounting & Finance","points":[
    "Master the real craft: accounting, taxation, auditing and financial management.",
    "Apply real finance tools and included micro-credentials from your very first semester.",
    f"{FEE_LINE}, with 0% interest EMI or a discount on upfront payment.",
    "A UGC-entitled, NAAC A++ B.Com that employers and CA/CMA paths recognise."]},
  "proof":{"testimonials":[
    {"name":"Sneha Iyer","spec":"B.COM A&F","role":"1st-Year Student","metric":"MY SKILL","stat":"now a career",
     "quote":"I always loved accounts. This degree turned that into a real finance career path."},
    {"name":"Kavya Menon","spec":"B.COM A&F","role":"2nd-Year Student","metric":"TOOLS","stat":"from sem 1",
     "quote":"Learning real finance tools from semester one made me genuinely job-ready."},
    {"name":"Aman Gupta","spec":"B.COM A&F","role":"Final Year","metric":"0% EMI","stat":"Rs 3,750 / mo",
     "quote":"The 0% EMI let me start right after 12th instead of waiting years to save up."},
    {"name":"Sara Thomas","spec":"B.COM A&F","role":"Graduated","metric":"PLACED","stat":"recognised",
     "quote":"A recognised B.Com plus real accounting skills got me hired into a finance role quickly."}],
    "facts":[{"k":"Learn","v":"Accounting, taxation, auditing, financial management"},
      {"k":"Fee","v":FEE_LINE},{"k":"EMI","v":EMI_LINE},{"k":"Recognition","v":REC_LINE}]},
  "cta":cta("READY FOR A","FINANCE CAREER?"),
 },
 {
  "id":"bcom-international-finance","intent":"Specialisation / International Finance (ACCA)","program":"B.Com",
  "specialization":"International Finance & Accounting","target_query":"bcom acca",
  "hero":{"eyebrow":"GLOBALLY ACCREDITED B.COM","headline_pre":"A B.COM WITH","highlight":"ACCA, UK.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore specialisations",
    "art_prompt":"Karan, a 19 year old Indian commerce student in smart-casual, confident, studying global finance on a laptop with a subtle international feel, modern home, aspirational.","burst":"GLOBAL!"},
  "statbar":[{"big":"ACCA, UK","label":"global accreditation"},{"big":"Rs 45,000","label":"per year"},
    {"big":"100% ONLINE","label":"study anywhere"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Karan wanted a finance career without borders.","dialogue":"I want to work globally.",
     "img_prompt":"Karan, 19, confidently studying global finance on a laptop at home, curious and ambitious, modern room."},
    {"n":2,"narration":"But a plain degree felt too local for his dream.","dialogue":"How do I go global?",
     "img_prompt":"Karan looking thoughtful, wondering how to build an international finance career, a laptop open, modest room."},
    {"n":3,"narration":"Then he found a B.Com integrated with ACCA, UK.","dialogue":"Global, and affordable!",
     "img_prompt":"Karan's face lighting up with excitement at a laptop showing a B.Com accredited by ACCA UK, warm hopeful glow."},
    {"n":4,"narration":"He enrolled and began building a global edge.","dialogue":"From local to global!",
     "img_prompt":"Karan confidently starting his first international finance lesson on a laptop, notebook ready, focused and happy, warm light."}],
  "turn":{"title":"Why A B.Com With ACCA, UK","points":[
    "Master global finance, IFRS and international accounting on an ACCA-aligned syllabus.",
    "Earn a globally recognised edge, accredited by ACCA, UK, alongside your degree.",
    f"All at the same affordable fee: {FEE_LINE}, with 0% interest EMI.",
    "A UGC-entitled, NAAC A++ B.Com, with the added global weight of ACCA."]},
  "proof":{"testimonials":[
    {"name":"Karan Rao","spec":"B.COM ACCA","role":"1st-Year Student","metric":"GLOBAL","stat":"ACCA edge",
     "quote":"I wanted a borderless finance career. An ACCA-integrated B.Com made that possible from day one."},
    {"name":"Kavya Menon","spec":"B.COM ACCA","role":"2nd-Year Student","metric":"IFRS","stat":"job-ready",
     "quote":"The ACCA-aligned syllabus and IFRS made me ready for global finance roles."},
    {"name":"Aman Gupta","spec":"B.COM ACCA","role":"Final Year","metric":"SAME FEE","stat":"no premium",
     "quote":"A globally accredited degree at the same affordable fee. That felt like a genuine head start."},
    {"name":"Sara Thomas","spec":"B.COM ACCA","role":"Graduated","metric":"PLACED","stat":"global-ready",
     "quote":"A globally recognised B.Com got me noticed for international finance roles."}],
    "facts":[{"k":"Learn","v":"Global finance, IFRS, ACCA-aligned syllabus, international accounting"},
      {"k":"Accreditation","v":"Accredited by ACCA, UK, recognised globally"},
      {"k":"Fee","v":FEE_LINE + ", same as the standard B.Com"},{"k":"Recognition","v":REC_LINE}]},
  "cta":cta("READY TO GO","GLOBAL?"),
 },
]

for s in STORIES_DATA:
    out = json.dumps(s, ensure_ascii=False, indent=2).replace("Rs ", "₹")
    (STORIES / f"{s['id']}.json").write_text(out, encoding="utf-8")
    print("wrote", s["id"], "->", s["target_query"])
print(f"\n{len(STORIES_DATA)} B.Com stories written")
