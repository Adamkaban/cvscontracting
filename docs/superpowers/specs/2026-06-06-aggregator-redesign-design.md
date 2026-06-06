# CVS Contracting — Aggregator Redesign + Data Enrichment

**Date:** 2026-06-06
**Status:** Approved (design), pending implementation plan
**Scope:** Full visual redesign (all page types) + re-normalization of `scripts/raw/companies_filtered.csv` into an enriched company schema.

---

## 1. Problem

- Home page (`src/pages/index.astro`) is a 15-line placeholder stub: no hero, no service grid.
- Existing components follow design.md tokens but the result reads as generic "AI-default" blue/white SaaS.
- Company JSON was imported with a **minimal** schema; the CSV holds rich trust fields (years in business, BBB, insured, service area, description) that were dropped.

## 2. Goals

1. Distinctive, modern lead-gen **aggregator** look ("Trust-editorial" direction) that does not read as templated AI output.
2. Re-normalize the CSV into an **enriched** company schema that feeds trust signals and E-E-A-T.
3. Apply one cohesive design system across **all page types**: home, service hub, city-service, blog, nav, footer.
4. Stay within project rules (design.md, content.md, seo.md, data.md) except the explicit, logged palette extension below.

## 3. Non-Goals

- No new routes, no Phase 2/3 features (claim, company profiles, lead form).
- No dark mode. No JS animation beyond CSS transitions + FAQ caret.
- No change to URL structure / `trailingSlash: "never"` (permanent decision).
- No manual rewriting of 1000 company descriptions (generated one-liners instead).

---

## 4. Approved Decisions

| Topic | Decision |
|---|---|
| Design direction | **Trust-editorial** |
| Palette | **Extend** design.md (logged deviation below) |
| Data | **Re-normalize** CSV into enriched schema |
| Redesign scope | **All page types** |
| `Insured` badge | **(a)** Show only on strict `yes`, with a once-per-page `*self-reported` footnote |

### 4.1 Palette extension (logged deviation from design.md)

design.md specifies white bg / blue-700 / green-700 / cold grays. This redesign **keeps** blue-700 (CTA/links), green-700 (verified/positive), amber-400 (stars), but **adds**:

- Page background: warm paper `#FAFAF7` (cards stay white for lift)
- Ink (headings, nav wordmark, footer block): `#0F172A`
- Borders: warm stone `#E7E5E4` instead of cold `gray-200`
- Section tint: `#FAFAF9`

Rationale: the primary lever against "AI-default" is warm neutrals + mono numerals + typographic rhythm, not a new accent hue. All other design.md constraints stand (light only, Geist, Phosphor inline SVG, no gradients on CTA, no carousels, no em-dash, "Get Free Quotes" CTA, affiliate `rel="nofollow sponsored"`).

---

## 5. Data Pipeline

### 5.1 Source reality (from coverage analysis of 1083 rows)

| Field | Coverage | Handling |
|---|---|---|
| google_rating / reviews | 100% | core, always shown |
| years_in_business | 44% (dirty: "30 years", "30") | parse to `int`; badge `{n}+ yrs` |
| bbb_rating | 9% (mostly `A+`) | badge `BBB {rating}` when present |
| insured | 36% (very noisy) | `true` only if value normalizes to yes; else omit |
| license_number | 9%, unverified | **dropped** (content rule: no unverified claims) |
| cost_range | 36%, unreliable | **dropped** per-company; use service avg from services.json |
| description | 89%, Angi text | **not rendered verbatim**; one-liner generated from structured fields |
| service_area | 50% | optional badge `Serves {area}` (truncated) |
| business_hours | 24% | stored, not shown in Phase 1 |
| email | 5% | stored, not shown |
| phone | 26% | shown (mono) when present; CTA is affiliate regardless |
| logo | 158 files in `public/logos/` | map to `/logos/{domain}.png` if file exists, else `null` → monogram |

### 5.2 Enriched schema (`CompanyEntry` in `src/types.ts`)

Add to existing interface (all new fields optional):

```typescript
export interface CompanyEntry {
  // existing
  name: string
  slug: string
  city_slug: string
  service_slug: string
  address: string
  zip: string
  phone: string | null
  rating: number
  review_count: number
  google_maps_url: string | null
  website: string | null
  logo_url: string | null
  claimed: boolean
  featured: boolean
  // new (enrichment)
  years_in_business?: number     // parsed int, omit if unknown
  insured?: boolean              // true only on strict yes
  bbb_rating?: string            // "A+", "A", etc.
  service_area?: string          // cleaned, truncated string
  blurb?: string                 // generated one-liner, NOT raw Angi text
}
```

`blurb` generation rule (deterministic, from structured data, no copy-paste):
`"{Service} in {City}{, serving service_area}{ · years+ yrs experience}"` — pick available parts, sentence-cased, no em-dash.

### 5.3 Normalizer

