#!/usr/bin/env python3
"""Generate the 4 JAIN brand / university-level story JSONs (from the 11.9M-impression generic
'JAIN University' search bucket): jain-online (hub), jain-fees, jain-reviews, jain-admission.
program='JAIN' -> brand theme (Ch3 shows all 7 programs). Brand-safe, no em dashes."""
import json, pathlib
STORIES = pathlib.Path(__file__).parent / "stories"; STORIES.mkdir(exist_ok=True)
BTN = "Talk to a counsellor"
def cta(pre, hl, button=BTN, sub="", burst="GO!"):
    return {"headline_pre": pre, "highlight": hl, "sub": sub, "button": button, "burst": burst}
REC = "NAAC A++ accredited, UGC-entitled online degrees"

STORIES_DATA = [
 {
  "id":"jain-online","intent":"Brand / all programs","program":"JAIN","specialization":"Online University",
  "target_query":"jain university online courses",
  "hero":{"eyebrow":"ONE UNIVERSITY, MANY PATHS","headline_pre":"JAIN ONLINE,","highlight":"YOUR DEGREE AWAITS.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore programmes",
    "art_prompt":"Aditya, a 22 year old Indian student in smart-casual, confident and hopeful, exploring online degree options on a laptop at home, aspirational bright mood.","burst":"EXPLORE!"},
  "statbar":[{"big":"7 PROGRAMMES","label":"UG & PG"},{"big":"100% ONLINE","label":"study anywhere"},
    {"big":"NAAC A++","label":"accredited"},{"big":"UGC","label":"entitled"}],
  "panels":[
    {"n":1,"narration":"Aditya wanted a recognised degree that fit his life.","dialogue":"Which university do I trust?",
     "img_prompt":"Aditya, 22, at a laptop exploring university options, curious and hopeful, tidy home."},
    {"n":2,"narration":"Countless options made the choice confusing.","dialogue":"So many claims, who is real?",
     "img_prompt":"Aditya looking a little overwhelmed by many browser options on a laptop, rubbing his head, modest room."},
    {"n":3,"narration":"Then he found JAIN Online, recognised and complete.","dialogue":"One trusted university!",
     "img_prompt":"Aditya's face lighting up with clarity at a laptop showing a clean JAIN Online programmes page, warm bright home."},
    {"n":4,"narration":"He picked his programme and began with guidance.","dialogue":"My degree journey begins!",
     "img_prompt":"Aditya confidently starting his first online lesson on a laptop, notebook ready, focused and happy, warm light."}],
  "turn":{"title":"Why Choose JAIN Online","points":[
    "Seven UGC-entitled programmes: MBA, BBA, MCA, BCA, B.Com, M.Com and MA.",
    "Study 100% online with weekend live classes, from anywhere, around your life.",
    "NAAC A++ accredited degrees, recognised for jobs, promotions and higher study.",
    "Affordable fees with 0% interest EMI, plus real AI tools and mentor support."]},
  "proof":{"testimonials":[
    {"name":"Aditya Rao","spec":"JAIN ONLINE","role":"Student","metric":"7 PATHS","stat":"one trusted uni",
     "quote":"I wanted one university I could trust. JAIN gave me a recognised degree that fit my life."},
    {"name":"Kavya Menon","spec":"JAIN ONLINE","role":"Working Professional","metric":"NAAC A++","stat":"recognised",
     "quote":"A NAAC A++, UGC-entitled degree earned online. It was accepted without a second thought."},
    {"name":"Rohit Shah","spec":"JAIN ONLINE","role":"Career Switcher","metric":"0% EMI","stat":"affordable",
     "quote":"Affordable fees and 0% EMI meant I could finally start, without a heavy burden."},
    {"name":"Sara Thomas","spec":"JAIN ONLINE","role":"Graduated","metric":"PLACED","stat":"supported",
     "quote":"Real support and a recognised degree opened the next door in my career."}],
    "facts":[{"k":"Programmes","v":"MBA, BBA, MCA, BCA, B.Com, M.Com, MA"},
      {"k":"Mode","v":"100% online, weekend live classes"},
      {"k":"Recognition","v":REC},{"k":"Support","v":"0% EMI, AI tools, mentor guidance"}]},
  "cta":cta("READY TO FIND","YOUR PROGRAMME?"),
 },
 {
  "id":"jain-fees","intent":"Brand / fees","program":"JAIN","specialization":"Fees",
  "target_query":"jain university fees",
  "hero":{"eyebrow":"JAIN ONLINE FEES","headline_pre":"JAIN FEES,","highlight":"CLEAR & AFFORDABLE.",
    "headline_post":"","sub":"","cta1":"Get my fee + plan","cta2":"Explore programmes",
    "art_prompt":"Sneha, a 21 year old Indian student in smart-casual, reassured and hopeful, reviewing a clear affordable fee breakdown on a laptop at home, bright mood.","burst":"CLEAR!"},
  "statbar":[{"big":"FROM Rs 22,500","label":"per year"},{"big":"0% EMI","label":"pay monthly"},
    {"big":"DISCOUNT","label":"pay upfront"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Sneha searched for the real cost of a JAIN degree.","dialogue":"What will it actually cost?",
     "img_prompt":"Sneha, 21, at a laptop searching for clear fee information, curious and focused, tidy home."},
    {"n":2,"narration":"Other sites showed vague numbers and hidden extras.","dialogue":"Just show me the full fee.",
     "img_prompt":"Sneha looking a little frustrated at a laptop showing unclear, incomplete fee information, modest room."},
    {"n":3,"narration":"Then she found JAIN's fees, clear and affordable.","dialogue":"Transparent, and doable!",
     "img_prompt":"Sneha's face relaxing with relief at a laptop showing a clean, clear fee breakdown, warm reassured glow."},
    {"n":4,"narration":"She enrolled with total clarity on the cost.","dialogue":"No surprises, just growth!",
     "img_prompt":"Sneha smiling confidently at her laptop after enrolling, calm and assured, warm hopeful light."}],
  "turn":{"title":"JAIN Online Fees, Made Clear","points":[
    "Affordable across the board: UG from about Rs 45,000/year, MA from just Rs 22,500/year.",
    "Pay upfront for a discount, or choose 0% interest EMI to spread the cost.",
    "Only Rs 2,500 one-time registration. Clear fees, no hidden charges.",
    "Every programme is NAAC A++ accredited and UGC-entitled."]},
  "proof":{"testimonials":[
    {"name":"Sneha Pillai","spec":"JAIN FEES","role":"Student","metric":"CLEAR","stat":"no surprises",
     "quote":"I just wanted the real number. JAIN showed the full fee clearly, with no hidden extras."},
    {"name":"Karan Mehta","spec":"JAIN ONLINE","role":"1st-Year Student","metric":"0% EMI","stat":"monthly",
     "quote":"The monthly EMI made a recognised degree easy to plan. I knew my exact cost from day one."},
    {"name":"Ritu Sharma","spec":"JAIN ONLINE","role":"Career Switcher","metric":"AFFORDABLE","stat":"UG & PG",
     "quote":"Whether UG or PG, the fees were genuinely affordable and clearly explained."},
    {"name":"Manoj K","spec":"JAIN ONLINE","role":"Graduated","metric":"NO HIDDEN","stat":"as promised",
     "quote":"No hidden charges appeared, ever. The fee I saw at the start was exactly what I paid."}],
    "facts":[{"k":"UG fees","v":"From about Rs 45,000/year (BBA, B.Com, BCA)"},
      {"k":"PG fees","v":"MA from Rs 22,500/year; MBA, MCA, M.Com affordable too"},
      {"k":"Payment","v":"0% interest EMI or an upfront discount"},
      {"k":"Extras","v":"Rs 2,500 one-time registration. No hidden charges."}]},
  "cta":cta("READY TO SEE","YOUR EXACT FEE?",button="Get my fee + plan"),
 },
 {
  "id":"jain-reviews","intent":"Brand / trust & recognition","program":"JAIN","specialization":"Reviews & Recognition",
  "target_query":"jain university reviews",
  "hero":{"eyebrow":"TRUSTED & RECOGNISED","headline_pre":"JAIN ONLINE,","highlight":"REAL & RECOGNISED.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore programmes",
    "art_prompt":"Rahul, a 23 year old Indian student in smart-casual, reassured and confident, reading positive information on a laptop at home, trusting hopeful mood.","burst":"TRUSTED!"},
  "statbar":[{"big":"NAAC A++","label":"top grade"},{"big":"UGC","label":"entitled"},
    {"big":"PLACEMENT","label":"support"},{"big":"THOUSANDS","label":"of learners"}],
  "panels":[
    {"n":1,"narration":"Rahul wanted proof that an online degree was respected.","dialogue":"Is it truly recognised?",
     "img_prompt":"Rahul, 23, at a laptop carefully researching, a little sceptical but hopeful, tidy home."},
    {"n":2,"narration":"He worried an online degree might not be valued.","dialogue":"Will employers accept it?",
     "img_prompt":"Rahul looking thoughtful and cautious at a laptop, weighing his options, modest room."},
    {"n":3,"narration":"Then he saw JAIN's NAAC A++ grade and UGC entitlement.","dialogue":"Real recognition, proven!",
     "img_prompt":"Rahul's face relaxing into a confident smile at a laptop showing strong accreditation and positive reviews, warm reassured glow."},
    {"n":4,"narration":"He enrolled, confident in a respected degree.","dialogue":"A degree that counts!",
     "img_prompt":"Rahul confidently starting his studies on a laptop, calm and assured, warm hopeful light."}],
  "turn":{"title":"Why JAIN Online Is Trusted","points":[
    "Accredited by NAAC with a top A++ grade, a mark of real quality.",
    "UGC-entitled online degrees, the same value as on-campus, recognised for jobs and higher study.",
    "Dedicated placement support, industry projects and mentor guidance.",
    "Trusted by thousands of learners across India and beyond."]},
  "proof":{"testimonials":[
    {"name":"Rahul Nair","spec":"JAIN ONLINE","role":"Student","metric":"RECOGNISED","stat":"NAAC A++",
     "quote":"I needed proof it was respected. NAAC A++ and UGC entitlement settled it for me."},
    {"name":"Kavya Menon","spec":"JAIN ONLINE","role":"Working Professional","metric":"ACCEPTED","stat":"by employer",
     "quote":"My employer accepted my JAIN degree without hesitation. That recognition mattered."},
    {"name":"Arun Nair","spec":"JAIN ONLINE","role":"Career Switcher","metric":"PLACEMENT","stat":"supported",
     "quote":"The placement support and real projects made my degree count in interviews."},
    {"name":"Sara Thomas","spec":"JAIN ONLINE","role":"Graduated","metric":"TRUSTED","stat":"thousands",
     "quote":"Joining a university thousands already trusted gave me real confidence."}],
    "facts":[{"k":"Accreditation","v":"NAAC A++ (top grade)"},
      {"k":"Recognition","v":"UGC-entitled online degrees, same value as on-campus"},
      {"k":"Careers","v":"Placement support, industry projects, mentor guidance"},
      {"k":"Community","v":"Trusted by thousands of learners"}]},
  "cta":cta("READY TO JOIN A","TRUSTED UNIVERSITY?"),
 },
 {
  "id":"jain-admission","intent":"Brand / admission","program":"JAIN","specialization":"Admissions 2026",
  "target_query":"jain university admission",
  "hero":{"eyebrow":"ADMISSIONS OPEN 2026","headline_pre":"JAIN ADMISSION,","highlight":"MADE SIMPLE.",
    "headline_post":"","sub":"","cta1":"Start my application","cta2":"Check eligibility",
    "art_prompt":"Priya, a 20 year old Indian student in smart-casual, confident and relieved, starting an online university application on a laptop at home, bright hopeful mood.","burst":"APPLY!"},
  "statbar":[{"big":"100% ONLINE","label":"apply from home"},{"big":"NO ENTRANCE","label":"merit based"},
    {"big":"7 PROGRAMMES","label":"UG & PG"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Priya wanted to join JAIN but felt unsure how.","dialogue":"Where do I even start?",
     "img_prompt":"Priya, 20, with a laptop looking unsure at an admissions page, hopeful but puzzled, tidy home."},
    {"n":2,"narration":"The steps and documents felt scattered.","dialogue":"Am I even eligible?",
     "img_prompt":"Priya with a few documents and notes, trying to make sense of admission steps, focused and determined."},
    {"n":3,"narration":"Then she found one simple online admission process.","dialogue":"Just a few clear steps!",
     "img_prompt":"Priya smiling with relief at a laptop showing a clean, simple step-by-step admission process, warm bright home."},
    {"n":4,"narration":"She applied in minutes, guided at every step.","dialogue":"My application is in!",
     "img_prompt":"Priya happily submitting her application on a laptop, a small confident thumbs up, proud and relieved, warm light."}],
  "turn":{"title":"How JAIN Admission Works","points":[
    "Simple eligibility: class 12 for UG programmes, a bachelor's degree for PG.",
    "The whole application is online, so you can apply from home in minutes.",
    "No entrance exam. Admission is merit based, and working professionals are welcome.",
    "Upload your documents, pay the registration fee, and a counsellor guides you through."]},
  "proof":{"testimonials":[
    {"name":"Priya Joshi","spec":"JAIN ONLINE","role":"1st-Year Student","metric":"APPLIED","stat":"in minutes",
     "quote":"I thought admission would be stressful. The online steps were clear and a counsellor guided me."},
    {"name":"Rohan Gupta","spec":"JAIN ONLINE","role":"Student","metric":"ANY STREAM","stat":"merit based",
     "quote":"No entrance exam. I applied on merit and joined the programme I wanted."},
    {"name":"Aisha Khan","spec":"JAIN ONLINE","role":"Working Professional","metric":"FROM HOME","stat":"fully online",
     "quote":"I applied from my phone at home. It took only a few minutes."},
    {"name":"Nikhil Rao","spec":"JAIN ONLINE","role":"2nd-Year Student","metric":"GUIDED","stat":"step by step",
     "quote":"Every time I had a doubt, my counsellor answered. Admission felt easy."}],
    "facts":[{"k":"Eligibility","v":"Class 12 for UG, a bachelor's degree for PG"},
      {"k":"Process","v":"100% online application, apply from home"},
      {"k":"Selection","v":"Merit based, no entrance exam"},
      {"k":"Support","v":"Dedicated counsellor guides every step"}]},
  "cta":cta("READY TO APPLY","TO JAIN ONLINE?",button="Start my application"),
 },
]

for s in STORIES_DATA:
    out = json.dumps(s, ensure_ascii=False, indent=2).replace("Rs ", "₹")
    (STORIES / f"{s['id']}.json").write_text(out, encoding="utf-8")
    print("wrote", s["id"], "->", s["target_query"])
print(f"\n{len(STORIES_DATA)} JAIN brand stories written")
