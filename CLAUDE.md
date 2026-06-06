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
src/data/cities.json              # city data — single source of truth
src/data/services.json            # service slugs, cost ranges, affiliate URLs
src/data/companies/[service].json # scraped company data from Outscraper
src/pages/[service]/[city].astro  # programmatic city-service pages
src/content/blog/                 # MDX blog posts
```

## Services (canonical slugs)

`basement-waterproofing` | `foundation-repair` | `snow-removal` | `excavation-contractors` | `concrete-contractors` | `french-drain-installation`

## Current Phase

**Phase 1:** ME + NH, 40–50 cities, 4 services, ~320 city pages + service hubs + 8 blog posts.

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
