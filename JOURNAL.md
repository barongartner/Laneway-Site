# The Page Reads the Markdown Itself - Wednesday Aug 19

*Written 11:47 AM, read off the clock. Replaces the approach committed about
ten minutes earlier in the same session.*

## Timeline

**The generator was the wrong answer to the question asked.** The entry above
this one built `tools/build_devlog.py` and a CI job to render `devlog.md` into
`devlog.html`. That kept the page static, but it meant either running a command
before every commit or granting the CI token write access to the repo. The
owner wanted neither: "i dont want to write a command, whenever i commit, its
updated to the repo, but when i open the website it fetches the md".

**So the page reads the file directly.** `devlog.html` now carries a parser at
the bottom of the file, fetches `devlog.md` on load, and builds the metrics
band and the entries from it. Writing an entry is editing markdown and
committing it. Nothing else runs, by anyone, at any point.

**The parser is the same subset, ported.** Version and date, headline, optional
pull quote with an optional attribution line, paragraphs, notes, `**bold**` and
`*italic*`, and the `[ok]` and `[bad]` verdict tags. Escaping happens before the
marks are applied, so an angle bracket in the prose can never become markup and
a malformed entry renders as visible literal text rather than broken HTML.

**Rendering parity was checked against the page as it stood before any of
this.** Every count matches: four metrics, fourteen entries, two pull quotes,
forty two notes, three verdict tags, thirty nine bold runs, one italic. Version
treatment still splits correctly, `0.18.1 / 0.19.0` as a display figure and
`Day zero` as a mono label. Read back through the DOM rather than by eye.

**One difference was found and chased down rather than waved off.** Extracted
text is 115 characters shorter than before, because the renderer concatenates
adjacent elements with no whitespace between them where the handwritten HTML
had newlines. Every instance is at a boundary where the whitespace never
rendered: `.who` is `display: block`, the metric label `.k` is `display:
block`, and the verdict tag already emits a trailing space. Confirmed by
reading the computed styles, not assumed.

## Changed

- `devlog.html`: the entries and metrics regions are now empty containers,
  `#log` and `#metrics`, filled at load. The generator's marker comments are
  gone. One `<script>` at the end of the file, about 170 lines. A `.fallback`
  style for the two cases where the log cannot load.
- `tools/build_devlog.py` and `.github/workflows/devlog.yml` deleted. Both
  existed for about ten minutes and are in the history if the approach is ever
  reversed.
- `CLAUDE.md`: the no build step rule is restored as an absolute, with the
  owner decision and its date recorded, and the cost of this approach written
  down beside it rather than left to be rediscovered.
- `README.md`: says to edit `devlog.md` and commit, and that the page must be
  served over http to render locally.

## Open

- **`devlog.html` no longer opens from disk.** A `fetch` from a `file://`
  origin is blocked, so opening it in Finder shows the chrome, the masthead and
  a line pointing at `devlog.md`. `index.html` is unaffected and still opens
  straight off disk. Recorded in `CLAUDE.md` as an accepted cost, not a bug to
  file.
- **The entries are no longer in the HTML source.** Anything that does not run
  JavaScript sees an empty log: crawlers that do not execute scripts, link
  unfurls, and readers with scripting off. A `<noscript>` block points at the
  markdown, which reads fine on its own. This is the same tradeoff as above and
  was accepted with it.
- The repository's default workflow permission was left at read. Nothing needs
  it now that CI is gone.
- Still carried over and untouched: no dark mode on the landing page, and
  in-page anchors landing under the sticky header on both pages.

# The Dev Log Becomes Markdown, and the Page Is Generated From It - Wednesday Aug 19

*Written 11:35 AM, read off the clock. The start was not recorded, so no
duration is claimed here.*

## Timeline

