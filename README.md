# JAIN Online - 50 Comic Landing Pages

Comic / Webtoon-style landing pages for JAIN Online, one per Google Ads search theme, across
all 7 programmes (MBA, BBA, MCA, BCA, B.Com, M.Com, MA) plus 4 university/brand pages.

- **Live site:** https://jain-comic-pages.vercel.app
- **Google Ads index:** [`GOOGLE-ADS-INDEX.md`](GOOGLE-ADS-INDEX.md) - every page mapped to its
  target search query, Final URL and search demand.
- Every CTA opens the **Sensei** chat counsellor directly
  (`sensei.onlinejain.com/?chat=1&from_partner=jain-online&entry=partner_marketing&landing=jain_online_landing_v2`).

Pages, specialisations and fees are evidence-based: specialisations verified against the live
AMS/UMS grid, fees from live PMS, page selection from real Google Ads search demand.

## Deploy (Vercel)

`web/` is the deploy root. Clean URLs like `/mba/finance`, `/jain/online`, `/ma/english`.

```
py -3.12 build_web.py                     # rebuild web/ from share/ + stories/
vercel deploy --prod --yes --cwd web
```

## Rebuild the pages

```
py -3.12 make_mba_stories.py   # (+ make_bba/mca/bcom/more/jain_stories.py) -> stories/*.json
py -3.12 gen_mba_art.py        # (+ the other gen_*_art.py) -> pages/img/*.jpg  [GEMINI_API_KEY in .env.local]
py -3.12 build.py              # stories/*.json -> pages/*.html  (programme-aware theme)
py -3.12 pack_all.py           # pages -> share/*.html  (self-contained: images + fonts embedded)
py -3.12 build_web.py          # share -> web/ + index.html + GOOGLE-ADS-INDEX.md
```

## Layout

| Path | What |
|------|------|
| `web/<programme>/<slug>.html` | 50 self-contained landing pages (Vercel Final URLs) |
| `web/index.html` | hub linking all 50 |
| `stories/*.json` | per-page content (hero, 4 panels, fees, testimonials, CTA) |
| `pages/` + `pages/img/` | built pages + generated art |
| `build.py` | template engine (programme-aware: MBA/MCA/B.Com/M.Com/MA/BCA/JAIN/BBA) |
| `make_*_stories.py` / `gen_*_art.py` | per-programme content + art generators |
| `map_all_impr.py` | routes every search query to its page |
| `ALL-50-LP-SUMMARY.csv` / `SEARCH-QUERIES-ALL-50.csv` | demand rollup + full query mapping |

## Standards
- Correct, brand-safe English; complete beginning-middle-end across the 4 panels.
- Hero/art on-theme, character-consistent, no baked-in text; no em/en dashes (`sanitize()` enforces).
- Fees verified from live PMS; specialisations from live UMS. `.env.local` (keys) is git-ignored.
