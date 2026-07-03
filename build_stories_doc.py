#!/usr/bin/env python3
"""Build STORIES-50.html — demand-driven: 50 Chapter-2 (4-panel) stories, each mapped to a real search query."""
import html, pathlib

# (course, angle, target_query, count, who, [ (caption, bubble, art) x4 ])
S = [
("MBA","Online — flagship","online mba courses",808,"Nikhil, 28 — wants an MBA but can't leave his job",[
 ("Nikhil scrolled every 'online MBA courses' result and closed the tab, unsure.","Can I really do an MBA while working?","Young man at night scrolling search results on a laptop, office bag nearby."),
 ("Campus classes clashed with the shifts he couldn't afford to lose.","I can't quit to sit in a classroom.","A campus timetable versus his work desk — torn between them."),
 ("Then he found it — a full online MBA, learn anytime, recognised degree.","Class after work? That works!","Relief at the laptop showing an online MBA, warm evening light."),
 ("Now he studies at 10 pm and leads at 10 am — no pause, no quitting.","Working AND learning. Finally.","Nikhil confident at work by day, studying by night, split scene.")]),
("MBA","Online — in India","online mba courses in india",551,"Ananya, 30 — wary of foreign, dollar-priced options",[
 ("Every 'online MBA' ad Ananya saw was foreign, flashy, priced in dollars.","Is there a real Indian one?","Woman at a laptop seeing overseas MBA ads, skeptical."),
 ("She needed a UGC-recognised Indian degree that employers here trust.","Will Indian companies accept it?","Worried, comparing logos and 'recognised?' notes."),
 ("Then — a UGC-entitled online MBA from an Indian university, NAAC A++.","Recognised, Indian, online — yes!","Relief at the laptop, NAAC A++ and UGC badges glowing."),
 ("Her HR verifies it instantly; the promotion goes through.","Recognised where it matters.","Ananya's degree accepted, HR nods, proud moment.")]),
("MBA","Online — working professionals","mba for working professionals",226,"Rakesh, 34 — 12 years' experience, no degree to show",[
 ("Rakesh trains new managers who out-rank him on paper.","Experience isn't opening the next door.","Man mentoring juniors who wear manager badges."),
 ("A campus MBA meant a career break he simply couldn't take.","I can't stop working at 34.","Worried at home, family and bills, high fees."),
 ("Then — an MBA built for working professionals: weekends and online.","Made for people like me!","Excited at the laptop, a 'for working professionals' MBA."),
 ("Two years on, his experience finally has the title to match.","Manager. On paper too.","Rakesh promoted, confident, team behind him.")]),
("MBA","Online — programs","online mba programs",707,"Sneha, 27 — overwhelmed by too many 'programs'",[
 ("A hundred 'online MBA programs' — Sneha had no idea which was real.","Which one actually counts?","Woman staring at a wall of program ads, confused."),
 ("Some were cheap and fake; the real ones felt out of budget.","Real ones cost a bomb, right?","Worried, comparing prices and 'recognised?' flags."),
 ("Then — one UGC-entitled online MBA program, affordable and flexible.","Real AND affordable — this one!","Relief landing on a trustworthy program, a glow."),
 ("She enrols in the program that's actually recognised — and priced right.","Chose right. Finally.","Sneha enrolled, confident, a welcome screen.")]),
("MBA","Fees","mba courses fees",716,"Vikram, 29 — braced for the worst when he searched fees",[
 ("Vikram typed 'mba courses fees' expecting numbers that would end the dream.","Please don't be in lakhs...","Man tensely searching MBA fees on a phone at night."),
 ("The big B-schools wanted 10-20 lakh he'd never have.","That's a house, not a degree.","Shocked at huge fee figures on the screen."),
 ("Then — a recognised online MBA at a fraction of the cost, 0% EMI.","Wait — I can actually pay this!","Relief at an affordable fee and EMI, warm glow."),
 ("He enrols on a monthly plan — no loan, no lakhs.","Big degree. Small instalments.","Vikram enrolling confidently, an EMI plan on screen.")]),
("MBA","Fees — JAIN","jain university mba fees",473,"Priya, 31 — heard JAIN was good, feared the price",[
 ("Priya kept hearing JAIN was reputable — surely that meant expensive.","Good college = huge fees?","Woman searching 'jain university mba fees', hopeful but nervous."),
 ("A reputed name usually meant a reputed price tag.","Can I even afford a good one?","Worried at the laptop, a quality-versus-cost dilemma."),
 ("Then the fee loaded — affordable, with EMI, and NAAC A++ behind it.","Reputed AND affordable?!","Pleasant shock at an affordable JAIN fee, accreditation badges."),
 ("She gets the respected degree without the scary number.","Quality, not lakhs.","Priya enrolled at JAIN Online, proud.")]),
("MBA","Fees — online","online mba courses fees",601,"Arjun, 26 — assumed 'online' still meant costly",[
 ("Arjun figured even online MBAs would cost a fortune.","Online, but still pricey?","Man checking online MBA fees, doubtful."),
 ("Some 'online' programs charged more than campus ones.","Why is this so expensive?","Worried, comparing inflated online fees."),
 ("Then — an online MBA that's genuinely affordable, pay-monthly.","Finally — online AND affordable!","Relief at an affordable online MBA fee."),
 ("He starts learning this month — for less than he feared per year.","Smart choice, small cost.","Arjun studying online, satisfied.")]),
("MBA","Distance","distance mba courses",522,"Kavya, 33 — no top B-school anywhere near her town",[
 ("In Kavya's town, the nearest good B-school was eight hours away.","Do I have to leave everything?","Woman looking at a map, her small town far from the cities."),
 ("Relocating for a campus meant leaving family and job behind.","I can't move my whole life.","Torn between home and a distant city."),
 ("Then — a distance MBA: learn from her town, degree recognised nationwide.","The B-school comes to me!","Excited at the laptop at home, a distance MBA."),
 ("She earns a national-grade MBA without leaving her hometown.","Small town. Big degree.","Kavya graduating from home, proud family.")]),
("MBA","Distance education","mba distance education",482,"Imran, 35 — climbed on a part-time bachelor's, wants to finish",[
 ("Imran clawed up with a part-time bachelor's; the ceiling returned.","One more degree to break through.","Man at a desk, a glass ceiling of light above him."),
 ("Full-time study was never an option with a family to run.","No time to sit in a class.","Worried, balancing family and work."),
 ("Then — an MBA by distance education: flexible, affordable, recognised.","Learn on my own hours!","Relief at the laptop, a distance-education MBA."),
 ("He breaks the ceiling — degree done, on his terms.","Made it. My way.","Imran promoted, confident.")]),
("MBA","Best — online","best online mba in india",383,"Meera, 28 — burned once by a worthless certificate",[
 ("Meera once paid for an 'online course' no employer recognised.","Never wasting money on fake again.","Woman frustrated, a useless certificate in hand."),
 ("This time she searched 'best online MBA in India' — trust was everything.","Is it actually recognised?","Carefully checking rankings and accreditations."),
 ("Then — a UGC-entitled, NAAC A++ online MBA, ranked and real.","This one's the real deal!","Relief at legitimate badges and rankings."),
 ("Her new degree passes every background check.","Recognised. Verified. Mine.","Meera's credential verified, HR approves.")]),
("MBA","Top colleges","top distance mba colleges in india",277,"Sandeep, 32 — wants a name that impresses on a CV",[
 ("Sandeep wanted a distance MBA that still looked strong on a CV.","Will recruiters respect it?","Man polishing his CV, unsure."),
 ("Many distance colleges felt second-rate.","Not just any college.","Comparing college names, doubtful."),
 ("Then — a top-ranked distance MBA: NAAC A++, industry-aligned.","A name that opens doors!","Excited at a top-college listing, rankings."),
 ("Recruiters recognise it instantly.","CV upgraded.","Sandeep in an interview, the interviewer nods.")]),
("MBA","Reviews / ranking","best distance mba in india",277,"Divya, 30 — reads every review before she commits",[
 ("Divya reads reviews for everything — a degree deserved the same.","What do real students say?","Woman reading reviews and ratings on a laptop."),
 ("Flashy ads told her nothing about real outcomes.","Ads aren't proof.","Skeptical at glossy ads."),
 ("Then — a highly-reviewed, top-ranked distance MBA, alumni wins everywhere.","The reviews are real!","Glowing student reviews and outcomes on screen."),
 ("She joins the batch the reviews raved about.","Chose by proof, not ads.","Divya enrolled, a five-star vibe.")]),
("MBA","Eligibility","mba course eligibility",153,"Farhan, 27 — average marks, sure he wouldn't qualify",[
 ("Farhan assumed his average marks locked him out of any MBA.","Am I even eligible?","Man hesitating over 'eligibility' on a laptop."),
 ("Big schools demanded high scores and entrance ranks.","They only want toppers.","Intimidating eligibility criteria on screen."),
 ("Then — a simple eligibility: a bachelor's degree, that's it.","I qualify?! Really?","Relief at an easy eligibility checklist, green ticks."),
 ("He applies in minutes — and gets in.","Eligible after all.","Farhan's acceptance screen, delighted.")]),
("MBA","Admission","mba admission",244,"Neha, 29 — dreads long, confusing admission processes",[
 ("Neha put off her MBA for years, dreading the admission maze.","Too many forms, too much hassle.","Woman overwhelmed by stacks of paperwork."),
 ("Campus admissions meant tests, queues, and travel.","I don't have time for all this.","Long queues and entrance-test stress."),
 ("Then — a fully online admission: apply, upload, done.","Admission in minutes?!","A simple online application flow, relief."),
 ("She's enrolled before the weekend ends.","That was actually easy.","Neha with an 'Admitted' confirmation, smiling.")]),
("MBA","Generic — courses","mba courses",493,"Rohit, 26 — knows he wants 'an MBA', nothing more",[
 ("Rohit knew he wanted 'an MBA' — but had no idea where to start.","So many courses... which one?","Man overwhelmed by MBA course options."),
 ("Every option looked costly, rigid, or confusing.","Is there a simple, doable one?","Confused at a cluttered comparison."),
 ("Then — one clear, flexible, affordable online MBA with guidance.","A clear path — at last!","Relief at a simple, guided MBA page."),
 ("A mentor maps his specialisation and he begins.","From lost to enrolled.","Rohit with a mentor, a confident start.")]),
("MBA","Scope / salary","online mba salary in india",35,"Aisha, 31 — needs proof it'll actually pay off",[
 ("Aisha wouldn't spend two years unless the numbers made sense.","Will this actually pay off?","Woman weighing salary-growth charts."),
 ("She feared spending on a degree that changed nothing.","What if my salary doesn't move?","Doubtful at a flat salary line."),
 ("Then she saw the outcomes — alumni salary jumps, real roles.","The ROI is real!","A rising salary graph, alumni roles listed."),
 ("Eighteen months later, her pay grade proves it.","Paid for itself.","Aisha with a raise letter, satisfied.")]),
("MBA","Specialisation — Digital Marketing","mba in digital marketing",227,"Kabir, 27 — self-taught marketer chasing a lead role",[
 ("Kabir runs campaigns but keeps getting passed for lead roles.","I need the credential to lead.","Man running campaigns, still a junior title."),
 ("A specialised MBA felt costly and campus-bound.","Can't quit to specialise.","Worried at fees and a campus timetable."),
 ("Then — an online MBA in Digital Marketing, affordable and flexible.","Specialise while I work!","Excited at an MBA Digital Marketing page."),
 ("He's promoted to Digital Marketing Lead.","From doer to leader.","Kabir leading a marketing team, confident.")]),
("MBA","Specialisation — HR","mba hr courses",201,"Fatima, 30 — the team's unofficial HR, wants it official",[
 ("Everyone leans on Fatima for people problems — minus the HR title.","Make my role official.","Woman counselling a colleague warmly."),
 ("An HR MBA on campus meant leaving her job.","I can't step away to study.","Worried, job versus course."),
 ("Then — an online MBA in HR: weekends, budget EMI.","Title, here I come!","Excited at an MBA HR page."),
 ("She's appointed Head of HR.","People are my profession now.","Fatima as HR Head, a nameplate on her desk.")]),
("MBA","Specialisation — Hospital Mgmt","mba in hospital management",212,"Priya, 32 — a nurse who really runs the ward",[
 ("Priya runs the ward better than anyone — without the manager badge.","I hold this place together.","Nurse coordinating a busy hospital ward."),
 ("A hospital-management MBA meant quitting nursing.","I can't leave the floor.","Tired post-shift, worried at fees."),
 ("Then — an online MBA in Hospital Management, study between shifts.","Care by day, degree by night!","Relief at an MBA Hospital Management page."),
 ("She's promoted to manage the whole department.","Nurse to manager.","Priya in an admin role, proud.")]),
("MBA","Specialisation — Finance","mba in finance",193,"Karan, 27 — great with numbers, stuck without the degree",[
 ("Karan reads markets for fun; his title still says 'executive.'","I want a career in finance.","Man reading market charts eagerly."),
 ("A finance MBA felt like lakhs and a career pause.","Too costly to switch.","Worried at fees."),
 ("Then — an online MBA in Finance: affordable, keep earning.","Switch without the free-fall!","Excited at an MBA Finance page."),
 ("New title: Financial Analyst.","Numbers are my job now.","Karan at a finance desk, confident.")]),
# ---------------- BBA (8) ----------------
("BBA","Online","online bba course",272,"Aditya, 18 — minds the family shop, can't attend full-time",[
 ("Aditya minds the family shop by day; college clashes with all of it.","I can't sit in class all day.","Teen at a shop counter, a college flyer set aside."),
 ("A campus BBA meant abandoning the shop that feeds them.","Who runs this if I go?","Torn between the shop and college."),
 ("Then — an online BBA: study anytime, a real degree.","Learn AND mind the shop!","Excited at a laptop on the counter."),
 ("He runs the shop by day and earns his BBA by night.","Both. At once.","Aditya studying after closing, proud.")]),
("BBA","Online (alt)","bba online course",246,"Riya, 18 — small town, no good college nearby",[
 ("Riya's town had no college with a real BBA.","Do I have to move away?","Teen girl looking toward a distant city."),
 ("Moving to a city cost more than the course itself.","Hostel and fees? Too much.","Worried at hostel and city costs."),
 ("Then — an online BBA she could do from home, recognised.","College, from my room!","Delighted at a laptop at home."),
 ("She's a BBA student without leaving home.","No move. Full degree.","Riya studying at home, family proud.")]),
("BBA","Fees — JAIN","jain university bba fees structure",339,"Aarav, 18 — first-gen dreamer bracing for the fee",[
 ("Dawn in Hubballi — Aarav opens the JAIN BBA fee structure, heart pounding.","Please don't be in lakhs.","Teen at a tea stall checking fees on a phone."),
 ("A business degree felt like it was only for rich kids.","Not for a boy like me?","A hopeful face dimming at the thought of cost."),
 ("Then the structure loaded — ₹45,000/year, 0% EMI, no hidden charges.","₹45,000? I can do this!","Eyes lighting up at a clear fee breakdown."),
 ("Appa slides over a savings envelope; Aarav enrols.","Step one — done.","Father handing over an envelope, mother teary and happy.")]),
("BBA","Fees — course","bba course fees",229,"Sneha, 18 — comparing fees across every college",[
 ("Sneha listed every BBA's fees — most made her stomach drop.","Why is a degree so costly?","Teen comparing high fee figures in a notebook."),
 ("The cheaper ones weren't even recognised.","Cheap OR real — never both?","Torn between price and recognition."),
 ("Then — a recognised BBA at ₹45,000/year with EMI.","Affordable AND real!","Relief at an affordable, recognised fee."),
 ("She picks the one that's both.","Smartest choice on my list.","Sneha enrolling, satisfied.")]),
("BBA","Admission","bba admission",113,"Neha, 18 — just finished 12th, unsure how to apply",[
 ("Fresh out of 12th, Neha found BBA admissions confusing.","Where do I even start?","Teen puzzling over admission steps."),
 ("Entrance forms and deadlines felt overwhelming.","So many forms and dates!","Overwhelmed by paperwork."),
 ("Then — a simple online admission after 12th, no entrance stress.","Apply online? That's it?","An easy online application flow."),
 ("Admitted before the week ends.","That was simple.","Neha with an 'Admitted' screen, delighted.")]),
("BBA","Generic — course","bba course",353,"Ishaan, 18 — knows he wants business, not much else",[
 ("Ishaan knew 'business' was his path — the how was a blur.","A BBA... but which, how?","Teen unsure among options."),
 ("Every route looked expensive or complicated.","Is there a simple way in?","Confused at cluttered options."),
 ("Then — a clear, affordable online BBA with guidance.","A simple path — yes!","Relief at a guided BBA page."),
 ("A counsellor picks his elective; he begins.","From clueless to enrolled.","Ishaan with a counsellor, confident.")]),
("BBA","Specialisation — Aviation","bba in aviation",95,"Farhan, 18 — grew up watching planes",[
 ("From his rooftop, Farhan dreams of running airport operations.","I belong at the airport.","Teen watching a plane, eyes bright."),
 ("Aviation courses looked glamorous — and priced like it.","Sky-high fees?","Worried at a pricey brochure."),
 ("Then — an affordable online BBA in Aviation Management.","My runway just opened!","Excited at a BBA Aviation page."),
 ("Ground-ops trainee at a real airport.","Cleared for take-off.","Farhan in an airport uniform, tarmac behind.")]),
("BBA","Specialisation — Digital Marketing","bba in digital marketing",110,"Kabir, 18 — turns memes viral, wants it as a career",[
 ("Kabir's posts go viral; everyone calls it 'just a hobby.'","This can be a career.","Teen with viral posts around him."),
 ("A degree for it? He assumed it cost a bomb.","Talent's free. Degrees aren't.","Doubtful at fees."),
 ("Then — an online BBA in Digital Marketing: affordable, EMI.","Turn viral into a career!","Excited at a BBA Digital Marketing page."),
 ("A local brand hires him in year one.","Memes to metrics.","Kabir running a brand's socials, proud.")]),
# ---------------- B.Com (6) ----------------
("B.Com","Online","bcom online course",219,"Pooja, 18 — runs the family shop's books",[
 ("Pooja keeps the shop's accounts; a campus B.Com would pull her away.","I can't leave the shop.","Teen doing ledgers at a counter."),
 ("City college meant travel, hostel, and lost help at home.","Who minds the shop?","Torn between shop and college."),
 ("Then — an online B.Com: study from the counter.","Books and business, together!","A laptop on the shop counter, happy."),
 ("Customers by day, coursework by night.","Shopkeeper today, CA tomorrow.","Pooja serving a customer, books beside her.")]),
("B.Com","Online — for students","online courses for bcom students",184,"Manish, 19 — working part-time, studying on the side",[
 ("Manish works part-time; regular college hours were impossible.","I have to earn while I learn.","Teen at a part-time job, tired."),
 ("Fixed classes clashed with every shift.","No time for a timetable.","A shift schedule versus a class schedule."),
 ("Then — an online B.Com he could fit around work.","Study on my schedule!","Relief at a flexible online B.Com."),
 ("He earns and studies — no compromise.","Both boxes ticked.","Manish working and studying, split scene, proud.")]),
("B.Com","Fees","jain university online bcom fees",179,"Vikram, 18 — smart, but money is tight at home",[
 ("Vikram's marks were strong; the family budget wasn't.","Can we afford a real degree?","Teen watching his parents count money."),
 ("Good colleges seemed to want money they didn't have.","Quality feels out of reach.","Worried at fee figures."),
 ("Then — an affordable online B.Com fee, pay-monthly.","This fits our budget!","Relief at an affordable fee and EMI."),
 ("First-gen commerce student, enrolled.","First of many firsts.","Vikram enrolled, family proud.")]),
("B.Com","Professional — ACCA","jain university b com with acca fees",132,"Aisha, 19 — wants a global accounting career",[
 ("Aisha dreams of auditing for companies worldwide.","I want a global finance career.","Teen with a globe and calculator."),
 ("Global qualifications sounded impossibly expensive.","Global = a fortune, right?","Worried at overseas costs."),
 ("Then — a B.Com with an ACCA pathway: affordable, EMI.","World-class, within budget!","Excited at a B.Com + ACCA page."),
 ("She clears her first ACCA paper.","Local roots, global ledger.","Aisha celebrating, a world map behind.")]),
("B.Com","Admission","bcom online admission",91,"Harish, 18 — missed the regular-college cutoffs",[
 ("Harish missed the local college cutoffs by a whisker.","Did I miss my only chance?","Teen dejected at a cutoff list."),
 ("He feared waiting a whole year to reapply.","A year lost?","A calendar, time slipping away."),
 ("Then — open online B.Com admission: apply now, after 12th.","I can start this term!","Relief at an open admission page."),
 ("Enrolled — no year wasted.","Back on track.","Harish admitted, relieved and proud.")]),
("B.Com","Specialisation — Accounting","bcom accounts",54,"Sana, 20 — already does neighbours' accounts",[
 ("Sana keeps books for half the neighbourhood already.","I could do this professionally.","Young woman helping with accounts."),
 ("A proper degree felt like a cost she couldn't justify.","Is the paper worth the price?","Worried at a desk of ledgers."),
 ("Then — an affordable online B.Com in Accounting & Finance.","Turn skill into a career!","Excited at a B.Com Accounts page."),
 ("She opens a small accounting desk.","Accountant. Official soon.","Sana at her own desk, clients waiting.")]),
# ---------------- MCA (6) ----------------
("MCA","Fees — JAIN","jain university mca fees",366,"Karthik, 23 — helpdesk coder eyeing a real dev role",[
 ("Karthik searched the JAIN MCA fee, bracing for lakhs.","Please be affordable.","Man checking MCA fees at night."),
 ("Master's degrees usually cost more than he earned.","On my salary? Doubtful.","Worried at fee figures."),
 ("Then — an affordable MCA fee, 0% EMI, keep the job.","This fits my budget!","Relief at an affordable MCA fee."),
 ("First real app shipped; title: Developer.","Helpdesk to codebase.","Karthik demoing an app, proud.")]),
("MCA","Fees — structure","jain university mca fees structure",317,"Ritika, 24 — wants every rupee spelled out",[
 ("Ritika wanted the full fee structure — no hidden shocks.","What's the real total?","Woman scanning a fee breakdown carefully."),
 ("Other colleges buried costs in the fine print.","Hidden fees everywhere.","Skeptical at fine print."),
 ("Then — a clear MCA fee structure: tuition, exam, EMI, done.","All clear, no surprises!","A transparent fee table, relief."),
 ("She enrols knowing exactly what she'll pay.","No surprises. Signed.","Ritika enrolling confidently.")]),
("MCA","Online","mca online course",304,"Naveen, 26 — sysadmin who can't attend day classes",[
 ("Naveen keeps servers alive on rotating shifts — day college is impossible.","My hours are all over.","Man in a server room, odd hours."),
 ("A campus MCA needed fixed daytime attendance.","I can't be there 9-to-5.","A shift clash with class times."),
 ("Then — an online MCA: learn on his own schedule.","Study around my shifts!","Relief at an online MCA page."),
 ("He moves from sysadmin to cloud engineer.","Server room to cloud.","Naveen presenting a cloud diagram.")]),
("MCA","Distance","mca distance education",209,"Prakash, 27 — BCA grad, no dev master's near him",[
 ("Prakash's BCA plateaued; no good MCA campus near his town.","Do I have to relocate?","Man at a desk, a distant-city map."),
 ("Moving for a master's meant losing his income.","Can't afford to move and study.","Worried at costs."),
 ("Then — an MCA by distance education: learn from home, recognised.","The master's comes to me!","Relief at a distance MCA page."),
 ("Promoted to Senior Software Engineer.","Ceiling? Gone.","Prakash leading a code review.")]),
("MCA","Specialisation — Cybersecurity","jain university mca cyber security",99,"Zoya, 24 — spots every scam, wants to defend for real",[
 ("Zoya flags phishing before anyone clicks — she wants it as a career.","I could defend companies.","Woman flagging a scam email."),
 ("A cybersecurity master's sounded elite and pricey.","Is that world affordable?","Worried at fees."),
 ("Then — an affordable MCA in Cyber Security, online.","Defender mode: unlocked!","Excited at an MCA Cyber Security page."),
 ("She lands a security-analyst role.","Ethical hacker. Employed.","Zoya at a security dashboard.")]),
("MCA","Admission","mca admission",147,"Aditya, 25 — dreads entrance tests and queues",[
 ("Aditya kept postponing his MCA, dreading the admission grind.","Entrance tests again?","Man avoiding a stack of forms."),
 ("Campus admission meant tests, travel, and waiting.","No time for all that.","Long queue and test stress."),
 ("Then — a simple online MCA admission after graduation.","Apply online, done!","An easy online application."),
 ("Enrolled in a weekend.","That was painless.","Aditya admitted, relieved.")]),
# ---------------- M.Com (4) ----------------
("M.Com","Distance","mcom distance education",187,"Divya, 29 — best accountant, no time for campus",[
 ("Divya's the sharpest accountant around — and the least promoted.","They want a master's.","Woman at a file-piled desk."),
 ("Campus classes with a job and family? Impossible.","No time to attend.","Juggling work and home."),
 ("Then — an M.Com by distance: study after hours, affordable.","Grow without pausing life!","Relief at a distance M.Com page."),
 ("Master's in hand, she gets the role she earned.","Senior Accountant. Finally.","Divya with a certificate, recognised.")]),
("M.Com","Distance (alt)","m com distance education",169,"Mohan, 30 — bank officer eyeing the manager's cabin",[
 ("Mohan's a solid officer; the manager's cabin needs a master's.","One degree from that door.","Officer glancing at a manager's cabin."),
 ("Evenings were gone after the branch closed.","No time after work.","Tired late nights."),
 ("Then — an M.Com by distance: study nights, easy fees.","The cabin's in reach!","Excited at a distance M.Com page."),
 ("New title on the door: Branch Manager.","Officer to manager.","Mohan in the manager's cabin, confident.")]),
("M.Com","Online","online mcom course",185,"Kavya, 28 — wants to specialise while working",[
 ("Kavya wanted to specialise in finance without quitting.","Upskill, but keep earning.","Woman at an accounts desk."),
 ("Fixed classes clashed with office hours.","Can't attend 9-to-5 classes.","A schedule clash."),
 ("Then — an online M.Com: flexible and affordable.","Learn on my hours!","Relief at an online M.Com page."),
 ("She steps up to a finance-analyst role.","Specialised. Promoted.","Kavya presenting a forecast.")]),
("M.Com","Fees","jain university online m com fees",163,"Sunil, 32 — stuck at the same grade for years",[
 ("Ten years in, Sunil's still at the same grade — a master's is the key.","Experience isn't enough.","Man at a long-held desk."),
 ("He feared a good master's would cost too much.","Can I afford to level up?","Worried at fees."),
 ("Then — an affordable online M.Com fee, pay-monthly.","Never too costly to grow!","Relief at an affordable fee."),
 ("He steps into a finance-lead role.","Same man, new grade.","Sunil in a lead role, confident.")]),
# ---------------- MA (4) ----------------
("MA","Distance — English","ma english distance education",157,"Aparna, 26 — a teacher who wants to teach literature",[
 ("Aparna teaches by day and writes stories by night.","I want to teach literature.","Teacher in a modest classroom, books everywhere."),
 ("A master's meant leaving her school and students.","I can't abandon my class.","Torn between students and a prospectus."),
 ("Then — MA English by distance: study anywhere, affordable.","Keep teaching AND grow!","Relief at a distance MA English page."),
 ("Now she's 'Aparna, MA' — a scholar for her students.","Lifelong learner. Literally.","Aparna teaching, MA certificate framed.")]),
("MA","Distance — Economics","ma economics distance education",133,"Rohit, 27 — data-entry clerk who wants to do policy",[
 ("Rohit types economic data all day and itches to interpret it.","I want to shape policy.","Man at a data-entry desk."),
 ("An economics master's felt costly and time-heavy.","Between job and money? Tough.","Worried at a laptop."),
 ("Then — MA Economics by distance: affordable, flexible.","From data to decisions!","Excited at a distance MA Economics page."),
 ("He co-authors his first policy brief.","Analyst. On the record.","Rohit presenting a brief.")]),
("MA","Distance — Psychology","ma psychology distance education",89,"Meher, 25 — the friend everyone leans on",[
 ("Meher is everyone's 3 a.m. call; she wants to help for real.","I could be a counsellor.","Woman comforting a friend."),
 ("A psychology master's sounded long and pricey.","Can I afford to help professionally?","Worried at home."),
 ("Then — MA Psychology by distance: budget fees, flexible.","Empathy as a profession!","Excited at a distance MA Psychology page."),
 ("She starts her counselling practicum.","Listener to counsellor.","Meher in a calm counselling room.")]),
("MA","Distance — general","ma distance education",151,"Vikas, 28 — civil-services aspirant, short on time and money",[
 ("Vikas preps for civil services between shifts — time and money run thin.","I can't study full-time.","Man studying late after work."),
 ("Another degree felt like one cost too many.","A fee I can't manage?","Worried at a modest desk."),
 ("Then — an MA by distance: affordable, alongside his prep.","Sharpen prep AND degree!","Excited at a distance MA page."),
 ("He clears prelims — with an edge.","Future officer, loading.","Vikas celebrating a cleared exam.")]),
# ---------------- BCA (2) ----------------
("BCA","Fees — JAIN","jain university bca fees",149,"Rahul, 18 — self-taught small-town coder",[
 ("Rahul taught himself to code on slow small-town internet.","I'll build things the world uses.","Teen coding on an old laptop at night."),
 ("A city computer degree cost more than the family earned.","Tech degrees aren't for us.","Excitement fading at high fees, father working behind."),
 ("Then — an affordable JAIN online BCA: small fee, pay-monthly.","I can do this from home!","Face lighting up at the fee page."),
 ("His first program runs — Software Engineer, loading.","Small town. Big code.","Rahul as the code runs, dawn light.")]),
("BCA","Online","jain university online bca",152,"Isha, 18 — no tech college near her town",[
 ("Isha loves building apps; no tech college sits near her town.","Do I have to leave home?","Teen with an app idea, a distant city."),
 ("Moving to a city for a BCA cost more than the degree.","Hostel and fees? Too much.","Worried at city costs."),
 ("Then — an online BCA she could do from home, recognised.","A tech degree, from my room!","Delighted at an online BCA page."),
 ("She ships her first app in first year.","Coder. From home.","Isha deploying an app, proud.")]),
]