**The ask was to write entries as markdown and have the page follow.** The
obvious version, fetching `devlog.md` from the page and rendering it in the
browser, was rejected before it was built. A `fetch` of a sibling file fails
from a `file://` origin, which would have broken the property this repo has
protected from the start: open the page off disk and see the finished page.
It would also have made the log invisible without JavaScript, to crawlers and
to link unfurls, and it would have meant inlining someone else's markdown
parser into a file whose rule is that it is self contained.

**Generating at commit time keeps every property.** `devlog.md` is now the
source of truth. `tools/build_devlog.py` renders it into `devlog.html`, which
stays committed complete: no script on the page, no fetch, no dependency,
works from disk, still one file.

**The generator is small because the log is regular.** A survey of the
existing page first: fourteen entries, and the only inline markup in the whole
file was thirty nine `<b>`, one `<i>`, and three verdict tag spans. No links,
no code spans, no nested lists. So this is not a markdown library, it is a
parser for the one shape the log actually uses, in standard library Python
with no dependencies. Two block types beyond paragraphs and notes: the pull
quote used by two entries, and the `[ok]` and `[bad]` verdict tags used by
three notes.

**Parity was proved, not assumed.** The existing fourteen entries were
extracted to `devlog.md` by a throwaway script, then rendered back through the
generator and compared against a pristine copy of the original page. The tag
sequence including classes is identical, 522 to 522, and the visible text is
identical, 15835 characters to 15835. Only line wrapping inside text nodes
differs, which changes nothing rendered. Checked in a browser as well: four
metrics, fourteen entries, two quotes, three tags, forty two notes, and the
version treatment still splits correctly, `0.18.1 / 0.19.0` as a display
figure and `Day zero` as a mono label.

## Changed

- `devlog.md`, new, the source of truth for the entries and the metrics band.
- `tools/build_devlog.py`, new. `--check` exits 1 when the page is stale.
- `devlog.html` now carries four marker comments. The generator rewrites only
  what sits between them and never touches the styles, masthead or footer.
- `.github/workflows/devlog.yml`, new. On a push that touches `devlog.md` or
  the generator it renders, runs the non-ASCII check, and commits the result
  only if it differs. The path filter excludes `devlog.html`, so the commit it
  makes cannot retrigger it.
- `CLAUDE.md`: the no build step rule is amended to "no build step between the
  repo and the reader", with the reason spelled out, and the dev log section
  now documents the markdown subset. `README.md` says which file to edit.

## Open

- **The workflow cannot push yet.** The repo's default workflow permission is
  read, so the commit step would fail. Nothing fails today, because the commit
  step exits early when there is no diff and the page is currently in sync.
  Flipping it to write is a repository setting and was left for the owner to
  decide, since it is the setting that stops a compromised action from writing
  to the repo. Until it is flipped, `python3 tools/build_devlog.py` before
  committing is the working path, and CI is a no-op.
- **The markdown subset is deliberately small.** A link in an entry, a nested
  list, or a code span will not render; the generator escapes first, so it
  fails visibly as literal text rather than silently emitting broken markup.
  Widening it is a change to the generator, not something to work around in
  the source.
- The landing page still has no dark mode, and in-page anchors still land
  under the sticky header. Both carried over from earlier today and are
  untouched.

# Device forward promoted to index - Tuesday Aug 18

*Written 8:20 PM, read off the clock. Second session entry today; the first
promoted variant A a little under half an hour earlier.*

## Timeline

**A fourth direction arrived after A had already shipped.**
`laneway-1e-device-forward.html`, held outside the repo in the downloads folder.
Same five sections and the same copy below the fold as A, byte for byte on a
diff of the visible text. The whole difference is the hero and the chrome: a
gradient paper ground, a backdrop blurred sticky header, pill buttons with a
warm shadow under the primary, soft shadowed panels, the supported feeds
surfaced as pills in the hero rather than only in the status section, and an
iPhone rendered in CSS showing the anchor case as the app would present it.