- New script: `scripts/normalize.py` (repo `.venv` is Python 3.13; CSV has multiline quoted fields that need a real CSV parser).
- Input: `scripts/raw/companies_filtered.csv`. Output: `src/data/companies/{service-slug}.json` for the 4 Phase-1 services.
- Steps: filter `rating >= 3.5`; dedupe by (`name`+`city_slug`); map city name to `city_slug` from cities.json; parse years; normalize insured/bbb; build blurb; map logo; sort by a quality score (rating × log(reviews)) so `#1..#N` ranking is meaningful.
- Quality gate: a city-service with `< 3` companies is **excluded** from output (so `getStaticPaths` never emits it).
- Idempotent: re-running reproduces the same JSON.

---

## 6. Design System

### 6.1 Tokens (in `src/styles/global.css` `@theme`)

- `--color-paper #FAFAF7`, `--color-ink #0F172A`, `--color-line #E7E5E4`, `--color-tint #FAFAF9`
- keep `--color-brand #1D4ED8`, `--color-success #15803D`, `--color-stars #FBBF24`
- mono numerals: existing `--font-mono` stack; applied via a `.num` utility (`font-variant-numeric: tabular-nums`)

### 6.2 Primitives

- **Eyebrow**: `uppercase tracking-widest text-xs font-medium text-gray-500`
- **Badge chip**: `inline-flex items-center gap-1 rounded-full border border-line px-2 py-0.5 text-xs`; variants: neutral (yrs/area), success (BBB, insured), with Phosphor icon
- **Monogram**: 48px rounded tile, initials, deterministic bg color from name hash — logo fallback
- **Hairline divider**: `border-t border-line`

### 6.3 Components to (re)build

| Component | Change |
|---|---|
| `Nav` | white sticky, ink wordmark + `Maine & NH` location pill, service links, right-side primary CTA |
| `CompanyCard` | rank index, logo/monogram, mono rating row, trust-badge row, generated blurb, hairline footer with phone + CTA, `hover:border-l-4 border-l-blue-700` |
| `Footer` | ink block, 4 columns (services / cities / company / legal), affiliate disclosure, "Updated {date}" |
| `index.astro` (Home) | full build: asymmetric hero with **live preview-card stack** (no stock photo), trust-bar, bento service grid (featured `col-span-2 row-span-2`), top cities, how-it-works, ink CTA band |
| Service hub (`[service]/index.astro`) | eyebrow hero, intro, how-it-works, striped mono cost table, city grid by state, FAQ |
| City-service (`[service]/[city].astro`) | 2-col, sticky sidebar (big mono cost range + CTA), redesigned company list, cost section, how-to-choose, FAQ, nearby cities, breadcrumb |
| Blog (`blog/[slug].astro`, `blog/index.astro`) | editorial `max-w-2xl`, pull-quotes, author/updated date |
| Supporting (`CTASidebar`, `CostSection`, `CostTable`, `CityGrid`, `ServiceHero`, `Breadcrumb`, `FAQAccordion`, `HowToChoose`, `NearbyCities`, blog/* ) | restyle to new tokens/primitives |

### 6.4 Anti-AI-default levers (explicit)

1. Warm paper bg + warm hairline borders (not cold gray, not heavy shadows)
2. Mono tabular numerals for every datum (rating, price, count, phone, years)
3. Uppercase eyebrow kickers + thin rules for section rhythm
4. Asymmetric hero whose right side is a real-data preview, not a stock image
5. Bento service grid with one featured tile (not 6 equal cards)
6. Rank-numbered company cards with real logos/monograms + trust badges

---

## 7. Compliance Checklist (must hold)

- [ ] No em-dash anywhere in rendered content (use comma/colon)
- [ ] Affiliate links `rel="nofollow sponsored"`, CTA text "Get Free Quotes"
- [ ] No verbatim Angi/Maps descriptions (generated blurbs only)
- [ ] No license-number / unverified certification claims
- [ ] `Insured` badge carries `*self-reported` footnote (one per page)
- [ ] Ratings always paired with review count
- [ ] City-service pages with `< 3` companies not generated
- [ ] One `<h1>` per page; heading nesting preserved
- [ ] All internal/canonical hrefs without trailing slash
- [ ] Hero image (preview stack) is LCP-safe; other images `loading="lazy"` + explicit dims
- [ ] Light theme only; CSS-only interactions

## 8. Verification

- `npm run build` succeeds; `npx astro check` clean
- Spot-check: home renders hero+bento; one city page renders enriched cards with badges; cost table mono; FAQ accordion CSS-only
- Confirm a `< 3` company city is absent from output and sitemap
- Grep rendered `dist/` for em-dash → zero hits in content

---

## 9. Open Risks

- `blurb` repetition across cities → mitigate by including city/area variation; acceptable since it is structured, not duplicated marketing prose.
- Logo domain matching imperfect (18% have logo_url, 158 files) → monogram fallback covers the rest.
- `service_area` strings can be long/noisy → truncate + whitelist sane values.
