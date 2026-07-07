#!/usr/bin/env python3
"""Generate the 5 MCA story JSONs (3 intent + 2 specialisation) for JAIN Online.
Persona = graduates (BCA/B.Sc/B.Com/any) or working IT professionals, ~22-27, who want a
real tech career or to upskill. Fees verified live from PMS 2026-07-07: standard MCA
Rs 1,60,000 total (Rs 40,000/sem) for the 2-yr program, reg Rs 2,500, 0% EMI ~Rs 6,667/mo.
Brand-safe, correct English, complete 4-panel arc, no em dashes."""
import json, pathlib
STORIES = pathlib.Path(__file__).parent / "stories"; STORIES.mkdir(exist_ok=True)

BTN = "Get my MCA plan"
def cta(pre, hl, sub="", button=BTN, burst="GO!"):
    return {"headline_pre": pre, "highlight": hl, "sub": sub, "button": button, "burst": burst}

FEE_LINE = "Rs 1,60,000 for the full 2-year MCA (Rs 40,000/semester)"
EMI_LINE = "0% interest EMI from about Rs 6,667/month, or an education loan"
REC_LINE = "UGC-entitled online MCA, NAAC A++ accredited"
STATBAR = [{"big":"Rs 40,000","label":"per semester"},{"big":"0% EMI","label":"pay monthly"},
           {"big":"100% ONLINE","label":"work & study"},{"big":"NAAC A++","label":"accredited"}]

