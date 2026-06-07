# Home Page SEO Optimization — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Maximize SEO authority signals on the home page — fix H1, add geo/cost keywords, wire internal links to `/maine` and `/new-hampshire`, add States section, Blog Preview, FAQ with FAQPage schema.

**Architecture:** All changes confined to `src/pages/index.astro` and `src/components/schema/OrganizationSchema.astro`. No new components — `FAQAccordion` and the existing blog content collection are reused. FAQ data defined once in `index.astro` frontmatter and passed to both the UI component and the schema component.

**Tech Stack:** Astro 5, Tailwind v4, TypeScript strict, JSON data files, `astro:content` for blog collection.

---

## File Map

| File | Action | What changes |
|------|--------|-------------|
| `src/components/schema/OrganizationSchema.astro` | Modify | Accept optional `faqs` prop; push FAQPage into `@graph` when provided |
| `src/pages/index.astro` | Modify | Meta description, H1, intro para, Grid H2, card cost ranges, States section, Top Cities H2 + link fix + CTAs, How It Works H2, Blog Preview section, FAQ section, CTA Band H2 |

---

## Task 1: OrganizationSchema — add FAQPage support

**Files:**
- Modify: `src/components/schema/OrganizationSchema.astro`

- [ ] **Step 1: Confirm current file**

  Run: `cat -n src/components/schema/OrganizationSchema.astro`
  Expected: file has no Props interface, `@graph` contains Organization + WebSite only.

- [ ] **Step 2: Rewrite OrganizationSchema.astro**

  Replace entire file with:

  ```astro
  ---
  import config from '../../../site.config.ts'

  interface Props {
    faqs?: Array<{ question: string; answer: string }>
  }

  const { faqs } = Astro.props

  const siteUrl = (import.meta.env.SITE_URL ?? config.seo.siteUrl).replace(/\/$/, '')

  const graph: object[] = [
    {
      '@type': 'Organization',
      name: config.brand.name,
      url: siteUrl,
      logo: siteUrl + config.brand.logo,
      description: config.seo.defaultDescription,
    },
    {
      '@type': 'WebSite',
      url: siteUrl,
      name: config.brand.name,
    },
  ]

  if (faqs && faqs.length > 0) {
    graph.push({
      '@type': 'FAQPage',
      mainEntity: faqs.map((f) => ({
        '@type': 'Question',
        name: f.question,
        acceptedAnswer: {
          '@type': 'Answer',
          text: f.answer,
        },
      })),
    })
  }

  const schema = {
    '@context': 'https://schema.org',
    '@graph': graph,
  }
  ---
  <script is:inline type="application/ld+json" set:html={JSON.stringify(schema)} />
  ```

- [ ] **Step 3: Build to verify no TypeScript errors**

  Run: `npm run build 2>&1 | tail -20`
  Expected: build succeeds, no errors mentioning `OrganizationSchema`.

- [ ] **Step 4: Commit**

  ```bash
  git add src/components/schema/OrganizationSchema.astro
  git commit -m "feat(schema): add optional FAQPage support to OrganizationSchema"
  ```

---

## Task 2: Meta description + Hero copy

**Files:**
- Modify: `src/pages/index.astro` lines 32–57

- [ ] **Step 1: Add meta description to SiteLayout opening tag**

  Find:
  ```astro
  <SiteLayout title="Contractor Services in Maine & Northeast US">
  ```
  Replace with:
  ```astro
  <SiteLayout
    title="Contractor Services in Maine & Northeast US"
    description="Find trusted foundation repair, basement waterproofing, excavation, and snow removal contractors in Maine and New Hampshire. Compare local companies, get free quotes. Avg cost: $300–$15,000."
  >
  ```

- [ ] **Step 2: Rewrite H1**

  Find:
  ```astro
          Find trusted local contractors, compare quotes free
  ```
  Replace with:
  ```astro
          Trusted Contractor Services in Maine & New Hampshire
  ```

- [ ] **Step 3: Replace intro paragraph**

  Find:
  ```astro
          <p class="mt-4 max-w-xl text-lg text-gray-600 leading-relaxed">
            Vetted foundation, waterproofing, excavation, and snow removal pros across ME and NH. Real ratings, no obligation.
          </p>
  ```
  Replace with:
  ```astro
          <p class="mt-4 max-w-xl text-lg text-gray-600 leading-relaxed">
            CVS Contracting connects Maine and New Hampshire homeowners with vetted local contractors for foundation repair, basement waterproofing, excavation, and snow removal. Browse real ratings across 40+ cities — from Portland and Bangor, ME to Manchester and Concord, NH. Average costs range from $300 for snow removal to $15,000 for foundation work.
          </p>
  ```

