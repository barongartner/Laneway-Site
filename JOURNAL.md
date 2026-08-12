# The site exists: landing page and dev log - Wednesday Aug 12

*Time worked: the site work is anchored to the 11:36 AM repo clone and ran to
11:47 AM. The opening prompt came a few minutes before the clone and was not
separately timestamped, so it is left unstated rather than guessed. This
session had been working on Laneway in the product repo immediately before,
finishing the Live Activity design cards at 11:29 AM.*

## Timeline

**"Open up Laneway, can we make a website or landing page for it on GitHub
Pages, not sure if the same repo is good but maybe another one, not sure."**
Read the product repo first: `CLAUDE.md`, `README.md`, the top of
`JOURNAL.md`, the commit history back to day one, `ios/Laneway/Theme.swift`
for the palette, and `src/laneway/gtfs.py` for the real feed registry.

The repo question answered itself. `barongartner/LANEWAY` is private, GitHub
Pages will not serve a site from a private repo without a paid plan, and
`CLAUDE.md` says the repo stays private. Publishing from the product repo
would have meant making the engine public to get a web page, which is a bad
trade. Presented that, plus the honesty problem: there is no App Store
listing and no public build, so the page cannot have a download button
without breaking the one rule.

**Owner decisions.** A separate repo for now, folded back in at launch. A dev
log rather than a signup form, because there is nothing to sign up for yet.
Landing page and dev log as separate HTML files. And the repo to use:
`barongartner/CLAUDE-CHANGE-THE-NAME`, empty and public, created the day
before.

**Renamed the repo.** `laneway` was rejected by the API: GitHub repository
names are case-insensitive per account, so it collided with the existing
`LANEWAY`. Went with `laneway-site`, which is also clearer about what it is
while both repos exist.

**Built two pages.** Both self-contained, no build step, no third-party
requests, dark mode on both.

- `index.html`. The anchor case is the hero: two panels side by side, the
  dead two hour walk every mapping app returns against the four-leg Laneway
  journey with a verification chip on each leg. The third leg is deliberately
  marked unverified, because a page selling a verification product should
  demonstrate the product saying "I do not know this" rather than hide it.
  Then the one rule, three real verdict cards taken from actual engine
  results (the supported MiWay Airport Road claim, the contradicted Terminal
  1 claim, an unsupported operator claim), the six-stage pipeline, and an
  honest status section split into "working today" and "not there yet".
- `devlog.html`. Nine entries, newest first, curated from the private journal
  rather than copied from it. The regressions and corrections were kept on
  purpose: the footpath downgrade that hid itself, the mode switch that
  redrew verified transit legs as driving lines, the walking finder that
  opened itself without consent, the on-device black screen. A log of only
  wins would read as marketing.

**Palette lifted from the app, not invented.** Every colour token on both
pages is converted straight out of `ios/Laneway/Theme.swift`: ink navy
`#172133`, warm amber `#E89E2E`, paper `#F7F5ED`, night `#0D1421`, verified
green `#299E63`, contradicted red `#D14238`. The two verifier colours are
never used decoratively on the page, same as in the app.

**Facts checked before they were written.** The five supported feeds on the
page come from `AGENCY_FEEDS` in `src/laneway/gtfs.py`, not from memory: UP
Express, GO Transit, TTC, MiWay, Calgary Transit. The test count (133) and
the current build (0.7.0) come from the most recent journal entry and commit
subject in the product repo.

**"Also keep a journal and CLAUDE.md for this one, import from main if you
need."** Written. The site `CLAUDE.md` inherits the one rule, the house
style and its check script, the clock rule, and the git identity rule, and
adds what is specific to a public repo sitting next to a private one: an
explicit list of what must never cross over, the no-build-step and
no-third-party-requests rules, and the note that the dev log is a curated
view of the private journal rather than a copy.

**"Host them with GitHub Pages."** A local preview server was declined, so
verification happened against the live Pages URL instead.

## Open

- The page carries no screenshots. The app has never been captured, and a
  landing page for a maps product will eventually need real ones. Mockups
  would be inventing an interface, so nothing was faked.
- Version, test count and feed list on the page need updating when they
  change in the product repo. There is nothing automatic connecting them.
- Not linked from `barongartner.github.io` yet.
- When the product launches, the two repos merge or the site moves to a real
  domain, per the owner decision above.
