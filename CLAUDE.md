# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Django 6.0 web app: an Uzbek-language **methodological e-platform** ("Inkorporatsion topshiriqlar") built around a dissertation on teaching primary-school technology (handicraft) via an *inkorporatsion* approach. UI text, code comments, and model `verbose_name`s are in Uzbek — match that language when writing user-facing strings.

Two audiences share one site: **teachers/researchers** (the outer shell — seven methodological sections) and **children** (the 10 interactive exercises, which now live inside the *Multimediya* section).

## Commands

The project runs against the checked-in virtualenv at `env/` (Windows). Invoke Python directly through it:

```bash
env/Scripts/python.exe manage.py runserver      # dev server
env/Scripts/python.exe manage.py check          # validate config (run after editing views/urls)
env/Scripts/python.exe manage.py makemigrations
env/Scripts/python.exe manage.py migrate
env/Scripts/python.exe manage.py collectstatic  # into staticfiles/ (WhiteNoise compresses)
env/Scripts/python.exe manage.py createsuperuser
```

There is no automated test suite — `home/tests.py` and `temp/tests.py` are empty boilerplate. Verify changes by running the server and exercising the affected flow in the browser.

Note: `DEBUG = False` even in development (`core/settings.py`). WhiteNoise serves static files, so `runserver` works without extra config.

**Two gotchas that will waste your time if you forget them:**
- Because `DEBUG = False`, Django uses the **cached template loader**. Editing a `.html` file has *no effect until you restart the server* — the autoreloader does not clear the template cache. CSS/JS edits do take effect (after `collectstatic`), which makes the staleness easy to misdiagnose.
- WhiteNoise indexes `staticfiles/` **once, at startup**. A file that appears there afterwards (a new stylesheet, a new image folder, a throwaway page you dropped in) **404s until the server restarts** — so a brand-new page can render as unstyled text with broken images while the old assets keep working. If a page suddenly looks like raw HTML, suspect this before touching the CSS. A missing stylesheet also lets inline `<svg>` icons render at their intrinsic size, i.e. enormous — give icons explicit `width`/`height` attributes so that failure mode stays cosmetic.
- Editing templates from PowerShell with `Set-Content -Encoding UTF8` writes a **UTF-8 BOM** (PS 5.1 behaviour), which then leaks in front of `<!DOCTYPE html>`. Use the `Edit`/`Write` tools, or `[System.IO.File]::WriteAllText` with `UTF8Encoding($false)`.

## Architecture

**Apps:** `core` (settings/urls/wsgi), `home` (everything real), `temp` (empty — ignore it).

### The platform shell (seven sections)

`templates/base.html` is the shell for every non-exercise page: sticky navbar, the seven sections, footer, and an inline SVG sprite holding the two signature motifs (`#palak` — a suzani rosette; `#orama` — a quilling spiral). Its stylesheet is `static/css/platform.css`, a self-contained design system that deliberately **does not** load `style.css`.

| # | Section | URL | Template | View |
|---|---------|-----|----------|------|
| 1 | O'zim haqimda | `/haqida` | `haqida.html` | `haqida` |
| 2 | Metodika | `/metodika` | `bolim.html` | `metodika` |
| 3 | Maqola | `/maqola` | `bolim.html` | `maqola` |
| 4 | Multimediya | `/multimediya` | `multimediya.html` | `multimediya` |
| 5 | Topshiriq | `/topshiriq` | `bolim.html` | `topshiriq` |
| 6 | Instruksion texnologik xarita | `/xarita` | `bolim.html` | `xarita` |
| 7 | Dars ishlanmalar | `/ishlanma` | `bolim.html` | `ishlanma` |

