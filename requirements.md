# CVS Contracting — Project Requirements

## Domain & Background

| Field | Value |
|-------|-------|
| Domain | cvscontracting.com |
| DR | 6 (Ahrefs) |
| Previous site | CVS Foundations & Excavation — local contractor, Saco, Maine |
| Link profile | Clean — local directories (Yelp, BBB, Yellow Pages), Facebook |
| Topical authority | Construction / contractor niche |
| Acquired | Expired domain purchase |

The domain has existing topical authority in the contractor niche and clean backlinks from a real business. "Contracting" in the domain is a high-value keyword for the niche.

---

## Business Model

**Hybrid lead gen aggregator.**

Priority order:
1. **Affiliate leads** (Angi / HomeAdvisor / Thumbtack) — immediate revenue, zero setup
2. **Direct lead sales** to local contractors — $30–80/lead, activate after traffic starts
3. **Paid listings / "Claim your business"** — $49–99/month, Phase 3
4. **Display ads** (Mediavine) — activate at 10k+ sessions/month

---

## Target Geography

**Phase 1:** Maine + New Hampshire
**Phase 2:** Vermont + Massachusetts + Connecticut + Rhode Island
**Phase 3:** Upstate New York

Rationale: Preserve geo-authority from original Maine site. Northeast = old housing stock (pre-1970), high water tables, 4–5 month winters. Perfect fit for all services.

---

## Services

| Slug | Service | Lead Value | Priority |
|------|---------|-----------|----------|
| `basement-waterproofing` | Basement Waterproofing | $50–150 | P1 — highest revenue |
| `foundation-repair` | Foundation Repair | $40–100 | P1 — domain authority |
| `snow-removal` | Snow Removal | $30–80 | P1 — seasonal, Northeast-specific |
| `excavation-contractors` | Excavation Contractors | $30–70 | P1 — domain history |
| `concrete-contractors` | Concrete Contractors | $25–60 | P2 |
| `french-drain-installation` | French Drain Installation | $30–60 | P2 — adjacent to waterproofing |
| `septic-system` | Septic System | $40–80 | P2 — rural ME/NH/VT, low competition |
| `land-clearing` | Land Clearing | $25–50 | P2 — adjacent to excavation |

---

## Site Architecture

### URL Structure

```
/                                        # Home — all services, Northeast hub
/[service]                               # Service hub (long guide + city list)
/[service]/[city]-[state]                # City-service page (programmatic)
/[service]/[city]-[state]/[company]      # Company profile page (Phase 3)
/blog                                    # Editorial content hub
/blog/[slug]                             # Individual post
/about
/contact
/claim                                   # Claim listing flow (Phase 3, noindex)
```

Note: `trailingSlash: "never"` in astro.config.mjs — all URLs without trailing slash.

### Example URLs
```
/basement-waterproofing
/basement-waterproofing/portland-me
/basement-waterproofing/manchester-nh
/foundation-repair
/foundation-repair/concord-nh
/snow-removal/portland-me
/blog/basement-waterproofing-cost-guide
```

### Page Count Estimate (Phase 1)
- 2 states × ~40 cities × 4 services = **~320 city-service pages**
- 4 service hub pages
- 8 blog posts
- Home + About + Contact
- **Total Phase 1: ~335 pages**

### Phase 2 Full Scale
- 6 states × 200 cities × 6 services = **~1,200 city-service pages**
- Company profiles: ~300–500 pages (if 5–10 companies per city)
- 30+ blog posts

---

## Data Strategy

### Company Data Source
**Outscraper** (outscraper.com) — Google Maps scraper.
- Cost: ~$20–50 for full Northeast dataset
- Output: CSV/JSON with name, address, phone, rating, review count, category

### Data Normalization
Raw Outscraper export → `scripts/normalize.ts` → `/src/data/companies/[service].json`

### Company JSON Schema
```json
{
  "name": "Aqua-Guard Waterproofing",
  "slug": "aqua-guard-waterproofing",
  "city_slug": "portland-me",
  "service_slug": "basement-waterproofing",
  "address": "123 Main St, Portland, ME 04101",
  "zip": "04101",
  "phone": "(207) 555-0100",
  "rating": 4.7,
  "review_count": 48,
  "years_in_business": 12,
  "google_maps_url": "https://maps.google.com/?cid=...",
  "claimed": false
}
```