**It was reviewed against the rules in this file before it went in.** It passes
the mechanical bar: the non-ASCII check is clean, there are no third-party
requests at runtime, `prefers-reduced-motion` is handled, and there is no build
step. The canonical `og:url` was stale, still pointing at
`barongartner.github.io/laneway-site` from before the move to this subdomain,
and was corrected to `https://lanewayapp.github.io/` as part of promoting it.

**Objections were raised and the owner decided to ship it anyway.** They are
recorded here in full rather than dropped, because the reasons do not go away
just because the page did.

## Changed

- `index.html` replaced with the device forward direction. Variant A, promoted
  earlier today, is superseded and recoverable from git history.
- `og:url` corrected to the current subdomain.
- `devlog.html`, `CLAUDE.md`, `README.md` untouched.

## Open

- **The device mock invents an interface.** The hero renders an iPhone screen in
  CSS: a status bar reading 14:02 and 5G, a header, and four plan rows. It is
  not a capture of the app. The rule in `CLAUDE.md` is that screenshots must be
  of the app as it actually is, and the standing open item in this journal said
  there were no screenshots precisely because a mockup would be inventing an
  interface. This is that mockup, and it is now the largest element on the page.
  `ios/Laneway.xcodeproj` exists in the product repo, so a real capture is
  possible and would settle this properly.
- **"4 legs, 38 min" is not backed by anything on the page.** The legs shown
  total 13 minutes of movement, and the third leg is stated to have no published
  timetable, so a total duration cannot be derived from what the reader is
  shown. It needs to come from the engine or come off the page.
- **The headline no longer contains the contrast.** A led with "Your map says it
  is a two hour walk. It is a four minute shuttle." This leads with "Trips that
  include the legs nothing else will route", which is a capability statement
  rather than a demonstration. The stronger line is preserved in git.
- **Still no dark mode**, on either page in the sense that matters: the landing
  page has no `prefers-color-scheme` block at all while `devlog.html` has three,
  so a reader in dark mode sees a paper landing page and a night dev log. This
  carried over from A and is unchanged.
- **In-page anchors land under the sticky header.** The header is 60px and no
  section carries a `scroll-margin-top`, so the nav links for the problem, proof
  and status all put the section heading behind the bar. Present on the previous
  index as well, so it is an old fault rather than a new one, and it affects
  `devlog.html` only if the same pattern is used there.
- **The supported feed list appears twice**, once in the hero and once in the
  status section, with identical entries.
- **119px of empty space inside the phone**, about a quarter of the plan card,
  between the last leg and the footnote. The screen height is fixed at 660px and
  the content does not fill it.

# Landing page variant A promoted to index - Tuesday Aug 18

*Written 7:56 PM, read off the clock. The start was not recorded, so no
duration is claimed here.*

## Timeline

**Three landing pages were live at once.** A survey of the published site found
`A.html` and `B.html` sitting in the repo root alongside `index.html`, all three
serving a full landing page. Nothing linked to either variant, but GitHub Pages
serves every file in the branch, so both were publicly reachable and indexable
at their own URLs. They had been left behind as drafts.

**The three were compared.** All three carry the same copy and the same five
sections, so the comparison came down to the hero and the palette. `index.html`
was the type specimen: an oversized "Laneway" set against cap height and
baseline guides, dark. `A.html` was paper, with the headline kept as a full
sentence and the anchor case rendered beside it as a vertical ticket. `B.html`
was dark, with the headline compressed to all capitals across the full width and
the legs laid out as a horizontal strip of four tiles.

**A was picked.** Three reasons, in order of weight. The headline keeps "Your
map says it is a two hour walk", which names who is wrong; B drops that clause
and the sentence loses its antagonist. The ticket gives the unverified leg a
full row with its caveat intact, "roughly every 20 min, no published timetable",
where B truncates it to a tile and the admission gets compressed into a chip.
And the paper treatment reads as a document rather than a poster, which is the
tone the one rule asks for: a page that argues for sourced facts should not
shout louder than its own claim.