def e(s): return html.escape(str(s))
order=[]; groups={}
for st in S:
    c=st[0]
    if c not in groups: groups[c]=[]; order.append(c)
    groups[c].append(st)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#fdf3da;--card:#fffdf5;--ink:#241d0f;--muted:#736a52;--navy:#1a237e;--gold:#f5b301;--line:#e8dcba;--chip:#fff6d9;--tgt:#eef0ff}
@media(prefers-color-scheme:dark){:root{--bg:#14121b;--card:#201c2c;--ink:#efe9dd;--muted:#a49b86;--navy:#aeb4ff;--gold:#f5b301;--line:#342e44;--chip:#2a2438;--tgt:#232a4d}}
:root[data-theme=light]{--bg:#fdf3da;--card:#fffdf5;--ink:#241d0f;--muted:#736a52;--navy:#1a237e;--gold:#f5b301;--line:#e8dcba;--chip:#fff6d9;--tgt:#eef0ff}
:root[data-theme=dark]{--bg:#14121b;--card:#201c2c;--ink:#efe9dd;--muted:#a49b86;--navy:#aeb4ff;--gold:#f5b301;--line:#342e44;--chip:#2a2438;--tgt:#232a4d}
body{background:var(--bg);color:var(--ink);font-family:'Segoe UI',system-ui,Roboto,Helvetica,Arial,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:980px;margin:0 auto;padding:40px 20px 72px}
.display{font-family:'Arial Black','Segoe UI',Impact,sans-serif;font-weight:900;letter-spacing:-.5px;line-height:1}
header.top{border-bottom:4px solid var(--gold);padding-bottom:22px}
header.top .kick{font-size:12px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:var(--gold)}
header.top h1{font-size:clamp(30px,5vw,48px);color:var(--navy);margin:8px 0 8px;text-wrap:balance}
header.top p{color:var(--muted);max-width:74ch;font-size:15px}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 2px}
.legend b{background:var(--navy);color:#fff;font-size:12px;font-weight:800;padding:5px 10px;border-radius:999px;letter-spacing:.5px}
.legend b span{color:var(--gold)}
h2.course{font-family:'Arial Black',sans-serif;font-weight:900;font-size:22px;color:var(--navy);margin:40px 0 4px;display:flex;align-items:baseline;gap:12px;border-top:2px solid var(--line);padding-top:26px}
h2.course .cnt{font-size:12px;font-weight:800;color:var(--gold);letter-spacing:1px}
.grid{display:grid;gap:16px;margin-top:16px}
.story{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 18px 8px}
.shead{display:flex;align-items:flex-start;gap:12px}
.num{flex:0 0 auto;width:34px;height:34px;border-radius:9px;background:var(--gold);color:#1a1400;font-family:'Arial Black',sans-serif;font-weight:900;font-size:15px;display:flex;align-items:center;justify-content:center}
.shead .meta{min-width:0;flex:1}
.shead .tag{font-size:11px;font-weight:800;letter-spacing:1.3px;text-transform:uppercase;color:var(--gold)}
.shead h3{font-size:16.5px;color:var(--ink);font-weight:800;margin:1px 0 2px}
.target{margin:12px 0 14px;background:var(--tgt);border:1px solid var(--line);border-radius:9px;padding:8px 12px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:13px}
.target .lbl{font-size:10.5px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;color:var(--navy)}
.target .q{font-family:'Consolas','SF Mono',monospace;font-weight:700;color:var(--ink)}
.target .cnt{margin-left:auto;font-size:11px;font-weight:800;color:var(--muted);white-space:nowrap}
.panels{display:grid;gap:11px;border-top:1px dashed var(--line);padding-top:12px}
.panel{display:grid;grid-template-columns:26px 1fr;gap:12px;align-items:start}
.panel .pn{font-family:'Arial Black',sans-serif;font-weight:900;font-size:13px;color:#fff;background:var(--navy);width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-top:2px}
.panel .cap{font-weight:700;font-size:14.5px}
.panel .bub{display:inline-block;margin-top:5px;background:var(--chip);border:1px solid var(--gold);color:var(--ink);font-size:13.5px;font-style:italic;padding:4px 11px;border-radius:14px 14px 14px 3px}
.panel .art{display:block;margin-top:6px;font-size:12px;color:var(--muted)}
.panel .art b{color:var(--gold);font-style:normal;letter-spacing:.5px}
footer.end{margin-top:48px;border-top:2px solid var(--line);padding-top:18px;color:var(--muted);font-size:12.5px}
@media(max-width:560px){.wrap{padding:26px 14px 56px}}
"""

parts=[f"<style>{CSS}</style>","<div class='wrap'>",
 "<header class='top'><div class='kick'>JAIN Online &middot; Demand-Driven Landing Pages</div>",
 "<h1 class='display'>50 Landing-Page Stories</h1>",
 "<p>Each page is aimed at a <b>real, high-volume search query</b> from the terms report (query &amp; count shown on every card). Same converting arc &mdash; <b>dream &rarr; the wall &rarr; the JAIN Online reveal &rarr; the win</b> &mdash; with the wall/reveal tuned to the query's intent (fees, online, distance, best/recognised, eligibility, specialisation).</p>",
 "<div class='legend'>"]
for c in order: parts.append(f"<b>{e(c)} <span>{len(groups[c])}</span></b>")
parts.append("</div></header>")

n=0
for c in order:
    parts.append(f"<h2 class='course'>{e(c)} <span class='cnt'>{len(groups[c])} PAGES</span></h2><div class='grid'>")
    for (course,angle,query,count,who,panels) in groups[c]:
        n+=1
        parts.append("<article class='story'>")
        parts.append(f"<div class='shead'><div class='num'>{n:02d}</div><div class='meta'>"
                     f"<div class='tag'>{e(course)} &middot; {e(angle)}</div><h3>{e(who)}</h3></div></div>")
        parts.append(f"<div class='target'><span class='lbl'>&#127919; Target query</span>"
                     f"<span class='q'>{e(query)}</span><span class='cnt'>{count} in report</span></div>")
        parts.append("<div class='panels'>")
        for i,(cap,bub,art) in enumerate(panels,1):
            parts.append(f"<div class='panel'><div class='pn'>{i}</div><div><div class='cap'>{e(cap)}</div>"
                         f"<div class='bub'>&ldquo;{e(bub)}&rdquo;</div>"
                         f"<span class='art'><b>ART</b> &nbsp;{e(art)}</span></div></div>")
        parts.append("</div></article>")
    parts.append("</div>")
parts.append(f"<footer class='end'>{n} demand-driven stories &middot; 7 courses &middot; each mapped to a real query from the search-terms report. Counts are query occurrences in the report. Ready to build on the locked template.</footer></div>")
pathlib.Path("STORIES-50.html").write_text("\n".join(parts),encoding="utf-8")
print("wrote STORIES-50.html with", n, "stories")