### City JSON Schema
```json
{
  "name": "Portland",
  "state": "Maine",
  "state_abbr": "ME",
  "slug": "portland-me",
  "county": "Cumberland County",
  "population": 68408,
  "lat": 43.6591,
  "lng": -70.2568,
  "nearby_cities": ["south-portland-me", "westbrook-me", "scarborough-me"],
  "phase": 1
}
```

---

## City-Service Page Requirements

Each page must include:
1. **H1**: `{Service} in {City}, {State}`
2. **Intro paragraph** — unique per city (use variables: county, population tier, climate note)
3. **Company listings** — 5–12 companies from scraped data (name, rating, phone, address)
4. **Cost section** — average cost range for this service in the region
5. **How to choose a contractor** — short section (shared component, not duplicate)
6. **Primary CTA** — "Get Free Quotes from {City} Contractors" → affiliate link
7. **FAQ** — 3–5 questions using city name in answers
8. **Schema** — `LocalBusiness` for each company + `Service` for the page

---

## Service Hub Page Requirements

Each `/[service]` page:
1. Long-form guide (1500–2500 words) — what is the service, when needed, cost, process
2. City index — links to all city pages for that service
3. "How it works" section
4. Average cost table by state
5. Primary CTA
6. Schema: `Service` + `FAQPage`

---

## Blog Content Plan (Phase 1)

| Post | Target Keyword | Word Count | Phase |
|------|---------------|-----------|-------|
| Basement Waterproofing Cost Guide | "basement waterproofing cost" | 2000 | P1 |
| Foundation Repair Cost | "foundation repair cost" | 2000 | P1 |
| How to Choose a Foundation Contractor | "how to choose foundation contractor" | 1500 | P1 |
| Snow Removal Cost Guide | "snow removal cost" | 1500 | P1 |
| Snow Removal Contract vs Per-Visit Pricing in New England | "snow removal contract vs per visit" | 1500 | P1 |
| Signs of Foundation Problems | "signs of foundation problems" | 1500 | P1 |
| Excavation Cost in Maine and New Hampshire | "excavation cost maine" | 1500 | P1 |
| Basement Waterproofing Contractors in Maine: What Homeowners Need to Know | "basement waterproofing contractors maine" | 1500 | P1 |
| French Drain Installation Cost | "french drain cost" | 1500 | P2 |
| Basement Waterproofing vs Encapsulation | "waterproofing vs encapsulation" | 1500 | P2 |

Note: "Waterproofing vs Encapsulation" and "French Drain Cost" moved to P2 — AI Overviews dominate generic comparison/informational queries. P1 blog targets local + transactional angles where AI Overview coverage is weak.

---

## SEO Requirements

### Technical
- Sitemap: auto-generated, submitted to GSC on launch
- Robots.txt: allow all
- Canonical tags on all pages
- Hreflang: not needed (English only)
- Core Web Vitals targets: LCP < 2.5s, CLS < 0.1, INP < 200ms

### Schema per Page Type
| Page | Schema |
|------|--------|
| Home | `Organization`, `WebSite` (with `SearchAction`), `BreadcrumbList` |
| Service hub | `Service`, `FAQPage`, `BreadcrumbList` |
| City-service | `Service`, `LocalBusiness` (per company), `FAQPage`, `BreadcrumbList` |
| Blog post | `Article`, `FAQPage`, `BreadcrumbList` |
| Company profile | `LocalBusiness`, `BreadcrumbList` |

### On-Page SEO Rules
- Title: `{Service} in {City}, {State} | CVS Contracting` (max 60 chars)
- Meta description: include city, state, service, cost range (max 155 chars)
- H1: one per page, must contain primary keyword
- Internal links: each city page links to service hub + 2–3 nearby city pages
- External links: affiliate links with `rel="nofollow sponsored"`

---

## Monetization Implementation

