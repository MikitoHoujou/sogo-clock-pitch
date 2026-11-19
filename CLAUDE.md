# Sogo Clock Wall pitch — how to edit

This repo is the Wild Tame pitch for the projection on the Sogo Yokohama clock wall. It is one
interactive page in English (`index.html`) and Japanese (`ja.html`). Teammates change it by
asking Claude. These rules keep the two languages in step and the page working.

## Files

- `src/page.html` — **the only file to edit.** The whole page: styles, content and script.
  It has no `<html>`/`<head>`/`<body>` tags; the build adds them.
- `i18n/ja.json` — list of `[English, Japanese]` text pairs. The build swaps each English
  string for its Japanese one, top to bottom, to make `ja.html`.
- `index.html`, `ja.html` — **built files. Never edit by hand**; run the build instead.
- `img/` — JPEG images the page uses.
- `tools/build.py` — the build.
- `TEAM-NOTES.md` — copied in from the Team Box on Claude. Don't edit by hand.

## Every change

1. `git pull` first, so you start from everyone's latest work.
2. Edit `src/page.html`.
3. Keep Japanese in step:
   - Changed English text → change the English side of its pair in `i18n/ja.json` to match
     exactly, and update the Japanese side.
   - New English text → add a pair. Put pairs for longer strings before pairs for short
     strings they contain, so the long one is replaced first.
   - Strings inside the page's JavaScript keep their quotes and `\'` escapes in the pair,
     exactly as they appear in the source.
   - Japanese copy: natural, polite business Japanese (です・ます), the way the rest of the page reads.
4. Run `python3 tools/build.py`. It must end with `not matched: 0` and both script checks `ok`.
   If a pair is not matched, the English text changed: fix the pair, don't delete it.
5. Look at both pages (open `index.html` and `ja.html` in a browser), English and Japanese.
6. Commit with a message that says what changed, then push.

## Page rules

- Keep the look: the `:root` colour and font tokens at the top of `src/page.html`, a bright
  page with SOGO blue as the one accent. Add new colours as tokens, not inline values.
- Directions live in the `DIRS` object in the script (keys `tactile`, `oddball`, `shadow`,
  `memory`, `hands`, `bay`, `hello` = A–G). Each has `name`, `jp`, `para`, `mediums`, `ideas`,
  `mood`, `tiers`, `day` (11 entries, 10:00–20:00), `frames` and `hue`.
- New images: JPEG, 1344 px wide, in `img/`, referenced as `img/<name>.jpg` (or by bare name
  inside `DIRS`/`FRAMES`). Only use images Wild Tame may use: client material, our own work,
  or licensed stock.
- The page must work at phone width with no sideways scrolling.
- This is confidential client work. Keep `noindex` (the build adds it), and don't link to
  personal accounts or sites. Everything stays under Wild Tame.

## Viewing

Once Pages is on for this repo, the live page is
https://wild-tame-co-ltd.github.io/sogo-clock-pitch/ (Japanese: `ja.html`). A push to `main`
updates it in about a minute.