- [ ] **Step 4: Build to verify**

  Run: `npm run build 2>&1 | tail -10`
  Expected: build succeeds.

- [ ] **Step 5: Commit**

  ```bash
  git add src/pages/index.astro
  git commit -m "feat(home): add meta description, rewrite H1 + hero intro for geo/service keywords"
  ```

---

## Task 3: Service Grid — H2 + cost range on non-featured cards

**Files:**
- Modify: `src/pages/index.astro` lines 85–112

- [ ] **Step 1: Rewrite Service Grid H2**

  Find:
  ```astro
      <h2 class="mt-2 text-3xl font-semibold tracking-tight text-ink">Browse by service</h2>
  ```
  Replace with:
  ```astro
      <h2 class="mt-2 text-3xl font-semibold tracking-tight text-ink">Contractor Services in Maine & New Hampshire</h2>
  ```

- [ ] **Step 2: Add cost range to non-featured cards**

  Find:
  ```astro
        {rest.map((s) => (
          <a href={`/${s.slug}`} class="group flex flex-col justify-between rounded-2xl border border-line bg-white p-6 hover:border-blue-700">
            <h3 class="text-lg font-semibold text-ink">{s.name}</h3>
            <div class="mt-4 flex items-center gap-3 text-sm text-gray-500">
              <span><span class="num font-semibold text-gray-900">{counts[s.slug] ?? 0}</span> pros</span>
              <span class="ml-auto font-medium text-blue-700 group-hover:underline">View &rarr;</span>
            </div>
          </a>
        ))}
  ```
  Replace with:
  ```astro
        {rest.map((s) => (
          <a href={`/${s.slug}`} class="group flex flex-col justify-between rounded-2xl border border-line bg-white p-6 hover:border-blue-700">
            <h3 class="text-lg font-semibold text-ink">{s.name}</h3>
            <div class="mt-4 flex items-center gap-3 text-sm text-gray-500">
              <span><span class="num font-semibold text-gray-900">{counts[s.slug] ?? 0}</span> pros</span>
              <span class="num">{usd(s.avg_cost_min)}&ndash;{usd(s.avg_cost_max)}</span>
              <span class="ml-auto font-medium text-blue-700 group-hover:underline">View &rarr;</span>
            </div>
          </a>
        ))}
  ```

- [ ] **Step 3: Build to verify**

  Run: `npm run build 2>&1 | tail -10`
  Expected: build succeeds.

- [ ] **Step 4: Commit**

  ```bash
  git add src/pages/index.astro
  git commit -m "feat(home): rewrite service grid H2, add cost ranges to non-featured cards"
  ```

---

## Task 4: States Section (new) — data prep + HTML

**Files:**
- Modify: `src/pages/index.astro` (frontmatter + template)

- [ ] **Step 1: Add per-state data prep to frontmatter**

  In the frontmatter, the current company loading loop is:
  ```astro
  const counts: Record<string, number> = {}
  let preview: CompanyEntry[] = []
  for (const s of services) {
    const mod = await import(`../data/companies/${s.slug}.json`).catch(() => ({ default: [] }))
    const list = mod.default as CompanyEntry[]
    counts[s.slug] = list.length
    if (s.slug === 'basement-waterproofing') preview = list.slice(0, 3)
  }
  ```

  Replace with:
  ```astro
  const meCitySlugs = new Set(cities.filter((c) => c.state_abbr === 'ME').map((c) => c.slug))
  const nhCitySlugs = new Set(cities.filter((c) => c.state_abbr === 'NH').map((c) => c.slug))
  const stateCounts: Record<string, number> = { ME: 0, NH: 0 }
  const counts: Record<string, number> = {}
  let preview: CompanyEntry[] = []
  for (const s of services) {
    const mod = await import(`../data/companies/${s.slug}.json`).catch(() => ({ default: [] }))
    const list = mod.default as CompanyEntry[]
    counts[s.slug] = list.length
    if (s.slug === 'basement-waterproofing') preview = list.slice(0, 3)
    for (const company of list) {
      if (meCitySlugs.has(company.city_slug)) stateCounts.ME++
      else if (nhCitySlugs.has(company.city_slug)) stateCounts.NH++
    }
  }
  ```

  Also add after the `topCities` line:
  ```astro
  const maineCityCount = cities.filter((c) => c.state_abbr === 'ME').length
  const nhCityCount = cities.filter((c) => c.state_abbr === 'NH').length
  ```