**B also had a layout fault.** Its leg strip is set as
`repeat(auto-fit, minmax(230px, 1fr))`, so below roughly 1030px of viewport the
fourth leg wraps onto its own row and leaves two empty cells inside the hero. It
is clean at 1280px and above. This was not the deciding reason but it was not
nothing.

## Changed

- `A.html` renamed to `index.html`, replacing the type specimen version.
- `B.html` deleted.
- `devlog.html`, `CLAUDE.md`, `README.md` untouched.
- The repo is back to the two pages `CLAUDE.md` says it has.

**Checked, not assumed.** No file in the repo referenced `A.html` or `B.html`,
so the deletion broke no link. The promoted page already carried the correct
canonical `og:url` of `https://lanewayapp.github.io/`, because it was written as
a candidate index rather than as a subpage, so no meta tag needed editing. The
non-ASCII check passes clean.

## Open

- **The promoted page has no dark mode.** `A.html` was written light only: it
  contains no `prefers-color-scheme` block at all, while `devlog.html` has
  three. On a reader whose machine is set to dark, the landing page now stays
  paper and the dev log goes night, which is a visible break between the only
  two pages on the site, and it contradicts the rule in `CLAUDE.md` that both
  pages carry dark mode and are always tested in both. The dark palette from the
  discarded specimen index cannot be lifted across unchanged, because the class
  names differ. This needs a dark palette written for the new markup.

# Moved to its own subdomain: lanewayapp.github.io - Tuesday Aug 18

*Ended 4:58 PM, read off the clock. The start was not recorded, so no duration
is claimed here.*

## Timeline

**"i want everything to be barongartner.github.io/everything except for
laneway, that needs to be laneway.github.io".** GitHub decides the shape of a
Pages URL from the repo name alone: a repo named `<account>.github.io` is
served at the root of that subdomain, and every other repo is served in a
subfolder under it. So the site could not be moved to its own subdomain by
configuration. It needed an account of its own.

**`laneway` was not available.** The org `github.com/Laneway` was registered on
Aug 7 2021 and has never been used: zero public repos, zero followers, nothing
pushed since the day it was created, and `laneway.github.io` returns a 404.
GitHub does not release a held name for inactivity alone without a trademark
claim, so it was treated as gone. Of the variants checked, `laneway-dev` was
also taken; `lanewayapp`, `getlaneway`, `laneway-io`, `uselaneway` and several
others were free. Owner picked `lanewayapp`.

**The move.** A free organisation, `lanewayapp`, created by hand, since the
GitHub API only allows org creation for Enterprise admins. Then the repo
transferred from `barongartner/Laneway-Site` into it and renamed to
`lanewayapp.github.io`. Pages carried its own configuration across both steps,
kept building from `main` at `/`, and came back up at the root of the new
subdomain.

**What broke, on purpose.** `barongartner.github.io/Laneway-Site/` is now a 404.
Repository URLs redirect after a transfer; Pages URLs do not. This cost nothing
today because the page was not linked from anywhere public: the personal site at
`barongartner.github.io` was checked and has no reference to Laneway.

**What made the move cheap.** The rule in `CLAUDE.md` about keeping the pages
free of anything painful to move. Both pages use relative links and inline
styles, with no absolute path and no host hard-coded anywhere except the
canonical URL in the `og:url` tags. Only two tags needed editing. That rule was
written for a future move to a real domain and it paid out early.

## Changed

- `index.html`, `devlog.html`: `og:url` repointed at the new subdomain.
- `README.md`: title and live URL.
- `CLAUDE.md`: live URL, plus a note in "Why this is a separate repo" recording
  why the repo now sits in an org rather than under the personal account.
- Local clone: `origin` repointed. The directory is still `~/Desktop/laneway-site`.

## Not done

- The private `barongartner/LANEWAY` engine repo was not touched.
- No custom domain. The `og:url` tags will need editing again if one is bought,
  which is the same two lines.

# Five Days of Dev Log Written at Once - Monday Aug 17

