# lanewayapp.github.io

The public landing page and dev log for **Laneway**, verified trip routing that
includes the legs no map has indexed.

Live at <https://lanewayapp.github.io/>.

## Layout

- `index.html` - the landing page
- `devlog.md` - the engineering log, newest entry first. **Edit this one.**
- `devlog.html` - generated from `devlog.md`, committed complete. Do not hand edit.
- `tools/build_devlog.py` - the generator, standard library only
- `CLAUDE.md` - working context, read it before touching anything
- `JOURNAL.md` - session log for this repo

The product itself lives in a separate private repo. This one holds nothing but
the site.

## Running it

There is no build step. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8076
```

Both pages are self-contained: styles are inline, there are no fonts to fetch, no
scripts, and no third-party requests. They render with no network at all.

## Editing the dev log

Write the entry in `devlog.md`, newest at the top, then:

```bash
python3 tools/build_devlog.py
```

That rewrites the entries and the metrics band inside `devlog.html` and leaves
the rest of the page alone. Pushing `devlog.md` to `main` runs the same script
in CI and commits the result, so the page updates either way. The markdown
subset the generator accepts is documented in `CLAUDE.md`.

## Editing

Read `CLAUDE.md` first. The short version:

- Nothing on the page may claim more than the product actually does today.
- ASCII only. No em dashes, no smart quotes. The check script is in `CLAUDE.md`.
- The palette comes from the app's `Theme.swift`. Do not invent colours.
- Keep both pages in sync when a shared style token changes.
