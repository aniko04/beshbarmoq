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
- **Sections 2, 3, 5, 6, 7 are admin-driven.** They all render `bolim.html` through the `_bolim()` helper in `home/views.py`; content comes from the `Material` model (`section`, `title`, `summary`, `body`, `file`, `link`, `manba`, `order`, `is_published`). To add a section, add a choice to `Material.SECTION_CHOICES` and a thin view calling `_bolim()`. Empty sections render a designed empty state, with an "add material" link for staff.
- **Section 1 (`haqida.html`) is hand-written** — author bio, ta'lim/faoliyat timeline and publications are filled in from the client's public BuxDPI profile. The author photo is optional: drop a file at `media/muallif.jpg` and the view's existence check swaps the motif placeholder for the image. The page ends with a `#portfolio` band holding a PDF from `media/hujjatlar/`; its inline viewer sets the `<iframe>` `src` only on first click, so the file isn't fetched on page load — keep that if you add more documents.
  - Client PDFs are Canva exports, which store **photographs as PNG** and blow the file up ~7×. Recompress before serving: `doc.rewrite_images(dpi_threshold=170, dpi_target=150, quality=88)` in PyMuPDF took the portfolio from 57.7 MB to 7.9 MB with the lowest page PSNR at 41 dB (visually identical, QR codes still decode). Originals stay in `malumotlar/`.
- Nav highlighting: each view passes `active` (e.g. `'maqola'`) and `base.html` compares it per link.

### Design system (`static/css/platform.css`)

Palette is drawn from Uzbek textile dyes rather than generic UI blue: `--siyoh` (indigo, the dominant chrome), `--anor` (pomegranate), `--zafaron` (saffron), `--firuza` (turquoise), over white/`--stone` surfaces. Type is **Bitter** (slab serif, display) + **Karla** (body). The `#palak` rosette is the one signature element — brand mark, eyebrow marker, card corner, empty state — so keep new decoration to a minimum.

Four rules worth knowing before you edit it:
- Link colour is scoped to `.prose a` / `.material-body a` **on purpose**. An earlier global `.pf a { color: … }` out-specified `.btn`, `.bolim-card` and `.brand` (all single-class selectors) and tinted every button and card title. Don't reintroduce it.
- Photographic backgrounds sit on `::before` at `z-index: -2` with a scrim on `::after` at `-1`, under `isolation: isolate`. Hero/`page-head` images live in `static/img/` (`hero-qogoz.jpg`, `sinf.jpg`, `qollar.jpg`).
- Global text scale is `html { font-size: 108% }` — a percentage, not px, so the browser's own font-size setting still applies. Everything else is in `rem`, so bump that one number rather than editing sizes one by one.
- **The navbar is deliberately two rows** (`.nav { order: 3; width: 100% }`): brand + auth on top, the seven section links below. Seven long Uzbek labels plus brand and auth need ~1350px on one row; the content `--wrap` is 1200px, which is why the old single-row bar was stuck at `font-size: 0.85rem`. Don't "fix" it back to one row without shrinking the labels. Below 1060px it collapses to the hamburger as before. `.muallif-card`'s sticky `top` is tuned to the taller bar.

### Exercise pages

The 10 exercises are unchanged and keep their own look: they load `static/css/style.css` (the vivid kids' theme with `.t-*` classes) and do **not** extend `base.html`. Their `.back-link` points at `/multimediya`, not `/`. The `talaba_required` decorator also bounces to `/multimediya`.

**Every page is a function view in `home/views.py` that renders one template.** There is no client-side framework and no JS build step. To add or change a page you touch three places in lockstep:
1. Template in `templates/` (or `templates/oquvchi/`)
2. A `render(...)` view in `home/views.py`
3. A `path(...)` route in `core/urls.py`

Running `manage.py check` after route/view edits catches most mistakes.

**Exercise structure:**
- **Exercises 1–5** — interactive games, open to everyone. One template each (`mashq1.html`…`mashq5.html`) plus a matching `static/js/mashqN.js` / `static/css/mashqN.css`.
- **Exercises 6–10** — three stages each: **video → test → crossword**, as templates `mashqNa.html` (video), `mashqNb.html` (test), `mashqNc.html` (crossword). The quiz and crossword logic live **inline in a `<script>` inside each HTML file** — not in external JS. (`static/js/mashqNb.js` files exist but the canonical logic is inline.)

**Roles & gating** (`home/models.py` → `Profile`, roles `oquvchi` / `talaba`):
- `talaba` (or `is_staff`) sees the teacher pages at `/mNa`, `/mNb`, `/mNc`, protected by the `@talaba_required` decorator in `home/views.py`.
- `oquvchi` sees pupil pages at `/oNa`, `/oNb`, `/oNc` rendering `templates/oquvchi/mNx.html` — these are **not** gated.
- `templates/multimediya.html` picks the link per card via the `show_advanced` context flag (`= is_talaba(user)`): `{% if show_advanced %}/m6a{% else %}/o6a{% endif %}`.
- Pupil versions of exercises 6–10 are all complete (video → test → crossword for each). See `OQUVCHI_QOLLANMA.md` for the full step-by-step of adding/extending a pupil exercise (including crossword grid data format and digraph cells like `CH`/`SH`/`G'`/`O'`) — note it still describes exercise 9 as video-only, which is now out of date.

**Results:** completing a test POSTs to `/api/save-result` (`save_result` view, login-required). It writes a `Result` row keyed by `mashq` (e.g. `'m8b'`); a result counts as passed only at 100% (`Result.save`). Any new test key must be added to `Result.MASHQ_CHOICES` in `home/models.py` or the save fails.

## Conventions & gotchas

- **Framing media needs `xframe_options_sameorigin`.** `XFrameOptionsMiddleware` stamps `X-Frame-Options: DENY` on *every* response, including `serve()`ing a PDF from `media/`. An `<iframe>` pointing at it then fails with Chrome's misleading "127.0.0.1 refused to connect" — which looks like a dead server, not a header. The media route in `core/urls.py` is wrapped in `xframe_options_sameorigin` for exactly this; everything else stays `DENY`.
- **Static/media URLs are hardcoded absolute paths** (`/static/css/style.css`, `/media/Video1.mp4`) — the templates deliberately do **not** use `{% static %}`. Because of this WhiteNoise is configured to compress but not hash static files (`CompressedStaticFilesStorage`, see `core/settings.py`). Media is served at runtime via a `serve()` route at the bottom of `core/urls.py`.
- **Per-exercise theming:** design tokens are CSS custom properties in `:root` and theme classes `.t-orange`, `.t-blue`, `.t-rose`, `.t-indigo`, `.t-coral`, `.t-emerald`, etc. in `static/css/style.css`. Each exercise page sets `<body class="t-...">` to recolor. Exercise→theme map: 6=`t-blue`, 7=`t-rose`, 8=`t-indigo`, 9=`t-coral`, 10=`t-emerald`. Design direction is a vivid, premium, full-color kids' aesthetic — avoid plain white.
- **URL routing** in `core/urls.py` keeps three parallel schemes for each exercise: short (`/m6a`), legacy (`/mashq6a.html`), and pupil (`/o6a`). Keep them consistent when adding routes.
- **`namuna/`** holds source/working files (Word docs + raw crossword HTML) used to author exercises; it is not part of the running app.
- `SECRET_KEY` is committed and `DEBUG=False`; `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` list the production domains (aniko.uz, texnoedu.uz, vibe-coder.uz, verbatum.xyz). This is a small self-hosted deployment, not a 12-factor setup.