*Time worked: about 10m (roughly 5:02 PM to 5:12 PM). Estimated from the first
file written this session; the end is read off the clock.*

## Timeline

**"are you updating the dev log on the site?"** No, and that was the honest
answer. The dev log had been sitting at 0.7.0 from Wednesday Aug 12 while the
product went to 0.19.0, so **twelve versions and five days** of work were
missing from the public page. Nobody had asked for it in the meantime, which is
exactly how a public log dies.

Five entries written, newest first, grouped by theme rather than one per patch
release, since a reader wants the story and not the changelog:

- **0.18.1 / 0.19.0**, the five minute plan and the invisible driving failure.
- **0.17.0 / 0.18.0**, recents and Something to do, including why "cool" is the
  one word the app cannot honour.
- **0.14.0 to 0.16.0**, the debug screen and the two questions it answered on
  its first read.
- **0.11.0 to 0.13.0**, voice becoming a conversation, and the basemap casing.
- **0.8.0 to 0.10.0**, bikes on the pathway network and first-run onboarding.

**Two stale claims fixed, which is the more important half.** This repo's own
rule says a stale number is a false claim with extra steps, and the page was
carrying three:

- The metrics block said current build 0.7.0 and 133 tests. Now 0.19.0 and 137.
- The landing page's "Not there yet" column still said **"No voice guidance
  yet"**. Voice input, spoken replies, and spoken turn-by-turn all shipped days
  ago, so the public page was actively wrong about the product. Voice moved to
  the "Working today" column and the "Not there yet" line now covers booking,
  payment, and accounts.

**Boundary check, since this repo is public and the product repo is not.**
Grepped the changed files for local network addresses, the engine port, the
LaunchAgent name, the wifi network, the device identifier, the Apple team id,
the owner's email, and the coordinates that appeared in the engine logs during
the Overpass outage. All clean. The outage entry describes the failure without
saying where it happened, and no real errand or destination appears anywhere.

# The site exists: landing page and dev log - Wednesday Aug 12

*Time worked: the site work is anchored to the 11:36 AM repo clone and ran to
11:54 AM. The opening prompt came a few minutes before the clone and was not
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
verification happened against the live Pages URL instead. Pages enabled on
`main` at the repo root, first build live at 11:48 AM.

**Three real bugs found during verification, all after the first deploy.**
Worth recording because two of them were invisible in the way I was
looking at the page.

- **The closing plate inverted in dark mode.** It was painted
  `background: var(--ink); color: var(--paper)`, and both tokens flip with
  the scheme, so in dark mode it rendered as a near-white slab across the
  full width. Now it has its own pinned tokens (`--plate`, `--plate-fg`)
  that do not flip: a dark plate on paper, a slightly raised panel against
  the night background. **The general lesson: a block that deliberately
  inverts the page cannot be built out of the page's own inverting
  tokens.**
- **The claim cards declared `margin-top` twice** on the citation block, so
  the later `16px` silently beat the `margin-top:auto` that was supposed to
  pin citations to the bottom. With quotes of different lengths the three
  citations did not line up. Found by reading computed styles, not by
  looking; the misalignment is subtle enough to read as intentional.
- **The hero and the masthead killed the page gutter.** Both elements carry
  `.wrap` for the horizontal gutter and then set their own `padding` with
  the shorthand, which resets left and right to zero. At desktop width the
  1060px max-width supplies its own margins so nothing looks wrong; at
  375px the headline sat flush against the edge of the screen. Longhands
  now. **Anything that is also a `.wrap` must use padding longhands.**

**Host gotcha, cost about ten minutes.** The browser pane on this Mac
screenshots pure black at any scroll offset other than zero, and it also
served a stale cached copy of the page after a redeploy, which briefly
looked like the plate fix had not worked. Two workarounds that did work:
verify structure and computed styles through JavaScript rather than by
eye, and to actually see a section, `display:none` the sections above it so
the target renders at scroll zero. Cache-bust with a query string after
every deploy. Both pages were confirmed in light and dark, at desktop and
at 375px, with no horizontal overflow.

