# lanewayapp.github.io

The public landing page and dev log for **Laneway**, verified trip routing that
includes the legs no map has indexed.

Live at <https://lanewayapp.github.io/>.

## Layout

- `index.html` - the landing page
- `devlog.md` - the engineering log, newest entry first. **Edit this one.**
- `devlog.html` - the page that reads `devlog.md` and renders it. Chrome only.
- `CLAUDE.md` - working context, read it before touching anything
- `JOURNAL.md` - session log for this repo

The product itself lives in a separate private repo. This one holds nothing but
the site.

## Running it

There is no build step. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8076
```

Styles are inline, there are no fonts to fetch and no third-party requests of
any kind. `index.html` has no scripts at all and renders with no network.
`devlog.html` carries one script, its own markdown renderer, and reads
`devlog.md` from this same folder.

## Editing the dev log

Write the entry at the top of `devlog.md` and commit it. That is the whole
process; there is no build and nothing to run. The page fetches the markdown
and renders it, so the site is updated as soon as the commit is served.

The markdown subset the page understands is documented in `CLAUDE.md`.

One consequence worth knowing: `devlog.html` needs to be served over http to
render, because browsers block `fetch` from a `file://` page. Opening it from
Finder shows the chrome and a pointer to the markdown. `python3 -m http.server`
below is enough to see it properly.

## Editing

Read `CLAUDE.md` first. The short version:

- Nothing on the page may claim more than the product actually does today.
- ASCII only. No em dashes, no smart quotes. The check script is in `CLAUDE.md`.
- The palette comes from the app's `Theme.swift`. Do not invent colours.
- Keep both pages in sync when a shared style token changes.
