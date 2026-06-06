# SEO Rules — CVS Contracting

## Google 2026 Context

HCU penalizes thin programmatic pages. Target high-intent local/transactional queries: "foundation repair [city] ME", "basement waterproofing contractors [city] NH". Avoid informational queries — AI Overviews dominate.

---

## Technical SEO

### Performance
- CWV: LCP < 2.5s, CLS < 0.1, INP < 200ms
- Hero: `loading="eager"`, WebP, explicit dimensions — LCP element
- All other images: `loading="lazy" decoding="async"`, explicit dimensions
- No heavy client JS

### Indexability
- Default robots meta: `index, follow` on all pages
- Stub pages not yet ready: `noindex`
- **Don't generate pages with < 3 companies** — exclude from `getStaticPaths`. Noindex stubs waste crawl budget.
- `<html lang="en">`
- Canonical: HTTPS, every page, no trailing slash — `https://cvscontracting.com/[service]/[city]-[state]`

### robots.txt (`public/robots.txt`)
```
User-agent: *
Disallow: /claim/
Sitemap: https://cvscontracting.com/sitemap-index.xml
```

### Sitemap
- `@astrojs/sitemap` generates `sitemap-index.xml` (not `sitemap.xml`)
- Include: city pages, service hubs, blog, home, about, contact
- Exclude: noindex stubs, /claim/
- Submit to GSC after launch

### IndexNow
Generate UUID key → `public/[key].txt`. After sitemap live:
`https://api.indexnow.org/IndexNow?url=https://cvscontracting.com/sitemap-index.xml&key=[key]`

### Affiliate Disclosure
Route `/affiliate-disclosure` required (FTC). Explain Angi/HomeAdvisor/Thumbtack commission. Link in every page footer.

### Redirects
- www→non-www: CF Pages settings
- HTTP→HTTPS: CF automatic

---

## Meta Tags

| Page | Title Pattern | Max |
|------|--------------|-----|
| City-service | `{Service} in {City}, {State} \| CVS Contracting` | 60 |
| Service hub | `{Service} Contractors in Northeast US \| CVS Contracting` | 60 |
| Blog post | `{Post Title} \| CVS Contracting` | 60 |
| Home | `Contractor Services in Maine & Northeast US \| CVS Contracting` | 60 |

Meta description: max 155 chars, include city, state, service keyword, cost range hint.
Example: `Find trusted basement waterproofing contractors in Portland, ME. Compare local companies, read reviews, and get free quotes. Avg cost: $3,000–$10,000.`

---

## Heading Structure

- H1: exactly one per page
- City-service H1: `{Service} in {City}, {State}`
- Service hub H1: `{Service} Contractors in Northeast US`
- H2–H6: nested, no skipping. Company listing: H2. Cost: H2. FAQ: H2.

---

## Schema (JSON-LD only, no microdata)

| Page | Required schemas |
|------|----------------|
| Home | `Organization` + `WebSite` + `BreadcrumbList` |
| Service hub | `Service` + `FAQPage` + `BreadcrumbList` |
| City-service | `Service` + `LocalBusiness` (per company) + `FAQPage` + `BreadcrumbList` |
| Blog post | `Article` + `FAQPage` + `BreadcrumbList` |
| All pages | `BreadcrumbList` (render physically on page too) |

**LocalBusiness** fields per company: `@type`, `name`, `address` (PostalAddress: streetAddress, addressLocality, addressRegion, postalCode), `telephone`, `aggregateRating` (ratingValue, reviewCount).

**Organization** (home): `@type: Organization`, `name: "CVS Contracting"`, `url`, `description`.

**WebSite SearchAction** (home): omit until search functionality exists.

---

## Target Keywords (priority)

1. Local transactional — `basement waterproofing contractors portland me` — highest intent
2. Cost intent — `foundation repair cost maine`, `snow removal prices nh`
3. Near me — `excavation contractors near me`
4. Comparison — mid-funnel blog
5. Informational — avoid (AI Overviews)

---

## Topical Authority Clusters

| Cluster | Hub URL | Blog focus |
|---------|---------|------------|
| Basement Waterproofing | `/basement-waterproofing` | cost guide, DIY vs pro, warning signs |
| Foundation Repair | `/foundation-repair` | cost guide, when to repair |
| Snow Removal | `/snow-removal` | cost guide, contracts vs per-visit |
| Excavation | `/excavation-contractors` | cost guide, site prep |

Each cluster = hub + 30–50 city pages + 1–2 blog posts.

---

## Internal Linking

- City-service page → service hub + 3 nearby city pages
- Service hub → all city pages for that service
- Blog post → 3–5 city pages + service hub
- Home → all service hubs + top cities per service

---

## URL Structure

`trailingSlash: "never"` — all URLs without trailing slash.

```
/[service]                               # Service hub
/[service]/[city]-[state]                # City-service page
/[service]/[city]-[state]/[company-slug] # Company profile (Phase 2)
/blog/[slug]                             # Blog post
/about  /contact  /claim (noindex)
```

Slugs: city = `portland-me`, service = exact canonical slug, company = slugified name.
**Never change URLs after publish.**

---

## Trailing Slash — Permanent Decision

`trailingSlash: "never"` in `astro.config.mjs` — **permanent architectural decision, do not revert.**

Why: Astro generates flat files → CF Pages serves `/service/portland-me` → 200, no internal 307.
With `"always"`: generates `slug/index.html` → CF adds 307 on all no-slash requests + `_redirects` creates infinite loops.

Rules:
- All canonical `href`: no trailing slash
- All internal `href` in `.astro` files: no trailing slash
- `public/_redirects` — 301 inbound trailing-slash URLs:
  ```
  /basement-waterproofing/ /basement-waterproofing 301
  /foundation-repair/ /foundation-repair 301
  /snow-removal/ /snow-removal 301
  /excavation-contractors/ /excavation-contractors 301
  /blog/:slug/ /blog/:slug 301
  /[service]/:city/ /[service]/:city 301
  ```

---

## Affiliate Links

- All affiliate links: `rel="nofollow sponsored"`
- CTA text: "Get Free Quotes" — not "Book Now" or "Hire Now"
- Footer: "This site may receive compensation when you click affiliate links"
- Never cloak affiliate URLs
