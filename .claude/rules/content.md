# Content Rules — CVS Contracting

## E-E-A-T Requirements

Every page must demonstrate Experience, Expertise, Authoritativeness, Trustworthiness.
- City-service pages: real company listings, local cost ranges, county context
- Blog posts: named author, "Last updated" date visible
- Service hubs: process explanations, cost tables, when-to-hire guidance
- Never publish city pages without at least 3 real company listings

---

## City-Service Page Structure (required, in order)

1. **H1**: `{Service} in {City}, {State}`
2. **Intro** (unique per city): mention county name, population tier, regional climate context. Min 30% unique vs other cities — no copy-paste.
3. **H2: Top {Service} Contractors in {City}** — 5–12 companies (name, rating, review count, address, phone). Affiliate CTA after list.
4. **H2: Cost of {Service} in {City}, {State}** — state avg range, price factors, sourced from HomeAdvisor/Angi.
5. **H2: How to Choose a {Service} Contractor** — shared component, 4–5 bullets (license, insurance, references, written estimates).
6. **H2: FAQ** — 3–5 questions, city name in at least 2 answers. Used for FAQPage schema.
7. **Footer**: breadcrumb, nearby cities ("Also serving: ..."), affiliate disclosure.

---

## Service Hub Page Structure (1500–2500 words)

1. **H1**: `{Service} Contractors in Northeast US`
2. Intro: what service is, who needs it, why Northeast
3. **H2: How {Service} Works** — steps, timeline, equipment
4. **H2: Average Cost** — table by state (ME, NH minimum)
5. **H2: When Do You Need {Service}?** — signs/triggers, DIY vs pro
6. **H2: How to Choose a Contractor**
7. **H2: {Service} by City** — grid of city links organized by state
8. **H2: FAQ** — 5–7 questions

---

## Blog Post Structure

Frontmatter:
```mdx
---
title:
description:          # 150–155 chars, keyword + benefit
author: "CVS Contracting Editorial Team"
pubDate: YYYY-MM-DD
updatedDate: YYYY-MM-DD
service: [slug]
category: cost-guide | how-to | comparison
---
```

Author must be a real or consistent persona with a dedicated `/about/[author-slug]` page — Google E-E-A-T requires traceable authorship.

Sections in order:
1. Quick Answer box (TL;DR, 2–3 bullets)
2. H2: Average Cost (lead with numbers)
3. H2: What Affects the Cost (4–6 factors)
4. H2: Cost by State (table)
5. H2: DIY vs Pro OR Vendor Comparison
6. H2: How to Find a Contractor (internal links to city pages)
7. H2: FAQ (3–5 Q&A, FAQPage schema)
8. Author bio: "CVS Contracting Editorial Team covers home improvement and contractor services across Northeast USA."

Rules: lead with concrete numbers, source cost ranges ("According to HomeAdvisor..."), min 3 internal links to city pages + service hub.

---

## Blog Content Priorities (Phase 1)

Bias toward local angles and transactional intent — avoid generic informational topics.

| Post | Target Keyword | Words |
|------|---------------|-------|
| Basement Waterproofing Cost Guide | "basement waterproofing cost" | 2000 |
| Foundation Repair Cost | "foundation repair cost" | 2000 |
| Snow Removal Cost Guide | "snow removal cost per visit" | 1500 |
| Snow Removal Contract vs Per-Visit | "snow removal contract vs per visit" | 1500 |
| Excavation Cost in ME and NH | "excavation cost maine" | 1500 |
| Signs of Foundation Problems | "signs of foundation problems" | 1500 |
| How to Choose a Foundation Contractor | "how to choose foundation contractor" | 1500 |
| Basement Waterproofing in Maine | "basement waterproofing contractors maine" | 1500 |

Phase 2 only (AI Overview risk): "french drain installation cost", "waterproofing vs encapsulation".

---

## What NOT To Do

- No city pages without real company listings
- No copy-paste Google Maps descriptions — rewrite naturally
- No "What is X" posts — AI Overviews dominate
- No ratings without review count
- No fake reviews or fabricated company data
- No identical intros across city pages (min 30% unique)
- No em-dash (—) — use comma or colon
- No generic phrases: "state-of-the-art", "industry-leading", "seamlessly", "robust"
- No cost numbers without citing source
- No specific license/certification claims without verification
- No fabricated stats — only HomeAdvisor, Angi, Thumbtack, US Census
- No specific Maine/NH building codes unless verified from official source
- No "Introduction" H2, no "In conclusion" endings

---

## AI Content Rules

1. Always inject real variables: city, county, state, population tier, cost ranges
2. Verify cost data: cross-reference HomeAdvisor, Angi, Thumbtack
3. Company data: never fabricate — Outscraper only
4. No hallucinated regulations
5. Review cost sections for accuracy before publish
