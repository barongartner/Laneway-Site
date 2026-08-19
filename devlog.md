# Metrics

- 6 | Days from empty repo to navigation
- 0.19.0 | Current build
- 137 | Tests, all offline
- 5 | Official transit feeds

# Entries

## 0.18.1 / 0.19.0 | Monday Aug 17
### A plan took five minutes, and the reason was invisible twice over

The product principle says under thirty seconds, with visible progress,
because beyond that people assume it hung. A real trip took about five
minutes, and the first report was not "this is slow" but "walking routing is
broken". The principle predicted its own symptom.

- **Both OpenStreetMap query mirrors were down at once**, one returning
  gateway timeouts and the other timing out on read. That alone is bad luck.
  What made it five minutes was the code around it: each mirror was given a
  twenty five second budget, so one tile could burn fifty seconds, and a
  failure was recorded nowhere, so every walking leg in the plan paid the full
  fifty seconds over again. Now the per-mirror budget is eight seconds, and a
  failed area is marked cold for three minutes so the rest of the plan falls
  back immediately. Worst case went from fifty seconds per leg to about
  sixteen seconds once.
- **Switching to driving kept the walking path.** The line itself was never
  wrong: a leg that cannot be re-routed keeps its old geometry and its old
  symbol, because drawing a driving route the router never returned would be
  worse. The bug was that this outcome was counted nowhere, so the summary
  line never mentioned it. The app showed a walking path under a driving
  selection and said nothing, which is the one rule broken on the screen where
  being right matters most.
- **The routing errors were being thrown away.** Apple's directions API was
  called with the error discarded, so every driving re-route failure in this
  app's history produced no diagnostic at all. It now reports what actually
  happened, separates a thrown error from an empty result, backs off between
  retries rather than firing straight back into a rate limit, and shows the
  last twelve failures on a screen inside the app. Reading device logs needs a
  cable and a Mac; the person hitting the bug is holding a phone.
- **Still open.** Whether the driving failure was rate limiting or something
  else is a theory until the next occurrence is read off that screen. The
  issue stays open rather than being closed on a fix to the reporting.

## 0.17.0 / 0.18.0 | Monday Aug 17
### Recents, and three things to do that the app can actually back up

Both big mapping apps lay their search surface out the same way: saved places
first, then recent destinations, then suggestions as you type. Laneway had the
first and the third and nothing in the middle, so every repeat trip was
retyped from nothing.

- **Recent destinations**, eight of them, newest first, one tap to plan again.
  Only destinations from plans that actually landed are kept. Recent
  *searches* are deliberately not stored: seeding the fastest path in the app
  with things that failed to plan would make the quickest route to a trip also
  the least reliable one.
- **Something to do near you**, three real places and a shuffle. The request
  was for three cool things, and cool is the one word this app cannot honour.
  Nothing available ranks places by how good an evening out they are, and a
  model asked to invent three fun spots produces plausible names, which is the
  exact failure the whole project exists to prevent. So the cards state what
  can be backed up: a real place, its category, and how far away it is. No
  ratings, no "open now" badge, no claim that any of it is good.
- **The shuffle is honest for the same reason.** It is a re-roll over real
  nearby places rather than a ranking pretending to be taste, which is
  arguably what a shuffle should be anyway. The results are pooled once and
  shuffled on the device, so a re-roll costs nothing.
- This is the one feature that works while the phone cannot reach the engine,
  because finding places nearby is done entirely on the device.

## 0.14.0 to 0.16.0 | Monday Aug 17
### A debug screen, and the two questions it answered immediately

Two problems had been invisible from the interface: a stale server address
that every screen reported as connected, and a stored home address written on
first run since version 0.9.0 that nothing had ever read back. Both are
obvious the moment the raw state is on a screen, and neither was findable
before one existed.

- **The debug screen shows what the app actually thinks:** which server it is
  using against every server it can see, a direct health check with the raw
  response, the location fix and its age, a spoken test line, a live
  microphone level, and every stored preference with its real value.
- **It earned itself on the first read.** The mode preferences collected
  during onboarding are written and never read by anything. The app asks which
  ways you travel, stores the answer, and plans every trip as though it never
  asked. That is now flagged in red on that screen, and filed rather than
  quietly fixed, because deciding whether to use it or stop asking is a
  product decision.
- **Onboarding could only ever be seen once.** The flag that marks it complete
  was written and never cleared, so the intro screens were a one time event
  that not even reinstalling brought back. There is now a way back in that
  erases nothing.