- [ ] **Step 2: Insert States Section in template after SERVICE BENTO section**

  Find the closing tag of the SERVICE BENTO section:
  ```astro
    </section>

    <!-- TOP CITIES -->
  ```
  Replace with:
  ```astro
    </section>

    <!-- STATES -->
    <section class="border-y border-line bg-tint">
      <div class="container py-16">
        <Eyebrow text="Where we operate" />
        <h2 class="mt-2 text-3xl font-semibold tracking-tight text-ink">Services by State</h2>
        <div class="mt-8 grid gap-4 sm:grid-cols-2">
          <a href="/maine" class="group flex flex-col justify-between rounded-2xl border border-line bg-white p-6 hover:border-blue-700">
            <div>
              <h3 class="text-xl font-semibold text-ink">Maine Contractors</h3>
              <p class="mt-2 text-sm text-gray-500">
                <span class="num font-semibold text-gray-900">{maineCityCount}</span> cities &middot;
                <span class="num font-semibold text-gray-900">{stateCounts.ME}</span> contractors
              </p>
            </div>
            <span class="mt-6 block text-sm font-medium text-blue-700 group-hover:underline">View Maine &rarr;</span>
          </a>
          <a href="/new-hampshire" class="group flex flex-col justify-between rounded-2xl border border-line bg-white p-6 hover:border-blue-700">
            <div>
              <h3 class="text-xl font-semibold text-ink">New Hampshire Contractors</h3>
              <p class="mt-2 text-sm text-gray-500">
                <span class="num font-semibold text-gray-900">{nhCityCount}</span> cities &middot;
                <span class="num font-semibold text-gray-900">{stateCounts.NH}</span> contractors
              </p>
            </div>
            <span class="mt-6 block text-sm font-medium text-blue-700 group-hover:underline">View New Hampshire &rarr;</span>
          </a>
        </div>
      </div>
    </section>

    <!-- TOP CITIES -->
  ```

- [ ] **Step 3: Build to verify**

  Run: `npm run build 2>&1 | tail -10`
  Expected: build succeeds.

- [ ] **Step 4: Commit**

  ```bash
  git add src/pages/index.astro
  git commit -m "feat(home): add States section linking /maine and /new-hampshire with city + contractor counts"
  ```

---

## Task 5: Top Cities — H2 rewrite + link bug fix + state CTAs

**Files:**
- Modify: `src/pages/index.astro` lines 114–128

- [ ] **Step 1: Rewrite Top Cities H2**

  Find:
  ```astro
        <h2 class="mt-2 text-3xl font-semibold tracking-tight text-ink">Top cities</h2>
  ```
  Replace with:
  ```astro
        <h2 class="mt-2 text-3xl font-semibold tracking-tight text-ink">Top Cities in Maine & New Hampshire</h2>
  ```

- [ ] **Step 2: Fix rotating-service link bug**

  Find:
  ```astro
          <a href={`/${services[i % services.length]?.slug}/${c.slug}`} class="rounded-lg border border-line bg-white px-4 py-3 text-sm hover:border-blue-700">
  ```
  Replace with:
  ```astro
          <a href={`/basement-waterproofing/${c.slug}`} class="rounded-lg border border-line bg-white px-4 py-3 text-sm hover:border-blue-700">
  ```
  Note: `i` is no longer referenced; remove it from the `.map` callback:
  Find:
  ```astro
          {topCities.map((c, i) => (
  ```
  Replace with:
  ```astro
          {topCities.map((c) => (
  ```

- [ ] **Step 3: Add state CTAs below city grid**

  Find (closing of TOP CITIES section):
  ```astro
        </div>
      </div>
    </section>

    <!-- HOW IT WORKS -->
  ```
  Replace with:
  ```astro
        </div>
        <div class="mt-6 flex flex-wrap gap-6">
          <a href="/maine" class="text-sm font-medium text-blue-700 hover:underline">View all Maine cities &rarr;</a>
          <a href="/new-hampshire" class="text-sm font-medium text-blue-700 hover:underline">View all New Hampshire cities &rarr;</a>
        </div>
      </div>
    </section>

    <!-- HOW IT WORKS -->
  ```

- [ ] **Step 4: Build to verify**

  Run: `npm run build 2>&1 | tail -10`
  Expected: build succeeds.

- [ ] **Step 5: Commit**

  ```bash
  git add src/pages/index.astro
  git commit -m "fix(home): correct city card links to /basement-waterproofing/{city}; add state CTAs; rewrite Top Cities H2"
  ```

---

## Task 6: Prose H2 rewrites — How It Works + CTA Band

**Files:**
- Modify: `src/pages/index.astro` lines 131–160

