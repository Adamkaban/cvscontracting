# Data Rules — CVS Contracting

## Data Sources

- **Companies**: Outscraper (Google Maps) → `scripts/normalize.ts` → `src/data/companies/[service-slug].json`
- **Cities**: Manual, US Census (population) + Google Maps (coords) → `src/data/cities.json`
- **Services**: Manual → `src/data/services.json`

## File Locations

```
src/data/
├── cities.json
├── services.json
└── companies/
    ├── basement-waterproofing.json
    ├── foundation-repair.json
    ├── snow-removal.json
    ├── excavation-contractors.json
    ├── concrete-contractors.json
    └── french-drain-installation.json
```

## Schemas

### cities.json
```typescript
{ name, state, state_abbr, slug, county, population, lat, lng, nearby_cities: string[], phase: 1|2|3 }
```
Slug: `${name.toLowerCase().replace(/\s+/g, '-')}-${state_abbr.toLowerCase()}` — "South Portland" → `south-portland-me`
`nearby_cities`: slugs only, not names.

### services.json
```typescript
{ name, slug, description, avg_cost_min, avg_cost_max, lead_value_min, lead_value_max, affiliate_url, priority: 1|2, keywords: string[] }
```

### companies/[service-slug].json
```typescript
{ name, slug, city_slug, service_slug, address, zip, phone, rating, review_count, google_maps_url,
  claimed?: boolean, website?: string, years_in_business?: number, featured?: boolean }
```

## Normalization Script

```bash
npx ts-node scripts/normalize.ts --input outscraper-export.csv --service basement-waterproofing
```

Rules:
1. Filter: rating >= 3.5 AND review_count >= 3 (pop < 10k: review_count >= 1 acceptable)
2. Deduplicate by phone
3. Normalize phone: `(207) 555-0100` format
4. Extract zip from address (last 5-digit sequence)
5. Generate slug from name
6. Map city name → city_slug (must match cities.json exactly)
7. Strip Outscraper metadata fields not in schema

## Data Quality Rules

- **Min 3 companies per city-service** — fewer → exclude from `getStaticPaths` entirely (noindex wastes crawl budget)
- Small city (pop < 10k): min 1 at rating >= 3.5 → page generated but noindex until 3+ added
- Only show rating >= 3.5
- Never fabricate company data — Outscraper only
- Address must include street + city + state + zip

## Slug Generation

```typescript
name.toLowerCase().replace(/[^a-z0-9\s-]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-').trim()
// "Aqua-Guard Waterproofing LLC" → "aqua-guard-waterproofing-llc"
```

## Phase Rollout

| Phase | States | Cities | Services |
|-------|--------|--------|---------|
| 1 | ME, NH | 40–50 | basement-waterproofing, foundation-repair, snow-removal, excavation-contractors |
| 2 | VT, MA, CT, RI | 150+ | + concrete-contractors, french-drain-installation, septic-system, land-clearing |
| 3 | upstate NY | 200+ | all services + company profiles |

Build filter: `cities.filter(c => c.phase <= CURRENT_PHASE)` via `PUBLIC_PHASE` env var.