- **Setting a home address only offered "use current location"**, which is no
  use to anyone not standing at home while they set it up. It now takes a
  typed address with real suggestions. A contacts picker was built first and
  then removed: it existed only because the platform will not tell an app
  which contact card belongs to its user, so it asked people to pick their own
  house out of a list of everyone they know. Autocomplete answers the same
  need without the privacy surface.

## 0.11.0 to 0.13.0 | Sunday Aug 16
### Voice becomes a conversation, and the map gets a choice of ground

Version 0.10.0 had put a microphone on the home bar that opened the composer
already listening. That is a dictation box wearing an assistant's clothes: you
still read a sheet and tap a button.

- **Voice mode is now a full screen conversation.** It listens, plans, answers
  out loud, and listens again. It waits for its own sentence to finish before
  reopening the microphone, because otherwise it hears itself and answers its
  own question, and a tap interrupts mid-sentence the way a person interrupts
  a person. The orb reacts to real microphone loudness rather than animating
  on a timer and hoping.
- **Typing stayed the default.** Voice mode is the only place a plan is spent
  without a tap, which reverses an earlier deliberate decision, so it is
  guarded three ways: entering the mode is deliberate, a take under two words
  restarts the microphone instead of planning, and the take is shown on screen
  as it is sent. A plan is never spent invisibly.
- **Standard, satellite and hybrid basemaps.** Not the free change it looked
  like: the route lines are thin and unoutlined, which reads fine on a flat
  basemap and vanishes over a parking lot or a treeline in aerial photography.
  Each leg now draws a dark casing underneath it on imagery, solid even where
  the leg is dotted. The casing is deliberately colourless, because green and
  amber already mean verified and unverified and a second stroke does not get
  to dilute that.
- **Home and Work**, as one tap trips. The stored home address finally does
  something, five versions after it started being collected.

## 0.8.0 to 0.10.0 | Thursday Aug 13
### Bikes on the pathway network, and a first run worth having

The walking router already knew every footpath in an area. Riding one is the
same graph at a different speed, with one real exception.

- **Bike and e-bike.** The router grew speed profiles, and bikes skip
  staircases, because a cyclist cannot ride a flight of steps. The test pins
  the physics rather than the output: walkers take the stairs shortcut, bikes
  detour around it, and the e-bike takes the same detour faster. Apple has no
  cycling profile at all, so fallback geometry is re-timed at riding speed
  rather than presented as a walk.
- **First run onboarding**, five screens: what the app is, the promise about
  verified against unverified, the ways you travel, the location ask with its
  reason stated before the system asks, and the lock screen option shown
  rather than described.
- **Speaking a trip.** Live transcripts stream in as you talk and 1.8 seconds
  of silence ends the take. The microphone runs only while something on screen
  says it is running.

## 0.7.0 | Wednesday Aug 12
### Live buses on the map, and a footpath regression that hid itself

Real vehicles now move on the map where the operator publishes a realtime
feed. The more useful entry, though, is the bug underneath it.

- **The footpath regression.** Walking routes had quietly stopped using real
  paths. The engine was serving correct data for the exact queries the phone
  was making, so the failure was transient throttling on the public
  OpenStreetMap query service, silently downgrading walks to a generic
  around-the-block route. Fixed by trying a second public mirror before giving
  up, and by logging the fallback so it can never be invisible again.
- **Live vehicle positions.** GTFS-Realtime over protobuf, held in memory
  fifteen seconds so polling phones share one fetch, with a stale snapshot
  served rather than nothing on a failed refresh. First live probe returned
  332 real buses. On the phone: amber dots, filtered to the visible region,
  capped at sixty, polled only while a plan with a transit leg is on screen.
- **The lock screen got a proper design pass**, and "big arrow guidance"
  became "Compass view", because a mode name should say what you see.

## 0.6.0 / 0.6.1 | Wednesday Aug 12
### The wait shows its work, and the anchor case is a journey again

An interface review with one blunt verdict: it gets the job done, but it does
not go the extra mile that justifies the AI built into it. Buttons are now
sized to their importance, and the planning wait tells you what it is
currently verifying instead of spinning.

- **The most important fix was a correctness one.** Switching travel modes was
  redrawing already-verified transit legs as driving lines. That is exactly
  the fabricated-fact failure this project exists to prevent: the screen would
  have shown a route no source supports. Mode switching now refuses to invent
  drives.
- **The anchor case had quietly broken** and was coming back as a single leg
  instead of a journey. Caught, fixed, and now covered.

## 0.3.0 to 0.5.2 | Tuesday Aug 11
### Walking on real paths, and a lock screen worth glancing at