- [ ] **Step 1: Rewrite How It Works H2**

  Find:
  ```astro
      <h2 class="mt-2 text-3xl font-semibold tracking-tight text-ink">Three steps to quotes</h2>
  ```
  Replace with:
  ```astro
      <h2 class="mt-2 text-3xl font-semibold tracking-tight text-ink">How to Find a Contractor in Maine or New Hampshire</h2>
  ```

- [ ] **Step 2: Rewrite CTA Band H2**

  Find:
  ```astro
          <h2 class="text-2xl font-semibold text-white">Ready to compare local contractors?</h2>
  ```
  Replace with:
  ```astro
          <h2 class="text-2xl font-semibold text-white">Find Vetted Foundation & Waterproofing Contractors in Maine & NH</h2>
  ```

- [ ] **Step 3: Build to verify**

  Run: `npm run build 2>&1 | tail -10`
  Expected: build succeeds.

- [ ] **Step 4: Commit**

  ```bash
  git add src/pages/index.astro
  git commit -m "feat(home): rewrite How It Works and CTA Band H2 with geo keywords"
  ```

---

## Task 7: Blog Preview section (new)

**Files:**
- Modify: `src/pages/index.astro`

- [ ] **Step 1: Add getCollection import to frontmatter**

  Find the existing imports at the top of the frontmatter:
  ```astro
  import SiteLayout from '../layouts/SiteLayout.astro'
  ```
  Add before it:
  ```astro
  import { getCollection } from 'astro:content'
  ```

- [ ] **Step 2: Add blog data fetch to frontmatter**

  Find at the end of the frontmatter data section (after the `today` line):
  ```astro
  const today = new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
  ```
  Add after it:
  ```astro
  const blogPosts = await getCollection('blog')
  const featuredPost = blogPosts.find((p) => p.id === 'basement-waterproofing-cost-guide')
  ```

- [ ] **Step 3: Insert Blog Preview section in template after HOW IT WORKS, before CTA BAND**

  Find:
  ```astro
    <!-- CTA BAND -->
  ```
  Insert before it:
  ```astro
    <!-- BLOG PREVIEW -->
    {featuredPost && (
      <section class="border-b border-line">
        <div class="container py-16">
          <Eyebrow text="Resources" />
          <h2 class="mt-2 text-3xl font-semibold tracking-tight text-ink">Contractor Cost Guides</h2>
          <div class="mt-8 max-w-xl">
            <a href="/blog/basement-waterproofing-cost-guide" class="group block rounded-2xl border border-line bg-white p-6 hover:border-blue-700">
              <h3 class="text-lg font-semibold text-ink group-hover:text-blue-700">{featuredPost.data.title}</h3>
              <p class="mt-2 text-sm text-gray-600 leading-relaxed">{featuredPost.data.description}</p>
              <span class="mt-4 block text-sm font-medium text-blue-700">Read guide &rarr;</span>
            </a>
          </div>
          <a href="/blog" class="mt-6 block text-sm font-medium text-blue-700 hover:underline">See all guides &rarr;</a>
        </div>
      </section>
    )}

    <!-- CTA BAND -->
  ```

- [ ] **Step 4: Build to verify**

  Run: `npm run build 2>&1 | tail -10`
  Expected: build succeeds. If blog collection not configured, error will mention `getCollection` — check `src/content/config.ts`.

- [ ] **Step 5: Commit**

  ```bash
  git add src/pages/index.astro
  git commit -m "feat(home): add Blog Preview section linking to basement waterproofing cost guide"
  ```

---

## Task 8: FAQ section + OrganizationSchema wiring

**Files:**
- Modify: `src/pages/index.astro`

- [ ] **Step 1: Add FAQAccordion import**

  In frontmatter imports, add:
  ```astro
  import FAQAccordion from '../components/common/FAQAccordion.astro'
  ```

- [ ] **Step 2: Define homeFaqs array in frontmatter**

  After the `featuredPost` line (end of data section), add:
  ```astro
  const homeFaqs = [
    {
      question: 'What contractor services does CVS Contracting offer?',
      answer:
        'CVS Contracting lists vetted contractors for foundation repair, basement waterproofing, excavation, and snow removal across Maine and New Hampshire.',
    },
    {
      question: 'How much does foundation repair cost in Maine?',
      answer:
        'Foundation repair in Maine typically costs $2,000–$15,000, with an average of $7,000. Factors include crack type, underpinning requirements, and wall stabilization.',
    },
    {
      question: 'How much does basement waterproofing cost in New Hampshire?',
      answer:
        'Basement waterproofing in New Hampshire typically costs $3,000–$10,000, with an average of $6,000. Factors include interior vs. exterior approach, sump pump installation, and encapsulation.',
    },
    {
      question: 'Which cities in Maine and New Hampshire do you serve?',
      answer:
        'CVS Contracting covers 40+ cities including Portland, Bangor, Lewiston, and Auburn in Maine, and Manchester, Concord, Nashua, and Dover in New Hampshire.',
    },
    {
      question: 'Are the contractors on CVS Contracting licensed and insured?',
      answer:
        "We list vetted local contractors. Always verify a contractor's license with the Maine Department of Professional & Financial Regulation or the New Hampshire Office of Professional Licensure and Certification (OPLC) before hiring.",
    },
  ]
  ```

