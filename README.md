# دليل مشروع موقع البورتفوليو — محمد الراشد
# Portfolio Website — Project Guide (Mohammed Alrashed)

> هذا الدليل يشرح المشروع كاملًا، ليتمكن أي شخص أو أي أداة ذكاء اصطناعي من التعديل عليه لاحقًا.
> This guide explains the whole project so anyone (a developer or any AI tool) can continue it.

---

## 1) Live links / الروابط
| What | Link |
|---|---|
| Live site (main) | https://malrashed.vercel.app |
| Backup (GitHub Pages) | https://mido19941414-ai.github.io/malrashed-portfolio/ |
| Source repository | https://github.com/mido19941414-ai/malrashed-portfolio |
| Hosting dashboard | https://vercel.com (project name: `malrashed`, account: mido19941414-ai) |

- Hosting is **free** (Vercel Hobby plan). No domain or server costs.
- Vercel's GitHub app has access to **this repository only**.
- **Any change pushed to the `main` branch goes live automatically within ~30 seconds.**

---

## 2) Folders on the computer (~/Documents) / المجلدات
| Folder | Purpose |
|---|---|
| `portfolio-website/` | Clean site with organized folders (`index.html` + `assets/…`). Open `index.html` to preview locally. |
| `portfolio-website-source/` | **Editable source**: `index.src.html` (template), `svgs.json` (exact tube positions), `build.py`, this guide. |
| `portfolio-deploy/` | The exact flat copy that is uploaded to GitHub (all files in one folder). |

The GitHub repo = the contents of `portfolio-deploy/` (flat: no sub-folders).
Flat naming used in the repo:
- `w-*.webp` → work images (logos, social posts, phones, reports, photography)
- `t01…t19.webp` → the 3D glass tubes
- `ttl-*.webp` → chapter title artwork (PORTFOLIO, LOGOS, SOCIAL MEDIA, REPORT, OTHER PROJECTS, THANK YOU)
- `me-*.webp` → personal photos
- `thmanyahsans-*.otf` → Thmanyah Sans font (all weights)
- `bg-streaks.webp`, `qr.png`, `og.jpg`

---

## 3) How to edit / طريقة التعديل

### A) Quick text or link change (easiest)
1. Open the repo on GitHub → click `index.html` → pencil icon (Edit).
2. Change the text, then **Commit changes** to `main`.
3. The live site updates automatically.

### B) Add or replace an image
1. Export as **.webp** (≈1600px max side, quality ~80).
2. Name it with the flat convention (e.g. `w-newclient-1.webp`).
3. GitHub repo → **Add file → Upload files** → commit to `main`.
4. Reference it in `index.html` (see section 5).

### C) Full rebuild from source (for developers / AI)
1. Edit `portfolio-website-source/index.src.html` (paths there use `assets/work/…`, `assets/tubes/…`).
2. Run `python3 build.py` → writes `portfolio-website/index.html` (injects tube scenes from `svgs.json`).
3. Flatten paths for deploy: replace `assets/work/`→`w-`, `assets/titles/`→`ttl-`, `assets/tubes/`, `assets/photos/`, `assets/fonts/`, `assets/` → `` (empty).
4. Upload the resulting `index.html` (and any new images) to the repo `main` branch.

---

## 4) Design system / نظام التصميم
- **Source material:** two portfolio PDFs (June 2026 dark/neon version + 2025 update). All content came from them.
- **Style:** the designer's own style — heavy headline + very light sub-line (weight contrast), cyan section labels, pink item labels, glassmorphism cards, glow on headlines, kashida in Arabic chapter titles.
- **Colors:** background `#03030f`; blue `#1219FF`; navy `#01087A`; cyan `#1AE4F6`; violet `#7B2CFF`; magenta `#E43CF5`.
- **Font:** **Thmanyah Sans** (ثمانية) for Arabic and English, weights Light/Regular/Medium/Bold/Black (files in the repo).
- **Tubes:** the 3D glass tubes are placed at the **exact coordinates from the PDF**, including the "weave" (a tube passing behind and in front of title letters / behind the head in the photos). This is done with SVG: a back copy + a front copy clipped by the original PDF clip path. Positions live in `svgs.json` (built by `scenes.py` + `build_svg.py` from the PDF).
- **Chapter titles** (PORTFOLIO, LOGOS, …) are the designer's original English artwork; in Arabic mode an Arabic title appears under each one.

---

## 5) Page structure / أقسام الصفحة (in order)
1. Hero — PORTFOLIO 2026 (woven tubes)
2. File contents (5 links)
3. About me (photo wrapped by tube) + stats (16+ years, 13 logos, 57+ social designs)
4. Toolkit (Photoshop / Illustrator / InDesign — Professional; AI tools — Good)
5. **LOGOS** chapter → Tajareb identity → Ertekaz identity → Single logos grid (11 logos)
6. **SOCIAL MEDIA** chapter → NAQSH · MAWANI (+ square series) · Roads Association · Year of the Camel 2024 · National & religious occasions · Brands & campaigns · Talent Management in Al-Baha
   - Rails are built by JavaScript from attributes, e.g. `data-set="naqsh1:4,naqsh2:5"` (files `w-naqsh1-1.webp`…) or `data-ph="8,15,13"` (phone mockups `w-phone-08.webp`…). **To add a post, add the file and extend the list.**
7. **REPORT** chapter → SANS annual report · Al-Bait Guests · Ithraa Al-Jood · More publications (5 books)
8. **OTHER PROJECTS** → Key photographer at the RSSA Annual Conference
9. **THANK YOU** → Contact (phone, email, social icons, Linktree, QR)

### Bilingual system
- Every translatable element has its English text inside the tag and Arabic in `data-ar="…"`.
- The language button swaps them and switches the page to RTL. The choice is remembered per visitor.

### Contact links (edit in the `SOCIALS` list inside the `<script>`)
WhatsApp `wa.me/966547455141` · Email `mido19941414@gmail.com` · Instagram `int.e5` · LinkedIn `mohammed-alrashed-9b28a6235` · Snapchat `int.e93` · TikTok `@int.e93` · X → Linktree (no X username given yet) · Linktree `linktr.ee/malrashed`.

---

## 6) Animations / الحركة
Loader · large tubes slide in from the edges and drift with scroll + mouse · woven small tubes float in sync · titles glow · headline words rise one by one · portraits rise into focus, rotating color glow behind, light sweep, 3D tilt · work images slowly zoom + shine on hover · logos pop then float · phones bob in a wave · social rails auto-scroll (pause on hover) · report books float + 3D tilt · glass cards with moving border light · counters, skill bars, marquee · custom cursor (desktop) · magnetic buttons · full-screen image viewer · respects "reduce motion".

---

## 7) History / سجل المشروع
- 2026-11-22: Built from the two portfolio PDFs; preview approved.
- 2026-11-23: Launched on Vercel (`malrashed.vercel.app`) + GitHub Pages backup; added direct contact links; Arabic copy rewritten in natural Arabic (not literal translation).