Apple's walking directions route you around the block. Real pedestrians cut
through the park. Walking legs now run on OpenStreetMap footpaths, drawn as
footstep dots, with smoothing that rounds gentle bends and keeps real corners
sharp.

- **Trip times became honest.** If the app cannot stand behind a duration, it
  does not print one.
- **A maneuver-arrow Live Activity** so the next turn is readable without
  unlocking the phone.
- **A correction worth recording:** the first cut of the walking finder opened
  itself automatically. A full screen takeover that happens to the traveller
  solves discovery by removing consent. It is now something you choose.

## Direction | Tuesday Aug 11
### The real vision: a maps alternative, not a planning tool

> "It IS supposed to be turn by turn, an alternative to Apple and Google
> Maps."
> -- Owner decision, Tuesday Aug 11

Scope rewritten the same hour. Planning and verification stay the foundation
and the moat, because verified routes are what make this an alternative rather
than a clone; navigation is the surface people actually live in. Voice
guidance stays out for now.

- **Navigation phase one shipped that day.** Follow mode with a tight camera,
  per-maneuver instructions on road legs, automatic leg advance with a haptic,
  sustained off-route detection, and an off-route banner whose tap replans to
  the same destination from wherever you now are. All the geometry is
  deterministic and runs on the device.

## Engine | Monday Aug 10
### A spinner that lies, and roads that are actually roads

- **The wait became truthful.** Planning runs as a job the app polls, so the
  card shows the real state: "Verified 3 of 6: MiWay route 7 serves stops on
  Airport Road."
- **Walk, taxi, drive and shuttle legs** now draw true routed lines. Transit
  legs stay schematic and dashed on purpose: a bus's real path is the
  operator's published data, not ours to invent. That honest gap is filed as
  an issue, not papered over.
- **The black screen.** The app rendered nothing on a real iPhone while the
  process stayed alive. The stock SwiftUI map view was hanging on that device
  and iOS combination; replacing it with the older UIKit map view fixed it
  outright. Two hours, and the kind of thing no simulator would have shown.

## Rebuild | Sunday Aug 9
### Map first, and the first fully verified leg

- **The app was rebuilt around the map** rather than around a form: full-bleed
  map, a search capsule, numbered pins, and the plan in a drag-up sheet. Pins
  come from two-pass geocoding, and a stop that cannot be placed confidently
  gets no pin at all rather than a wrong one. Plain geocoding had been putting
  "YYZ Terminal 1" in Rhode Island.
- [ok] **First verified leg** On the anchor case, live: a MiWay bus leg with
  both of its claims supported by the official feed.
- **Saved plans went offline**, with the full response and its resolved map
  geometry stored on the device.

## Feeds | Saturday Aug 8
### Official feeds before the open web, and the first supported claim

Transit claims are now checked against operators' own published schedule data
before anything on the web is trusted. This produced both of the results the
project was built to produce, on the same afternoon.

- [ok] **Supported** "MiWay route 7 serves stops on Airport Road", grounded in
  the official feed, which lists a stop at 6445 Airport Rd.
- [bad] **Contradicted** The same feed proved route 7 does **not** enter
  Pearson Terminal 1, correctly killing a claim the planner had reached for.
  The verifier catching the planner is the system working, not the system
  failing.
- **Challenge pages are now treated as unreachable**, never as documents, so a
  bot-check page can never be cached and cited as evidence.
- **The engine became a background service** nobody has to start by hand.

## First build | Friday Aug 7 to Saturday Aug 8
### Verifier before retriever, and a phone that finds its own engine

The build order was deliberate and slightly backwards: the verifier was
written third, before the thing that fetches anything, because the impressive
part of this product is the reasoning and the valuable part is the
verification.

- **Provenance is enforced by the type system.** A fact without a source URL
  and a fetch timestamp cannot be constructed at all, so it cannot be
  forgotten in review.
- **The verifier can return "unsupported"** and was never allowed to collapse
  into a yes or no. It cites verbatim spans from sources it was handed, and it
  fails closed.
- **First real-world lesson, immediately:** the airport's own website blocks
  the crawler and the obvious mapping source disallows it in robots.txt. So
  the legs came back honestly unverified. That is the correct behaviour and it
  set the agenda for the next week: go to the operators' published feeds.
- **The phone finds the engine by itself** over local network discovery, with
  a free demo plan so the interface can be worked on without spending a cent.

## Day zero | Friday Aug 7
### Just working, boiler plate stuff

> Never present a fact the system cannot back up. One fabricated shuttle stop
> destroys trust permanently.

Everything since has been an argument with that sentence, and the sentence has
won every time.