- [ ] **Step 3: Pass faqs prop to OrganizationSchema**

  Find:
  ```astro
    <OrganizationSchema slot="schema" />
  ```
  Replace with:
  ```astro
    <OrganizationSchema slot="schema" faqs={homeFaqs} />
  ```

- [ ] **Step 4: Insert FAQ section in template after BLOG PREVIEW, before CTA BAND**

  Find:
  ```astro
    <!-- CTA BAND -->
  ```
  Insert before it:
  ```astro
    <!-- FAQ -->
    <section class="border-b border-line">
      <div class="container py-16">
        <Eyebrow text="Common questions" />
        <FAQAccordion faqs={homeFaqs} />
      </div>
    </section>

    <!-- CTA BAND -->
  ```

- [ ] **Step 5: Build to verify**

  Run: `npm run build 2>&1 | tail -10`
  Expected: build succeeds, no TS errors.

- [ ] **Step 6: Validate output contains FAQPage schema**

  Run: `grep -c 'FAQPage' dist/index.html`
  Expected: `1`

- [ ] **Step 7: Commit**

  ```bash
  git add src/pages/index.astro
  git commit -m "feat(home): add FAQ section with FAQPage schema wired through OrganizationSchema"
  ```

---

## Task 9: Final build + sanity checks

- [ ] **Step 1: Full build**

  Run: `npm run build 2>&1 | tail -20`
  Expected: exits 0, no warnings.

- [ ] **Step 2: Verify meta description in output**

  Run: `grep -o 'name="description" content="[^"]*"' dist/index.html`
  Expected: contains "Find trusted foundation repair, basement waterproofing..."

- [ ] **Step 3: Verify H1**

  Run: `grep -o '<h1[^>]*>[^<]*</h1>' dist/index.html`
  Expected: "Trusted Contractor Services in Maine & New Hampshire"

- [ ] **Step 4: Verify /maine and /new-hampshire links exist**

  Run: `grep -c 'href="/maine"' dist/index.html && grep -c 'href="/new-hampshire"' dist/index.html`
  Expected: each returns `2` or more (States section + city CTA).

- [ ] **Step 5: Verify city links use consistent service**

  Run: `grep 'href="/basement-waterproofing/' dist/index.html | wc -l`
  Expected: 12 (one per top city card).
  Run: `grep 'href="/' dist/index.html | grep -v 'basement-waterproofing\|/maine\|/new-hampshire\|/blog\|/foundation\|/snow\|/excavation\|/concrete\|/french' | head -5`
  Expected: no unexpected service rotations in city links.

- [ ] **Step 6: Final commit (if any unstaged)**

  ```bash
  git status
  # if clean, nothing to do
  ```

---

## Self-Review: Spec vs Plan

| Spec requirement | Task |
|-----------------|------|
| Meta description explicit prop | Task 2 Step 1 |
| H1 geo rewrite | Task 2 Step 2 |
| Intro paragraph with services + cities + cost range | Task 2 Step 3 |
| Service Grid H2 rewrite | Task 3 Step 1 |
| Non-featured card cost range | Task 3 Step 2 |
| States Section with /maine + /new-hampshire links | Task 4 |
| Top Cities H2 rewrite | Task 5 Step 1 |
| City link bug fix (consistent service) | Task 5 Step 2 |
| State CTAs below city grid | Task 5 Step 3 |
| How It Works H2 rewrite | Task 6 Step 1 |
| CTA Band H2 rewrite | Task 6 Step 2 |
| Blog Preview section | Task 7 |
| FAQ section with FAQAccordion | Task 8 Step 4 |
| FAQPage schema in OrganizationSchema @graph | Tasks 1 + 8 Steps 2–3 |
| No BreadcrumbList on home | Not implemented (correct — out of scope) |
| Internal linking audit targets all met | States (Task 4), Cities (Task 5), Blog (Task 7) |