STORIES_DATA = [
 {
  "id":"mca-course","intent":"Generic / course overview","program":"MCA",
  "specialization":"Online","target_query":"mca course",
  "hero":{"eyebrow":"BUILD A REAL TECH CAREER","headline_pre":"YOUR MCA,","highlight":"ONE CLEAR PATH.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore specialisations",
    "art_prompt":"Rahul, a 23 year old Indian graduate man in a casual collared shirt, confident and hopeful, choosing a tech career path on a laptop in a modern home, aspirational mood.","burst":"LET'S GO!"},
  "statbar":[{"big":"5 SPECIALISATIONS","label":"choose your path"},{"big":"100% ONLINE","label":"work & study"},
    {"big":"Rs 40,000","label":"per semester"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Rahul had a degree, but wanted a serious tech career.","dialogue":"I want to build real software.",
     "img_prompt":"Rahul, 23, at a laptop coding simple shapes, curious and driven, modern tidy home."},
    {"n":2,"narration":"Too many courses and unclear paths left him unsure.","dialogue":"Which one actually helps?",
     "img_prompt":"Rahul looking a little overwhelmed by many open browser options on a laptop, rubbing his head, modest room."},
    {"n":3,"narration":"Then he found a clear, recognised online MCA.","dialogue":"One solid path, finally!",
     "img_prompt":"Rahul smiling with clarity at a laptop showing a clean MCA page with specialisations, warm bright home."},
    {"n":4,"narration":"He picked a specialisation and started with guidance.","dialogue":"My tech career begins!",
     "img_prompt":"Rahul confidently starting his first MCA lesson on a laptop, notebook ready, focused and happy, warm light."}],
  "turn":{"title":"Why Start Your MCA Here","points":[
    "Choose from in-demand tech specialisations: Data Science, AI, Cloud, Cyber Security, Full Stack.",
    "Study 100% online with weekend live classes, so you can learn while you work.",
    f"Just {FEE_LINE}, with 0% interest EMI or a discount on upfront payment.",
    "Real, hands-on tech tools and mentor support from your very first semester."]},
  "proof":{"testimonials":[
    {"name":"Rahul Nair","spec":"MCA DATA SCIENCE","role":"Recent Graduate","metric":"CLEAR PATH","stat":"guided",
     "quote":"I had a degree but no direction. The clear specialisations and guidance made my tech path obvious."},
    {"name":"Tanvi Shah","spec":"MCA ONLINE","role":"1st-Year Student","metric":"5 PATHS","stat":"my pick",
     "quote":"Picking my specialisation meant the degree matched the exact tech job I wanted."},
    {"name":"Aditya Kumar","spec":"MCA CLOUD","role":"Working Professional","metric":"HANDS-ON","stat":"from sem 1",
     "quote":"Real, hands-on projects from semester one made me genuinely job-ready, not just certified."},
    {"name":"Pooja Reddy","spec":"MCA CYBER SECURITY","role":"Graduated","metric":"PLACED","stat":"recognised",
     "quote":"A recognised MCA, learned online at my pace. It opened the first real door in tech."}],
    "facts":[{"k":"Choose","v":"Data Science, AI, Cloud, Cyber Security, Full Stack"},
      {"k":"Mode","v":"100% online, weekend live classes, learn while you work"},
      {"k":"Fee","v":FEE_LINE},{"k":"Recognition","v":REC_LINE}]},
  "cta":cta("READY TO BEGIN","YOUR MCA?"),
 },
 {
  "id":"mca-online","intent":"Online / flexible","program":"MCA",
  "specialization":"Online","target_query":"online mca",
  "hero":{"eyebrow":"AN MCA THAT FITS YOUR JOB","headline_pre":"A REAL MCA,","highlight":"100% ONLINE.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore specialisations",
    "art_prompt":"Sneha, a 24 year old Indian working woman in smart-casual, smiling as she studies coding on a laptop in the evening at home after work, warm lamp light, balanced and aspirational.","burst":"ONLINE!"},
  "statbar":[{"big":"100% ONLINE","label":"work & study"},{"big":"WEEKEND","label":"live classes"},
    {"big":"0% EMI","label":"pay monthly"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Sneha worked in IT support and wanted to move up.","dialogue":"I need a real tech degree.",
     "img_prompt":"Sneha, 24, in smart-casual at a work desk with a laptop, capable but ambitious, modern workplace."},
    {"n":2,"narration":"A full-time campus MCA meant quitting her job.","dialogue":"Do I give up my salary?",
     "img_prompt":"Sneha looking torn, glancing between her office badge and a campus brochure, soft conflicted expression, tidy desk."},
    {"n":3,"narration":"Then she found a recognised MCA she could do online.","dialogue":"Study and keep my job!",
     "img_prompt":"Sneha's face lighting up with relief at a laptop showing a 100% online MCA, warm glow, cosy home study corner in the evening."},
    {"n":4,"narration":"Now she studies evenings and weekends, career intact.","dialogue":"No pause, real growth.",
     "img_prompt":"Sneha happily attending a weekend live online class on her laptop at home, notebook beside her, calm and confident, warm light."}],
  "turn":{"title":"Why An Online MCA Just Works","points":[
    "Study 100% online, anytime, from your laptop. No campus, no commute.",
    "Weekend live classes plus recordings, so learning fits around a full-time job.",
    "The same UGC-entitled, NAAC A++ MCA, recognised for tech jobs and higher studies.",
    f"Just {FEE_LINE}, with 0% interest EMI or a discount on upfront payment."]},
  "proof":{"testimonials":[
    {"name":"Sneha Menon","spec":"MCA ONLINE","role":"Working Professional","metric":"NO PAUSE","stat":"kept my job",
     "quote":"I earned my MCA without leaving IT support. Weekend classes and recordings made it possible."},
    {"name":"Sana Iqbal","spec":"MCA DATA SCIENCE","role":"1st-Year Student","metric":"0% EMI","stat":"Rs 6,667 / mo",
     "quote":"The monthly EMI fit my salary and the schedule fit my life. It genuinely just worked."},
    {"name":"Divya Rao","spec":"MCA CLOUD","role":"Career Switcher","metric":"RECOGNISED","stat":"UGC-entitled",
     "quote":"A recognised degree earned online. My new tech employer accepted it without a second thought."},
    {"name":"Meena S","spec":"MCA ONLINE","role":"Graduated","metric":"PROMOTED","stat":"on my terms",
     "quote":"I studied around work and still graduated on time. That flexibility grew my tech career."}],
    "facts":[{"k":"Mode","v":"100% online, learn anytime with weekend live classes"},
      {"k":"Fee","v":FEE_LINE},{"k":"EMI","v":EMI_LINE},{"k":"Recognition","v":REC_LINE}]},
  "cta":cta("READY TO STUDY","ONLINE?"),
 },
 {
  "id":"mca-course-fees","intent":"Fees / affordability","program":"MCA",
  "specialization":"Data Science","target_query":"mca course fees",
  "hero":{"eyebrow":"THE FEE COMPARISON","headline_pre":"A RECOGNISED MCA,","highlight":"Rs 40,000/SEMESTER.",
    "headline_post":"","sub":"","cta1":"Get my fee + plan","cta2":"Explore specialisations",
    "art_prompt":"Arjun, a 23 year old Indian graduate man in smart-casual, happily surprised at a laptop showing an affordable MCA fee after comparing options, bright hopeful mood, tidy home.","burst":"Rs 40K!"},
  "statbar":[{"big":"Rs 40,000","label":"per semester"},{"big":"0% EMI","label":"pay monthly"},
    {"big":"DISCOUNT","label":"pay upfront"},{"big":"NAAC A++","label":"accredited"}],
  "panels":[
    {"n":1,"narration":"Arjun compared MCA fees, option after option.","dialogue":"Why is a tech degree so costly?",
     "img_prompt":"Arjun, 23, at a desk comparing several high fee figures in a notebook, concerned and focused, papers around him, tidy home."},
    {"n":2,"narration":"Many programs ran into lakhs of rupees.","dialogue":"Is a real MCA only for the rich?",
     "img_prompt":"Arjun looking discouraged at a laptop showing an expensive fee, chin in hand, soft disappointed expression, modest room."},
    {"n":3,"narration":"Then he found a recognised MCA at Rs 40,000 a semester.","dialogue":"Affordable and recognised?",
     "img_prompt":"Arjun's eyes widening with hope at a laptop showing a clear, affordable, recognised MCA fee, warm glow of relief."},
    {"n":4,"narration":"He enrolled on a 0% EMI he could manage.","dialogue":"A real MCA, no heavy debt!",
     "img_prompt":"Arjun smiling confidently holding a blank enrollment confirmation at home, calm and assured, warm hopeful light. No cash or money shown."}],
  "turn":{"title":"Why This MCA Fee Is A Steal","points":[
    f"Just {FEE_LINE}. A recognised tech degree at a fair, honest price.",
    "Pay upfront and get a discount, or split it into easy 0% interest EMI.",
    "0% interest EMI from about Rs 6,667/month, so there is no heavy lump sum.",
    "Only Rs 2,500 one-time registration. Clear fees, no hidden charges."]},
  "proof":{"testimonials":[
    {"name":"Arjun Pillai","spec":"MCA DATA SCIENCE","role":"Recent Graduate","metric":"Rs 40K / sem","stat":"recognised",
     "quote":"I compared everywhere. A UGC-entitled MCA at Rs 40,000 a semester was the clear, honest choice."},
    {"name":"Karan Das","spec":"MCA · SEM 1","role":"1st-Year Student","metric":"0% EMI","stat":"Rs 6,667 / mo",
     "quote":"The 0% EMI meant no lump sum. I pay a small amount each month and my MCA keeps going."},
    {"name":"Nisha Verma","spec":"MCA CLOUD","role":"Career Switcher","metric":"DISCOUNT","stat":"paid upfront",
     "quote":"We paid upfront and got a clear discount. A recognised tech degree at this price felt fair."},
    {"name":"Vikram Rao","spec":"MCA CYBER SECURITY","role":"Graduated","metric":"DEBT-LIGHT","stat":"no burden",
     "quote":"I finished my MCA without a heavy loan. The monthly plan fit my budget perfectly."}],
    "facts":[{"k":"Fee","v":FEE_LINE},{"k":"Upfront","v":"Discount on one-time full payment"},
      {"k":"EMI","v":EMI_LINE},{"k":"Extras","v":"Rs 2,500 one-time registration. No hidden charges."}]},
  "cta":cta("READY TO START","FOR Rs 40K A SEM?",button="Get my fee + plan"),
 },
 {
  "id":"mca-data-science","intent":"Specialisation / Data Science","program":"MCA",
  "specialization":"Data Science","target_query":"mca in data science",
  "hero":{"eyebrow":"TURN DATA INTO A CAREER","headline_pre":"AN MCA IN","highlight":"DATA SCIENCE.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore specialisations",
    "art_prompt":"Neha, a 24 year old Indian graduate woman in smart-casual, focused and confident, studying a clean data dashboard on a laptop, modern home, analytical and aspirational.","burst":"INSIGHT!"},
  "statbar":STATBAR,
  "panels":[
    {"n":1,"narration":"Neha loved finding patterns and solving problems.","dialogue":"Data is where I shine.",
     "img_prompt":"Neha, 24, happily exploring a simple data chart on a laptop at home, curious and analytical, modern room."},
    {"n":2,"narration":"But a data science career needed real depth.","dialogue":"How do I go pro?",
     "img_prompt":"Neha looking thoughtful, wondering how to build a data science career, a laptop with a simple chart open, modest room."},
    {"n":3,"narration":"Then she found an MCA in Data Science, online.","dialogue":"My data career starts here!",
     "img_prompt":"Neha's face lighting up with excitement at a laptop showing an MCA in Data Science, warm hopeful glow."},
    {"n":4,"narration":"She enrolled and began mastering the real craft.","dialogue":"From curious to qualified!",
     "img_prompt":"Neha confidently starting her first data science lesson on a laptop, notebook ready, focused and happy, warm light."}],
  "turn":{"title":"Why An MCA In Data Science","points":[
    "Master the real craft: Python, machine learning, data visualisation and big data.",
    "Apply real AI and analytics tools on hands-on projects from your very first semester.",
    f"{FEE_LINE}, with 0% interest EMI or a discount on upfront payment.",
    "A UGC-entitled, NAAC A++ online MCA that tech employers recognise."]},
  "proof":{"testimonials":[
    {"name":"Neha Rao","spec":"MCA DATA SCIENCE","role":"Recent Graduate","metric":"MY SKILL","stat":"now a career",
     "quote":"I loved data. This MCA turned that into a real, in-demand data science career."},
    {"name":"Kavya Menon","spec":"MCA DATA SCIENCE","role":"1st-Year Student","metric":"HANDS-ON","stat":"from sem 1",
     "quote":"Real machine-learning projects from semester one made me genuinely job-ready."},
    {"name":"Arun Nair","spec":"MCA DATA SCIENCE","role":"Working Professional","metric":"0% EMI","stat":"kept my job",
     "quote":"The 0% EMI let me move into data science without quitting my job."},
    {"name":"Sara Thomas","spec":"MCA DATA SCIENCE","role":"Graduated","metric":"PLACED","stat":"recognised",
     "quote":"A recognised MCA plus real data skills got me hired into a data role quickly."}],
    "facts":[{"k":"Learn","v":"Python, machine learning, data visualisation, big data"},
      {"k":"Fee","v":FEE_LINE},{"k":"EMI","v":EMI_LINE},{"k":"Recognition","v":REC_LINE}]},
  "cta":cta("READY FOR A","DATA CAREER?"),
 },
 {
  "id":"mca-cyber-security","intent":"Specialisation / Cyber Security","program":"MCA",
  "specialization":"Cyber Security","target_query":"mca in cyber security",
  "hero":{"eyebrow":"DEFEND THE DIGITAL WORLD","headline_pre":"AN MCA IN","highlight":"CYBER SECURITY.",
    "headline_post":"","sub":"","cta1":BTN,"cta2":"Explore specialisations",
    "art_prompt":"Karthik, a 24 year old Indian graduate man in smart-casual, confident and focused, studying a clean secure-shield glyph on a laptop, modern home, capable and aspirational.","burst":"SECURE!"},
  "statbar":STATBAR,
  "panels":[
    {"n":1,"narration":"Karthik was fascinated by how systems stay safe.","dialogue":"I want to stop the hackers.",
     "img_prompt":"Karthik, 24, focused at a laptop showing a simple shield glyph, curious and driven, modern room."},
    {"n":2,"narration":"But a security career needed real qualifications.","dialogue":"How do I make this a job?",
     "img_prompt":"Karthik looking thoughtful, wondering how to build a cyber security career, a laptop open, modest room."},
    {"n":3,"narration":"Then he found an MCA in Cyber Security, online.","dialogue":"My security career starts here!",
     "img_prompt":"Karthik's face lighting up with excitement at a laptop showing an MCA in Cyber Security, warm hopeful glow."},
    {"n":4,"narration":"He enrolled and began mastering the real craft.","dialogue":"From curious to qualified!",
     "img_prompt":"Karthik confidently starting his first cyber security lesson on a laptop, notebook ready, focused and happy, warm light."}],
  "turn":{"title":"Why An MCA In Cyber Security","points":[
    "Master the real craft: network security, ethical hacking, cryptography and cloud security.",
    "Apply real security tools on hands-on labs from your very first semester.",
    f"{FEE_LINE}, with 0% interest EMI or a discount on upfront payment.",
    "A UGC-entitled, NAAC A++ online MCA that tech employers recognise."]},
  "proof":{"testimonials":[
    {"name":"Karthik Rao","spec":"MCA CYBER SECURITY","role":"Recent Graduate","metric":"MY PASSION","stat":"now a career",
     "quote":"I was fascinated by security. This MCA turned that into a real cyber security career."},
    {"name":"Kavya Menon","spec":"MCA CYBER SECURITY","role":"1st-Year Student","metric":"HANDS-ON LABS","stat":"from sem 1",
     "quote":"Real security labs from semester one made me confident and genuinely job-ready."},
    {"name":"Arun Nair","spec":"MCA CYBER SECURITY","role":"Working Professional","metric":"0% EMI","stat":"kept my job",
     "quote":"The 0% EMI let me move into cyber security without quitting my job."},
    {"name":"Sara Thomas","spec":"MCA CYBER SECURITY","role":"Graduated","metric":"PLACED","stat":"in demand",
     "quote":"A recognised MCA plus real security skills got me hired into an in-demand role."}],
    "facts":[{"k":"Learn","v":"Network security, ethical hacking, cryptography, cloud security"},
      {"k":"Fee","v":FEE_LINE},{"k":"EMI","v":EMI_LINE},{"k":"Recognition","v":REC_LINE}]},
  "cta":cta("READY TO","DEFEND & EARN?"),
 },
]

for s in STORIES_DATA:
    out = json.dumps(s, ensure_ascii=False, indent=2).replace("Rs ", "₹")
    (STORIES / f"{s['id']}.json").write_text(out, encoding="utf-8")
    print("wrote", s["id"], "->", s["target_query"])
print(f"\n{len(STORIES_DATA)} MCA stories written")