### Phase 1 — Affiliate (Immediate)
- Sign up: Angi Ads Partner, HomeAdvisor Pro, Thumbtack Pro
- CTA button on every city-service page → affiliate deep link for that service + city
- Track via UTM params

### Phase 2 — Direct Leads ($3–6 months)
- Add lead capture form (name, phone, email, project description)
- Send to Zapier → Google Sheet
- Manually sell leads to contractors found via cold email / LinkedIn

### Phase 3 — Claim Listing ($6–12 months)
- Add `/claim` flow — company submits info, pays $49–99/month via Stripe
- Claimed listings get: featured placement, direct phone link, badge, reviews
- Requires Astro SSR mode + database (Turso) + Stripe

---

## Launch Phases

### Phase 1 — Foundation (Weeks 1–3)
- [ ] Sign up for Angi Ads Partner + HomeAdvisor affiliate + Thumbtack (start timer — approval takes 1–2 weeks)
- [ ] Purchase Outscraper data for ME + NH, all 4 P1 services (~$30–50)
- [ ] Init Astro project, Tailwind, Cloudflare Pages
- [ ] Create `cities.json` (ME + NH cities, 40–50 cities)
- [ ] Create `services.json` (4 P1 services)
- [ ] Run `scripts/normalize.ts` → generate company JSON files
- [ ] Build city-service page template (`getStaticPaths` filters by data availability — only generate pages with ≥3 companies)
- [ ] Build service hub template
- [ ] Generate city-service pages (count depends on data coverage)
- [ ] Add `public/robots.txt` (disallow /claim/, include sitemap URL)
- [ ] Add `public/_redirects` (trailing slash 301s)
- [ ] Add `public/[indexnow-key].txt` + submit to Bing IndexNow
- [ ] Add `/affiliate-disclosure` page (FTC requirement)
- [ ] Submit sitemap to GSC
- [ ] Set up Cloudflare Web Analytics
- [ ] Add affiliate CTAs to all city pages

### Phase 2 — Content (Weeks 4–8)
- [ ] Publish 8 blog posts (see content plan)
- [ ] Expand to VT + MA + CT + RI
- [ ] Add 2 more services (concrete, french drain)
- [ ] Internal link audit

### Phase 3 — Monetization (Months 3–6)
- [ ] Add lead capture forms
- [ ] Cold outreach to contractors in ME + NH
- [ ] First direct lead sales

### Phase 4 — Scale (Months 6–12)
- [ ] Build claim listing feature
- [ ] Expand to upstate NY
- [ ] Company profile pages
- [ ] Apply to Mediavine (if 10k+ sessions)
- [ ] Consider domain flip on Flippa/Empire Flippers

---

## KPI Targets

| Metric | Month 3 | Month 6 | Month 9 | Month 12 |
|--------|---------|---------|---------|----------|
| Indexed pages | 200+ | 600+ | 1000+ | 1200+ |
| Organic sessions/mo | 300–500 | 2,000+ | 5,000+ | 8,000+ |
| Affiliate revenue/mo | $30–80 | $300+ | $600+ | $1,000+ |
| Direct lead revenue | $0 | $0 | $300+ | $800+ |
| Total revenue/mo | $30–80 | $300+ | $900+ | $1,800+ |

Notes:
- Month 3 affiliate revenue is conservative: DR 6 + new domain = slow indexing. 300–500 sessions at 1–2% affiliate CTR = realistic.
- Direct lead sales require traffic + outreach — don't start contractor outreach until Month 6 when data on top-converting cities is available.
- Apply to Mediavine only at 10k+ sessions/mo (likely Month 9–10).

---

## Competitive Landscape

| Competitor | DR | Strategy | Weakness |
|-----------|-----|---------|---------|
| Angi.com | 74 | Paid listings | Thin city pages, high bounce |
| HomeAdvisor | 72 | Lead gen | Poor UX, aggressive calls |
| Thumbtack | 68 | Marketplace | Not geo-specific |
| Yelp | 93 | Reviews | Generic, not contractor-focused |
| LocalCity sites | 5–20 | Thin directories | Outdated data |

Gap: No niche site focused specifically on foundation/excavation/waterproofing in Northeast with real company data and quality content.