## Open

- The page carries no screenshots. The app has never been captured, and a
  landing page for a maps product will eventually need real ones. Mockups
  would be inventing an interface, so nothing was faked.
- Version, test count and feed list on the page need updating when they
  change in the product repo. There is nothing automatic connecting them.
- Not linked from `barongartner.github.io` yet.
- When the product launches, the two repos merge or the site moves to a real
  domain, per the owner decision above.

---

# Both pages reset as a type specimen - Wednesday Aug 12

*Time worked: anchored to the 12:36 PM clock check taken once the two sites
had been read, and ran to 12:55 PM. This session opened on unrelated work
(a web design aesthetics reference page) and moved to the sites when the
owner asked for the redesign; that prompt was not separately timestamped,
so it is left unstated rather than guessed.*

## Timeline

**"Redesign my 2 sites like type specimen."** The two sites are
`barongartner.github.io` and this one. The reference is the Type Specimen
plate from the owner's own aesthetics page: an oversized glyph as the hero,
size ladders, technical annotation in the margins, and metrics treated as
content.

**Named the problem before starting.** That plate's own failure note says a
system font stack undercuts the whole conceit, because a specimen exists to
show off a face. This repo forbids third-party requests, so there are no
fonts to fetch and no face to sell. The way through was to stop pretending:
the margins now say the page is set in the two families the reading machine
already has, its grotesque for metrics and labels, its serif for statements.
That is true, and it keeps the specimen from claiming something it cannot
back up.

**Both pages got the same plate.** The wordmark is set past the measure so
the frame crops the last letter, with cap height, x-height and baseline
drawn across it and labelled in the margin.

- The guides are positioned by arithmetic, not by eye. For this class of
  grotesque the cap height is .717em and the x-height .523em, and in a line
  box of height L the baseline sits .77 - (1 + L)/2 + L above the bottom of
  the box, which is .15em at the .84 line height used here. Those constants
  are in the CSS as `--wm` and `--base`, so the guides land on the letters
  at every viewport width.
- The wordmark is set mixed case rather than caps on purpose. An all-caps
  sample has no x-height to demonstrate, so the middle guide would have
  been labelling a position nothing on the page showed. "Laneway" and
  "Dev log" both put lowercase under that guide, and both have a descender
  that crosses the baseline and gets cropped by the frame.

**Everything else went flat.** Rounded cards, pills and drop shadows are the
opposite of a specimen sheet, so they are gone: hairline rules, square
corners, no shadows. The palette did not move, and the three verifier
colours still mean only what they meant.

- Verdict chips are now mono labels preceded by a solid square of the
  verdict colour, rather than tinted rounded pills.
- The pipeline stage numbers are set as display figures, greyed except for
  stage 05, the verifier, which stays amber.
- `index.html` gained a metrics band: four figures, every one of them read
  off this same page (four legs in the anchor case, three verdicts, five
  feeds, six stages). Nothing new is claimed.
- The dev log's stats became the same band, and each entry now carries its
  version as a display figure in the margin. Numbered releases get the
  figure treatment; named phases like "Direction" and "Day zero" are set as
  mono labels, because they are labels and not releases.

**Checked, not assumed.** Text was diffed word for word against the previous
version of both pages: zero words removed from `index.html`, and the five
from `devlog.html` are all capitalisation changes in the stats labels. No
link changed on either page. The non-ASCII check passes clean, and a
separate grep confirmed no em dash, en dash, arrow or smart quote entities
were introduced. Both pages were read in light and dark.

## Open

- Still no screenshots, for the same reason as before: the app has never
  been captured and mockups would be inventing an interface.
- The version, test count and feed list in the metrics band still need
  updating by hand when they change in the product repo. The band makes
  them more prominent than they were, so a stale number now costs more.
- Nothing is committed. The working tree holds the redesign for review.
