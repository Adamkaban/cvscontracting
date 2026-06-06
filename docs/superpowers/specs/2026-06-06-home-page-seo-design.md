# Home Page SEO Optimization — Design Spec

**Date:** 2026-06-06
**Scope:** `src/pages/index.astro` + `src/components/schema/OrganizationSchema.astro`
**Goal:** Maximize SEO signals on the home page without touching city-service pages.

---

## Context

Home page is the **authority hub** — not a money page. Transactional traffic ("basement waterproofing Portland ME") belongs to city-service pages. Home page goals:
1. Pass topical authority signals and PageRank to city-service pages via internal links.
2. Rank for broad hub queries: "contractor services Maine New Hampshire".
3. E-E-A-T trust signals — Google must see this as an authoritative regional aggregator.
4. Serve branded/navigational traffic.

Primary target keyword: `contractor services Maine New Hampshire`

---

## Changes

### 1. Meta Tags

**Title:** No change — already correct per SEO rules:
`Contractor Services in Maine & Northeast US | CVS Contracting`

**Description:** Currently not passed — falls back to config default. Add explicit prop:
```
Find trusted foundation repair, basement waterproofing, excavation, and snow removal contractors in Maine and New Hampshire. Compare local companies, get free quotes. Avg cost: $300–$15,000.
```
(153 chars — within 155-char limit)

---

### 2. Schema

Extend `OrganizationSchema.astro` to include `FAQPage` in the `@graph` array alongside Organization + WebSite. FAQ data passed as prop from `index.astro`.

No BreadcrumbList needed on home (root page — nothing to show visually or in schema).

---

### 3. Section-by-Section Changes

#### HERO (existing — rewrite copy)

**H1 rewrite:**
- Current: `Find trusted local contractors, compare quotes free`
- New: `Trusted Contractor Services in Maine & New Hampshire`
- Rationale: Geographic + service keywords in H1; current has none.

**New intro paragraph** (insert below H1, above pill links):
> CVS Contracting connects Maine and New Hampshire homeowners with vetted local contractors for foundation repair, basement waterproofing, excavation, and snow removal. Browse real ratings across 40+ cities — from Portland and Bangor, ME to Manchester and Concord, NH. Average costs range from $300 for snow removal to $15,000 for foundation work.

Signals: service list, geo names, cost ranges — all in first 250 chars of body copy.

**Pill links:** No change (already link to service hubs).

**Stats line:** No change.

**Right column (live preview):** No change.

---

#### SERVICE GRID (existing — H2 + card costs)

**H2 rewrite:**
- Current: `Browse by service`
- New: `Contractor Services in Maine & New Hampshire`

**Card fix:** All non-featured cards currently show contractor count but no cost range. Add `${s.avg_cost_min.toLocaleString()}–${s.avg_cost_max.toLocaleString()}` line to all cards (featured card already shows it).

---

#### STATES SECTION (new)

Insert after SERVICE GRID, before TOP CITIES.

```
H2: Services by State
Two cards side-by-side (grid-cols-2):
  - Maine → /maine
    "Maine Contractors" + X cities + X contractors + "View Maine →"
  - New Hampshire → /new-hampshire
    "New Hampshire Contractors" + X cities + X contractors + "View New Hampshire →"
```

Data: compute Maine city count + NH city count from `citiesData`. Company counts already in `counts` object.

Rationale: `/maine` and `/new-hampshire` pages exist but are **not linked from home anywhere** — Google cannot discover or attribute authority to them.

---

#### TOP CITIES (existing — H2 + link fix + CTAs)

**H2 rewrite:**
- Current: `Top cities`
- New: `Top Cities in Maine & New Hampshire`

**Link fix (critical bug):**
- Current: `/${services[i % services.length]?.slug}/${c.slug}` — rotates services per city index, produces random URLs
- New: `/basement-waterproofing/${c.slug}` — consistent, highest-value service

**Add state CTAs** below city grid:
```
"View all Maine cities →" → /maine
"View all New Hampshire cities →" → /new-hampshire
```

---

#### HOW IT WORKS (existing — H2 only)

**H2 rewrite:**
- Current: `Three steps to quotes`
- New: `How to Find a Contractor in Maine or New Hampshire`

Step copy: no change.

---

#### BLOG PREVIEW (new — insert after HOW IT WORKS)

```
H2: Contractor Cost Guides
1 card: "Basement Waterproofing Cost Guide" → /blog/basement-waterproofing-cost-guide
  Description: excerpt from post frontmatter description
CTA: "See all guides →" → /blog
```

Import via `getCollection('blog')`, then `find(p => p.id === 'basement-waterproofing-cost-guide')`. Use `post.data.title` and `post.data.description`.

---

#### FAQ (new — insert after BLOG PREVIEW, before CTA BAND)

Use existing `FAQAccordion` component. 5 questions:

| # | Question | Answer summary |
|---|----------|---------------|
| 1 | What contractor services does CVS Contracting offer? | Foundation repair, basement waterproofing, excavation, snow removal across ME + NH |
| 2 | How much does foundation repair cost in Maine? | $2,000–$15,000; avg $7,000. Factors: crack type, underpinning, wall stabilization |
| 3 | How much does basement waterproofing cost in New Hampshire? | $3,000–$10,000; avg $6,000. Factors: interior/exterior, sump pump, encapsulation |
| 4 | Which cities in Maine and New Hampshire do you serve? | 40+ cities: Portland, Bangor, Lewiston, Auburn (ME); Manchester, Concord, Nashua, Dover (NH) |
| 5 | Are the contractors on CVS Contracting licensed and insured? | We list vetted contractors. Always verify license with Maine Dept. of Professional & Financial Regulation / NH Office of Professional Licensure and Certification (OPLC) |

Same FAQ data feeds FAQPage schema.

---

#### CTA BAND (existing — H2 rewrite)

**H2 rewrite:**
- Current: `Ready to compare local contractors?`
- New: `Find Vetted Foundation & Waterproofing Contractors in Maine & NH`

Subtext: no change.

---

## Internal Linking Audit (post-optimization)

| Target page | Linked from home? | How |
|-------------|------------------|-----|
| `/foundation-repair` | Yes | Pill + service card |
| `/basement-waterproofing` | Yes | Pill + service card (featured) + city links |
| `/excavation-contractors` | Yes | Pill + service card |
| `/snow-removal` | Yes | Pill + service card |
| `/maine` | **Yes (new)** | States section + city CTA |
| `/new-hampshire` | **Yes (new)** | States section + city CTA |
| `/blog` | **Yes (new)** | Blog preview CTA |
| `/blog/basement-waterproofing-cost-guide` | **Yes (new)** | Blog preview card |
| City-service pages | Yes (fixed) | Top Cities grid (consistent service) |

---

## Files Modified

1. `src/pages/index.astro` — all section changes
2. `src/components/schema/OrganizationSchema.astro` — add FAQPage support

No new components needed — FAQAccordion already exists.

---

## Out of Scope

- City-service pages
- Service hub pages
- Blog posts
- Nav / Footer
- robots.txt / sitemap