- The landing page (`/`, `templates/index.html`) is the platform pitch: hero, the seven-section grid, the "Platforma haqida" article. It is **not** the exercise list any more.
- **Sections 2, 3, 5, 6, 7 are admin-driven.** They all render `bolim.html` through the `_bolim()` helper in `home/views.py`; content comes from the `Material` model (`section`, `title`, `summary`, `body`, `file`, `muqova`, `link`, `manba`, `order`, `is_published`). To add a section, add a choice to `Material.SECTION_CHOICES` and a thin view calling `_bolim()`. Empty sections render a designed empty state, with an "add material" link for staff. **Add materials as `Material` rows, never as hand-written HTML in `bolim.html`** — the admin-managed flow is the client's explicit choice.
  - `muqova` is an optional cover image (`FileField`, **not** `ImageField` — Pillow is not installed in `env/`, and `ImageField` would fail `manage.py check`). Filled in → the card shows a book cover; empty → the old file-extension badge. Covers for PDFs are rendered from page 1 with PyMuPDF at 460px wide, JPEG q82 (~20 KB), into `media/materiallar/muqova/`.
  - Materials with a viewable PDF (`Material.koruv_url`) get a **"Ko'rish"** button that reveals an inline `<iframe>`; its `src` is set on first click so a 10 MB book is not fetched on page load. One delegated click handler in `bolim.html` covers every card. `koruv_url` returns `file` when it is a PDF, otherwise the optional **`koruv`** field — a PDF rendition of a Word file, since browsers can't frame `.doc`/`.docx`. "Dars ishlanmalar" is all Word, so each row has a `koruv` PDF in `media/ishlanmalar/koruv/` while "Yuklab olish" still hands over the editable original. Word itself does the conversion (`Word.Application` COM → `ExportAsFixedFormat($out, 17)`); LibreOffice is not installed.
  - **Sub-sections (`Material.kichik_bolim`)** — a section can split its materials into collapsible `<details>` groups. Only **Topshiriq** uses this so far: *Rasmli test* and *Texnologik diktantlar*, from `Material.KICHIK_BOLIM_CHOICES`, wired up by passing `guruhlash=` to `_bolim()`. The groups always render, even while empty, so the page doesn't change shape as the client fills them; a material with a blank `kichik_bolim` falls back to a flat card above the groups. The card markup itself lives in the `templates/_material.html` partial, included from both the flat list and each group — edit it there, not in `bolim.html`.
    - **«Rasmli test» is a real interactive test page**, not just a file list: `/topshiriq/rasmli-test` → `rasmli_test_sahifa` → `templates/rasmli_test.html` + `static/css/rasmli-test.css`. Questions and the answer key live in **`home/rasmli_test.py`** (15 tasks, 33 answer rows × 5 points = 165, 20-minute timer) — built from `malumotlar/topshiriqlar/Rasmli test.docx`, whose 45 pictures were extracted to `static/img/rasmli-test/sNN{a,b,s}.jpg` (task 13's multi-tool options are composited into one tile each). Four rules decide how a picture looks, each learned the hard way: (1) alpha must be flattened onto white or transparent PNGs render **black**; (2) **quality is per-content** — Word's own JPEGs are copied byte-for-byte, PNG photos go q92, and clipart/line art goes **q97 with `subsampling=0`**, because plain q82 visibly mangles flat colour; (3) **never upscale** — every source is 180–320px, so `.rt-variant-rasm` is a fixed-height white box and the `<img>` sits at its natural size inside it (`width:auto; max-width/height:100%`), which is why it looks sharp; (4) **every file is `.jpg`, deliberately** — an earlier pass wrote clipart as `.png`, so regenerating the images silently changed five URLs and the running server served 404s for them. The filename must depend only on question number and letter. `home/apps.py` registers a system check (`home.W001`) that fails `manage.py check` when any of the 45 files is missing, so a broken extraction can't reach the page unnoticed. Image URLs carry `?v=N` from `RASM_VERSIYA` — bump it whenever a picture is replaced under an existing name, or browsers keep showing the old one. The tiles also deliberately **do not** use `loading="lazy"`: the whole set is ~1 MB, and a tile that hasn't loaded yet is an unanswerable question. Two question shapes: single-answer (click a picture) and matching (3 pictures + N labelled rows, one A/B/S each). **The Word contains no answer key** — it was derived by looking at the pictures, so if the client disputes an answer, fix the letter in `_XOM` and nothing else. Scoring/timer are inline JS in the template (project convention); a logged-in user's result is POSTed to `/api/save-result` under the `rtest` key (added to `Result.MASHQ_CHOICES`). **The test opens behind a start gate** (`.rt-parda` + `.rt-boshla`): the page renders blurred under a modal, and only the "Boshlash" click hides it and calls `soatniBoshla()` — the timer no longer starts on the first answer, so a child who leaves the page open doesn't lose time. The blur is `backdrop-filter` on the overlay, **never `filter` on the content** — a `filter` on an ancestor makes it the containing block for `position: fixed`/`sticky`, which would tear the navbar, the sticky panel and the floating clock out of place. Note the gate is unrecoverable if the inline JS dies (see the Google Fonts rule below); that is deliberate — failing visibly beats letting a pupil answer 33 questions into a dead "Tekshirish" button. **Leaving mid-test is also guarded**: while `soatId !== null && !tekshirildi`, a capture-phase click handler `confirm()`s before following any link (navbar "Chiqish" included) and `beforeunload` covers tab-close/reload. The two share a `chiqishgaRuxsat` flag so a confirmed exit isn't asked twice; both go quiet once `tekshir()` has run, because only then has the score been POSTed anywhere. A group can advertise such a page via `_bolim(..., ilova={kalit: {...}})`, which renders the indigo `.guruh-ilova` call-to-action above that group's materials.
    - The **navbar "Topshiriq" item is a hover menu** listing the same two sub-sections (`base.html` → `.nav-item` / `.nav-menu`, CSS-only: `:hover` + `:focus-within`, no JS). "Rasmli test" links straight to the test page; "Texnologik diktantlar" still points at the accordion group (`/topshiriq#diktant`) until that half is built.
      Anchor plumbing for the group links: each `<details>` carries `id="{{ g.kalit }}"`, and a small script in `bolim.html` opens the targeted group on load *and* on `hashchange` (needed because a `<details>` doesn't open from a hash on its own, and because clicking the menu while already on the page only changes the hash). `.guruh` has `scroll-margin-top: 94px` so the sticky navbar doesn't cover the summary. Below the 1365px hamburger breakpoint the panel goes `position: static` and the two entries simply sit indented under "Topshiriq" — there is no hover on touch.
  - Two traps that bit during this work, both silent: (1) `.material.has-muqova` **must** declare explicit `grid-template-columns` — with `auto` in the first column, Chrome sizes it to the `alt` text before the image decodes and crushes the text column to zero width; and it needs re-declaring inside the 660px media query, since `.material` alone loses on specificity. (2) `{# … #}` is **single-line only** in Django — a multi-line one renders as visible page text.
- **Section 1 (`haqida.html`) is hand-written** — author bio, ta'lim/faoliyat timeline and publications are filled in from the client's public BuxDPI profile. The author photo is optional: drop a file at `media/muallif.jpg` and the view's existence check swaps the motif placeholder for the image. The page ends with a `#portfolio` band holding a PDF from `media/hujjatlar/`; its inline viewer sets the `<iframe>` `src` only on first click, so the file isn't fetched on page load — keep that if you add more documents.
  - Client PDFs are Canva exports, which store **photographs as PNG** and blow the file up ~7×. Recompress before serving: `doc.rewrite_images(dpi_threshold=170, dpi_target=150, quality=88)` in PyMuPDF took the portfolio from 57.7 MB to 7.9 MB with the lowest page PSNR at 41 dB (visually identical, QR codes still decode). Originals stay in `malumotlar/`.
- Nav highlighting: each view passes `active` (e.g. `'maqola'`) and `base.html` compares it per link.

### Design system (`static/css/platform.css`)

The **logo** is the client's circular craft emblem, kept in `logo/` as the original JPG and published as `static/img/logo.png` (256px, white background flood-filled to alpha, PNG-8 ≈ 34 KB). It is the brand mark in the navbar and footer (`.brand-logo`) and the source of the favicons (`favicon.ico` 16/32/48, `favicon-32.png`, `apple-touch-icon.png` — all three linked from every template's `<head>`, including the standalone exercise pages, which do not extend `base.html`). Regenerating: Pillow is **not** in `env/` — run image scripts on system Python (`py -3.11`), same as PyMuPDF. `#palak` is still the decorative motif everywhere else; it is just no longer the logo.

Palette is drawn from Uzbek textile dyes rather than generic UI blue: `--siyoh` (indigo, the dominant chrome), `--anor` (pomegranate), `--zafaron` (saffron), `--firuza` (turquoise), over white/`--stone` surfaces. Type is **Bitter** (slab serif, display) + **Karla** (body). The `#palak` rosette is the one signature element — brand mark, eyebrow marker, card corner, empty state — so keep new decoration to a minimum.

Four rules worth knowing before you edit it:
- Link colour is scoped to `.prose a` / `.material-body a` **on purpose**. An earlier global `.pf a { color: … }` out-specified `.btn`, `.bolim-card` and `.brand` (all single-class selectors) and tinted every button and card title. Don't reintroduce it.
- Photographic backgrounds sit on `::before` at `z-index: -2` with a scrim on `::after` at `-1`, under `isolation: isolate`. Hero/`page-head` images live in `static/img/` (`hero-qogoz.jpg`, `sinf.jpg`, `qollar.jpg`).
- Global text scale is `html { font-size: 108% }` — a percentage, not px, so the browser's own font-size setting still applies. Everything else is in `rem`, so bump that one number rather than editing sizes one by one.
- **The navbar is one row and sized to the millimetre.** Seven long Uzbek labels + brand + auth barely fit, so the sizes come from *measuring*, not from eye. The binding case is a **logged-in** user with a long name — `.nav-user` + "Chiqish" add ~199px that the logged-out view never shows, so always check both. Three things move together: `.topbar .wrap`'s `max-width: 1340px` (wider than the 1200px content `--wrap` on purpose), the hamburger breakpoint, and `.nav a`'s font-size/padding (with `.nav { gap: 0 }`). Enlarge any of them and the breakpoint has to rise too, or "Chiqish" gets clipped by `overflow-x: hidden`.
  - **The size is a four-step ladder, not one number.** `0.94rem` is only the *base* step, chosen for the 1366px laptop; on a wide monitor that left the labels looking tiny against empty gutters, so `min-width` queries scale the whole navbar up. Each step raises `.topbar .wrap`'s `max-width` **together with** the font sizes — bump the font alone and the links stay crushed into 1340px and wrap to a second row.

    | Viewport | `.nav a` | `.wrap` max-width | measured content | needs |
    |---|---|---|---|---|
    | ≤1279px | hamburger | — | — | — |
    | 1280–1365px | 0.88rem / 7px | 1340px | — | — |
    | 1366–1449px | 0.94rem / 7px | 1340px | 1325px | 1340px |
    | 1450–1559px | 1.00rem / 9px | 1420px | 1411px | 1426px |
    | 1560–1659px | 1.06rem / 11px | 1510px | 1502px | 1517px |
    | ≥1660px | 1.12rem / 13px | 1600px | 1594px | 1609px |

    "Measured content" is the `.wrap` box width **including its own 56px padding**; "needs" adds ~15px for the scrollbar. Every step keeps 25–50px of slack. Note the older figures in this file (1279px for 0.94rem, "+48px") were *ink* spans from pixel-scanning, which exclude that padding — don't mix the two conventions or you will double-count.
  - **Measuring without a browser session or a running page:** give a throwaway page `.topbar .wrap { max-width: none; width: max-content }`, stack one navbar copy per candidate size, and load it over `file://` in headless Chrome — no server, no `staticfiles/` restart dance. Two ways to read the number back, both used here:
    - *Preferred:* let page JS `await document.fonts.ready`, then read `getBoundingClientRect().width` and print it into the DOM. Exact, sub-pixel, and it can assert `document.fonts.check('600 1rem Karla')` — **if the fonts fell back, every width is wrong**, so check this before trusting a run.
    - *Pixel scan:* screenshot, then in Pillow (`py -3.11`) find the left/right-most pixel differing from `--siyoh` (#14203A). Skip the band's top/bottom few rows or the 1px `border-bottom` reads as full-width content. Good for verifying the *shipped* breakpoints: render at each width and check the dark band stays exactly **74px tall** — a second row is the failure this whole section exists to prevent.
    - `--dump-dom` exits 21 with empty output if `--user-data-dir` is a relative path; pass an absolute Windows path. `--screenshot` works either way.
  - Beware when screenshotting: a *fresh* `--user-data-dir` has no font cache — if the network is down, `fonts.googleapis.com` stalls and `load` never fires, so anything keyed to `window.onload` (including page JS you're trying to test) silently never runs. The user's own Chrome usually holds a lock on the default profile, so a throwaway profile is the only option.
  - Renaming a nav label re-opens this. "Instruksion xarita" → "Instruksion texnologik xarita" alone cost +88px, which is what forced `.nav a` down from `0.92rem`/`9px 9px`. To measure without guessing: drop a throwaway page into `staticfiles/` with the logged-in navbar markup wrapped in a `width: 1280px` box, and screenshot it with headless Chrome (`--headless=new --window-size=1500,150 --screenshot=…`). Screenshotting at `--window-size=1280` directly is unreliable — the headless viewport comes out just under 1280 and the hamburger fires, which looks like an overflow bug but isn't.

### Auth pages

`login.html` and `register.html` are standalone (no `base.html`) but belong to the **platform** layer: they load `platform.css` + `static/css/auth.css` and use its tokens. They used to load the kids' `style.css`, which is why they were violet/pink — if either page ever looks off-brand again, check which stylesheet it links. `auth.css` is shared by both; the background uses the same `::before` image / `::after` scrim trick as `.page-head`.

### Exercise pages

The 10 exercises are unchanged and keep their own look: they load `static/css/style.css` (the vivid kids' theme with `.t-*` classes) and do **not** extend `base.html`. Their `.back-link` points at `/multimediya`, not `/`. The `talaba_required` decorator also bounces to `/multimediya`.

**Every page is a function view in `home/views.py` that renders one template.** There is no client-side framework and no JS build step. To add or change a page you touch three places in lockstep:
1. Template in `templates/` (or `templates/oquvchi/`)
2. A `render(...)` view in `home/views.py`
3. A `path(...)` route in `core/urls.py`

Running `manage.py check` after route/view edits catches most mistakes.

**Exercise structure:**
- **Exercises 1–5** — interactive games. `@login_required` but **not** role-gated: any signed-in user sees them. One template each (`mashq1.html`…`mashq5.html`) plus a matching `static/js/mashqN.js` / `static/css/mashqN.css`.
- **Exercises 6–10** — three stages each: **video → test → crossword**, as templates `mashqNa.html` (video), `mashqNb.html` (test), `mashqNc.html` (crossword). The quiz and crossword logic live **inline in a `<script>` inside each HTML file** — not in external JS. (`static/js/mashqNb.js` files exist but the canonical logic is inline.)
  - **Exercise 9 breaks the a/b/c pattern**: it has a *second* video page, `m9a2` / `o9a2` (`mashq9a2.html`, `oquvchi/m9a2.html`), routed in all three URL schemes. Anything that iterates the exercises mechanically will miss it.

**Roles & gating** (`home/models.py` → `Profile`, roles `oquvchi` / `talaba`):
- `talaba` (or `is_staff`) sees the teacher pages at `/mNa`, `/mNb`, `/mNc`, protected by the `@talaba_required` decorator in `home/views.py`.
- `oquvchi` sees pupil pages at `/oNa`, `/oNb`, `/oNc` rendering `templates/oquvchi/mNx.html` — `@login_required`, but **not** role-gated. In short: *every* exercise page requires login; only `/mNx` additionally requires the role.
- Gating failures go two different ways, which matters when debugging a redirect: no session → `LOGIN_URL = '/login'` with `?next=`; signed in but wrong role → straight to `/multimediya`, no message. `login_view`/`register_view` return to `next` through `_safe_next()`, which validates the host (open-redirect guard) — keep that if you touch the auth flow.
- `templates/multimediya.html` picks the link per card via the `show_advanced` context flag (`= is_talaba(user)`): `{% if show_advanced %}/m6a{% else %}/o6a{% endif %}`.
- Pupil versions of exercises 6–10 are all complete (video → test → crossword for each). See `OQUVCHI_QOLLANMA.md` for the full step-by-step of adding/extending a pupil exercise (including crossword grid data format and digraph cells like `CH`/`SH`/`G'`/`O'`) — note it still describes exercise 9 as video-only, which is now out of date.

**Results:** completing a test POSTs to `/api/save-result` (`save_result` view, login-required). It writes a `Result` row keyed by `mashq` (e.g. `'m8b'`); a result counts as passed only at 100% (`Result.save`). Any new test key must be added to `Result.MASHQ_CHOICES` in `home/models.py` or the save fails.

## Conventions & gotchas

- **Framing media needs `xframe_options_sameorigin`.** `XFrameOptionsMiddleware` stamps `X-Frame-Options: DENY` on *every* response, including `serve()`ing a PDF from `media/`. An `<iframe>` pointing at it then fails with Chrome's misleading "127.0.0.1 refused to connect" — which looks like a dead server, not a header. The media route in `core/urls.py` is wrapped in `xframe_options_sameorigin` for exactly this; everything else stays `DENY`.
- **Google Fonts must never be loaded with CSS `@import`.** `platform.css` used to start with one; an `@import` is a render-blocking stylesheet, so when `fonts.googleapis.com` is slow or blocked (school networks, offline dev) the page's inline `<script>` blocks never run — the Rasmli test froze with unclickable tiles and a dead "Tekshirish" button, which looks exactly like broken JS. The fonts now load from each `<head>` via `<link media="print" onload="this.media='all'">` (+`preconnect`, +a `<noscript>` fallback) in `base.html`, `login.html`, `register.html`. Same rule applies if `style.css` is ever touched — it still has an `@import` for the kids' fonts.
- **Static/media URLs are hardcoded absolute paths** (`/static/css/style.css`, `/media/Video1.mp4`) — the templates deliberately do **not** use `{% static %}`. Because of this WhiteNoise is configured to compress but not hash static files (`CompressedStaticFilesStorage`, see `core/settings.py`). Media is served at runtime via a `serve()` route at the bottom of `core/urls.py`.
  - **Consequence: a CSS edit can be invisible in the browser, and it does not look like a caching problem.** No hashing means the URL never changes, so a browser that has the old stylesheet keeps using it — the *new HTML* arrives while the *old CSS* styles it. The failure mode is a half-rendered page, not an obviously missing stylesheet: when the start modal was added to the Rasmli test, its markup appeared as unstyled text spilling over the header, which reads as broken HTML. Before debugging CSS that "doesn't apply", confirm the browser actually has the new file.
  - The fix in use is the same `?v=N` cache-buster the test images already use: `platform.css`, `auth.css` and `rasmli-test.css` are linked as `…css?v=2` from `base.html`, `login.html`, `register.html` and `rasmli_test.html`. **Bump that number in the same commit as the stylesheet edit** — WhiteNoise ignores the query string when finding the file, so the only thing it changes is the cache key.
  - Three separate caches sit between an edit and the screen, and they fail differently: the **template** cache (needs a server restart, `DEBUG=False`), **WhiteNoise's** startup index (needs a restart for *new* files), and the **browser** (needs `?v=` or a hard refresh). A change that seems to have had no effect is almost always one of these, not the edit.
- **Per-exercise theming:** design tokens are CSS custom properties in `:root` and theme classes `.t-orange`, `.t-blue`, `.t-rose`, `.t-indigo`, `.t-coral`, `.t-emerald`, etc. in `static/css/style.css`. Each exercise page sets `<body class="t-...">` to recolor. Exercise→theme map: 6=`t-blue`, 7=`t-rose`, 8=`t-indigo`, 9=`t-coral`, 10=`t-emerald`. Design direction is a vivid, premium, full-color kids' aesthetic — avoid plain white.
- **URL routing** in `core/urls.py` keeps three parallel schemes for each exercise: short (`/m6a`), legacy (`/mashq6a.html`), and pupil (`/o6a`). Keep them consistent when adding routes.
- **`malumotlar/`** holds the client's original source files (Word docs, uncompressed Canva PDFs) that the served material is derived from — e.g. `malumotlar/topshiriqlar/Rasmli test.docx`. It is **gitignored**, so it exists only on this machine: don't assume a future checkout can regenerate anything from it. `logo/` likewise keeps the original emblem JPG. Neither is part of the running app. (An older `namuna/` directory is gone.)
- **`staticfiles/`, `media/` and `db.sqlite3` are committed to git.** Consequences: `collectstatic` output must be committed alongside the `static/` edit that caused it or production serves the old asset; every uploaded `Material` file and every admin edit shows up as a repo diff. Expect a dirty tree after simply running the site.
- `SECRET_KEY` is committed and `DEBUG=False`; `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` list the production domains (aniko.uz, texnoedu.uz, vibe-coder.uz, verbatum.xyz, d-steam.uz). This is a small self-hosted deployment, not a 12-factor setup.
- `requirements.txt` covers only the runtime (Django, whitenoise, asgiref, sqlparse, tzdata) and is **UTF-16 encoded** — read it with an encoding-aware tool, and don't append to it from a shell redirect. Pillow and PyMuPDF are deliberately absent: the image/PDF scripts run on system Python (`py -3.11`), never in `env/`.
