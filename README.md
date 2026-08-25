# Fellowships For Free (F4F)

> **[fellowship4free.com](https://fellowship4free.com/) is the home of this project.**
> Corrected 2026-08-25 by owner ruling. This block previously said the opposite, that the
> domain was being retired and the project consolidated onto `jonathanlindavis.com/f4f`.
> That is stale and was contradicted by live behaviour: `jonathanlindavis.com/f4f` has
> 301'd TO fellowship4free.com since 2026-08-22, by owner order recorded at `_redirects`
> lines 193 to 196 in the `Jonathanlindavis.com` repo. Traffic flows from
> jonathanlindavis.com out to this domain, not the other way.
>
> Two things a maintainer needs to know and neither is obvious from this repo alone. The
> canonical dataset is `data/fellowships.json` in the **`Jonathanlindavis.com` repo**, not
> here, so the sync path between that file and what this domain serves has to stay honest
> or this site silently drifts from canon. And `jonathanlindavis.com/open-data-f4f`
> remains live as a mirror, pending the F4F rollout decision, so two pages currently serve
> the same dataset. Whether that mirror gains a canonical tag pointing here or is retired
> is an open question, not a settled one.

**Because finding money shouldn't cost you money.**

A free, public, open-data index of graduate and early-career fellowships — a no-paywall
alternative to membership-gated databases.

*A Project by Jonathan Lin Davis.*

- **Live site** (`index.html`): loads `data/fellowships.json`, with search, filtering,
  sort, and one-click CSV/JSON export — all in the browser, no backend.
- **Open data:** `data/fellowships.{json,csv}` — CC-BY-4.0. Code is MIT.

The weekly RSS-import pipeline described in earlier versions of this README
(`scripts/fetch_candidates.py`, `approve_candidates.py`, etc.) has been removed. Those
scripts were already broken, stale against a schema change from a prior redesign. The
original sentence here credited "the jonathanlindavis.com/f4f consolidation" for
superseding them, which is wrong on the same 2026-08-25 correction as the header block:
no such consolidation is happening. What actually replaced them is the growth scout,
`run_f4f_growth.ps1`, which commits to the canonical dataset in the `Jonathanlindavis.com`
repo on a weekly schedule.

## Sourcing policy (historical)

F4F never scraped websites — it read only published RSS/Atom feeds and APIs, and honored
`robots.txt`. This principle carries forward wherever F4F's data collection continues.

## Data schema (as last deployed here)

Bare JSON array, one object per fellowship:
`id, organization, name, url, opens, deadline, amount, other_benefits, eligibility, area, flags, notes`

## Licenses
Code: MIT (`LICENSE`). Data: CC-BY-4.0 (`LICENSE-DATA`).
