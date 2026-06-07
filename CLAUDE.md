# CVS Contracting — Project Rules

## What This Is

Contractor lead gen aggregator at cvscontracting.com.
Niche: foundations, basement waterproofing, excavation, snow removal.
Geo: Northeast USA — Phase 1: Maine + New Hampshire.

## Monetization

- **Affiliate (primary)** — Angi / HomeAdvisor / Thumbtack on every city-service page. `rel="nofollow sponsored"`. CTA: "Get Free Quotes".
- **Direct leads (Phase 2)** — lead capture form → sell to contractors $30–80/lead
- **Claim listing (Phase 3)** — contractors pay $49–99/month

## Tech Stack

Astro 5, static SSG (`output: "static"`), Cloudflare Pages, Tailwind v4 (`@tailwindcss/vite`), TypeScript strict, JSON data files only.

## Commands

```bash
npm run dev
npm run build
npm run preview
npx astro check
```

## Key Files

```
src/data/cities.json                    # city data — single source of truth
src/data/services.json                  # service slugs, cost ranges, affiliate URLs
src/data/companies/[service].json       # scraped company data from Outscraper
src/content/blog/                       # MDX blog posts (1 of 8 written: cost guide)

src/pages/index.astro                   # home
src/pages/[service]/index.astro         # service hub
src/pages/[service]/[city].astro        # programmatic city-service pages
src/pages/[service]/maine.astro         # ME state landing per service
src/pages/[service]/new-hampshire.astro # NH state landing per service
src/pages/maine.astro                   # ME state overview
src/pages/new-hampshire.astro           # NH state overview
src/pages/locations.astro               # all locations index
src/pages/blog/index.astro              # blog index
src/pages/blog/[slug].astro             # blog post
src/pages/about.astro                   # about page
src/pages/about/editorial-team.astro    # author page (E-E-A-T)
src/pages/contact.astro
src/pages/affiliate-disclosure.astro
src/pages/privacy.astro
src/pages/404.astro

src/components/layout/                  # Nav.astro, Footer.astro
src/components/common/                  # Breadcrumb, CTAButton, FAQAccordion, Badge, Eyebrow, Monogram, CookieBanner
src/components/city/                    # CompanyCard, CompanyList, CTASidebar, CostSection, HowToChoose, NearbyCities
src/components/hub/                     # ServiceHero, CityGrid, CostTable, WhenToHire
src/components/blog/                    # BlogHeader, QuickAnswer, CTABox, AuthorBio
src/components/schema/                  # OrganizationSchema, ServiceSchema, LocalBusinessSchema, FAQSchema, ArticleSchema
src/components/seo/                     # SEOHead.astro
src/styles/global.css                   # Tailwind v4 entry point
```

## Services (canonical slugs)

`basement-waterproofing` | `foundation-repair` | `snow-removal` | `excavation-contractors` | `concrete-contractors` | `french-drain-installation`

## Current Phase

**Phase 1:** ME + NH, 40–50 cities, 4 active services, ~320 city pages + service hubs + 8 blog posts (1 written).
Redesign complete. State landing pages built (`/maine`, `/new-hampshire`, `/[service]/maine`, `/[service]/new-hampshire`).
Blog: `basement-waterproofing-cost-guide.mdx` done. 7 posts remaining (see `.claude/rules/content.md`).

## Rules by Domain

- UI/frontend → `.claude/rules/design.md`
- SEO → `.claude/rules/seo.md`
- Content/blog → `.claude/rules/content.md`
- Data/schema → `.claude/rules/data.md`
- Dev setup/Astro → `.claude/rules/dev.md`

## Agents

- Deploy & health check → `.claude/agents/deployer.md`
- SEO & content audit → `.claude/agents/reviewer.md`
- Write blog posts / city content → `.claude/agents/writer.md`

## Rules

- Never re-read `astro.config.mjs`, `src/data/cities.json` more than once per session
- Run `npm run build` at end of task, not mid-task
- Never commit raw Outscraper exports — normalize first via `scripts/normalize.ts`
- Never publish city pages with < 3 companies — exclude from `getStaticPaths` entirely
- Stage files explicitly — never `git add -A`
