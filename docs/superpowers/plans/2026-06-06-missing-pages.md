# Missing Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 5 missing pages (/maine, /new-hampshire, /about, /about/editorial-team, /contact) and update Nav + Footer to expose them.

**Architecture:** All pages are static Astro files using the existing `SiteLayout` wrapper. State pages (Maine/NH) pull data from `cities.json` and `services.json` at build time. Contact page embeds a Tally.so iframe. Nav gets a "Locations" `<details>` dropdown + "About" link. Footer gets live geo-links and additional columns.

**Tech Stack:** Astro 5, Tailwind v4, TypeScript strict, JSON data files, Tally.so embed (https://tally.so/r/44zgNA)

---

## File Map

| Action | File | Purpose |
|--------|------|---------|
| Create | `src/pages/maine.astro` | Maine state hub page |
| Create | `src/pages/new-hampshire.astro` | NH state hub page |
| Create | `src/pages/about.astro` | About page (placeholder structure) |
| Create | `src/pages/about/editorial-team.astro` | Author page for blog bylines |
| Create | `src/pages/contact.astro` | Contact page with Tally embed |
| Modify | `src/components/layout/Nav.astro` | Add Locations dropdown + About link + mobile CTA |
| Modify | `src/components/layout/Footer.astro` | Live Coverage links, add About/Contact columns |

---

## Task 1: Maine State Hub Page

**Files:**
- Create: `src/pages/maine.astro`

- [ ] **Step 1: Create `src/pages/maine.astro`**

```astro
---
import SiteLayout from '../layouts/SiteLayout.astro'
import Breadcrumb from '../components/common/Breadcrumb.astro'
import FAQAccordion from '../components/common/FAQAccordion.astro'
import Eyebrow from '../components/common/Eyebrow.astro'
import citiesData from '../data/cities.json'
import servicesData from '../data/services.json'
import type { CityEntry, ServiceEntry } from '../types'

const phase = parseInt(import.meta.env.PUBLIC_PHASE ?? '1')
const services = (servicesData as ServiceEntry[]).filter((s) => s.priority <= phase)
const cities = (citiesData as CityEntry[]).filter(
  (c) => c.state === 'Maine' && c.phase <= phase,
)

const faqs = [
  {
    question: 'What contractor services are available in Maine?',
    answer:
      'CVS Contracting connects Maine homeowners with licensed contractors for foundation repair, basement waterproofing, excavation, and snow removal across 19 cities from Portland to Bangor.',
  },
  {
    question: 'How much do contractor services cost in Maine?',
    answer:
      'Costs vary by service. Basement waterproofing in Maine typically runs $3,000–$10,000. Foundation repair averages $2,000–$15,000. Excavation ranges $1,500–$12,000. Snow removal contracts range $300–$3,000 per season.',
  },
  {
    question: 'Do Maine contractors need to be licensed?',
    answer:
      'Maine requires contractors to be licensed through the Maine Department of Professional and Financial Regulation. Always verify a contractor\'s license before signing a contract.',
  },
  {
    question: 'Which cities in Maine does CVS Contracting cover?',
    answer:
      'We cover 19 Maine cities including Portland, Bangor, Lewiston, Auburn, Augusta, South Portland, Westbrook, Biddeford, and more. Use the city links below to find contractors in your area.',
  },
]
---
<SiteLayout
  title="Contractor Services in Maine"
  description="Find licensed foundation repair, basement waterproofing, excavation, and snow removal contractors across Maine. Compare local companies and get free quotes."
  canonicalUrl="/maine"
>
  <div class="container max-w-4xl py-16">
    <Breadcrumb items={[{ label: 'Home', href: '/' }, { label: 'Maine' }]} />

    <Eyebrow text="Maine" />
    <h1 class="text-3xl md:text-4xl font-bold text-ink tracking-tight mt-2">
      Contractors in Maine
    </h1>
    <p class="text-base text-gray-600 leading-relaxed mt-4 max-w-2xl">
      Find trusted local contractors for home improvement and exterior services across Maine.
      CVS Contracting connects homeowners with licensed, reviewed businesses in 19 cities
      statewide — from Portland and Bangor to smaller communities across the state.
    </p>

    <section class="mt-12">
      <h2 class="text-2xl font-semibold text-ink tracking-tight">Services We Cover in Maine</h2>
      <p class="text-gray-600 mt-2">
        Browse by service to find contractors, compare ratings, and get free quotes.
      </p>
      <ul class="grid grid-cols-1 gap-4 sm:grid-cols-2 mt-6">
        {services.map((s) => (
          <li>
            <a
              href={`/${s.slug}`}
              class="flex flex-col gap-1 rounded-xl border border-line bg-white p-5 hover:border-blue-700 hover:shadow-sm transition-shadow duration-150"
            >
              <span class="text-base font-semibold text-ink">{s.name}</span>
              <span class="text-sm text-gray-500">{s.description}</span>
              <span class="text-xs text-blue-700 mt-1 font-medium">
                Avg cost: ${s.avg_cost_min.toLocaleString()}–${s.avg_cost_max.toLocaleString()}
              </span>
            </a>
          </li>
        ))}
      </ul>
    </section>

    <section class="mt-12">
      <h2 class="text-2xl font-semibold text-ink tracking-tight">Maine Cities We Serve</h2>
      <p class="text-gray-600 mt-2">
        Select your city to browse contractors and compare quotes for any service.
      </p>
      <ul class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 mt-6">
        {cities.map((c) => (
          <li>
            <a
              href={`/basement-waterproofing/${c.slug}`}
              class="block rounded-lg border border-line bg-white px-4 py-3 text-sm text-blue-700 hover:border-blue-700"
            >
              {c.name}
            </a>
          </li>
        ))}
      </ul>
    </section>

    <FAQAccordion faqs={faqs} />
  </div>
</SiteLayout>
```

- [ ] **Step 2: Verify build compiles**

```bash
cd /Users/usara/Desktop/Проекты/Сайты/cvscontracting && npx astro check 2>&1 | tail -20
```
Expected: no TypeScript errors on maine.astro

---

## Task 2: New Hampshire State Hub Page

**Files:**
- Create: `src/pages/new-hampshire.astro`

- [ ] **Step 1: Create `src/pages/new-hampshire.astro`**

```astro
---
import SiteLayout from '../layouts/SiteLayout.astro'
import Breadcrumb from '../components/common/Breadcrumb.astro'
import FAQAccordion from '../components/common/FAQAccordion.astro'
import Eyebrow from '../components/common/Eyebrow.astro'
import citiesData from '../data/cities.json'
import servicesData from '../data/services.json'
import type { CityEntry, ServiceEntry } from '../types'

const phase = parseInt(import.meta.env.PUBLIC_PHASE ?? '1')
const services = (servicesData as ServiceEntry[]).filter((s) => s.priority <= phase)
const cities = (citiesData as CityEntry[]).filter(
  (c) => c.state === 'New Hampshire' && c.phase <= phase,
)

const faqs = [
  {
    question: 'What contractor services are available in New Hampshire?',
    answer:
      'CVS Contracting connects New Hampshire homeowners with licensed contractors for foundation repair, basement waterproofing, excavation, and snow removal across 21 cities from Manchester and Nashua to Concord and Portsmouth.',
  },
  {
    question: 'How much do contractor services cost in New Hampshire?',
    answer:
      'Costs vary by service. Basement waterproofing in New Hampshire typically runs $3,000–$10,000. Foundation repair averages $2,000–$15,000. Excavation ranges $1,500–$12,000. Snow removal contracts range $300–$3,000 per season.',
  },
  {
    question: 'Do New Hampshire contractors need to be licensed?',
    answer:
      'New Hampshire requires contractors to hold appropriate trade licenses through the NH Office of Professional Licensure and Certification. Always ask for proof of license and insurance before work begins.',
  },
  {
    question: 'Which cities in New Hampshire does CVS Contracting cover?',
    answer:
      'We cover 21 New Hampshire cities including Manchester, Nashua, Concord, Dover, Portsmouth, Keene, Laconia, and more. Use the city links below to find contractors near you.',
  },
]
---
<SiteLayout
  title="Contractor Services in New Hampshire"
  description="Find licensed foundation repair, basement waterproofing, excavation, and snow removal contractors across New Hampshire. Compare local companies and get free quotes."
  canonicalUrl="/new-hampshire"
>
  <div class="container max-w-4xl py-16">
    <Breadcrumb items={[{ label: 'Home', href: '/' }, { label: 'New Hampshire' }]} />

    <Eyebrow text="New Hampshire" />
    <h1 class="text-3xl md:text-4xl font-bold text-ink tracking-tight mt-2">
      Contractors in New Hampshire
    </h1>
    <p class="text-base text-gray-600 leading-relaxed mt-4 max-w-2xl">
      Find trusted local contractors for home improvement and exterior services across
      New Hampshire. CVS Contracting connects homeowners with licensed, reviewed businesses
      in 21 cities statewide — from Manchester and Nashua to Concord, Portsmouth, and beyond.
    </p>

    <section class="mt-12">
      <h2 class="text-2xl font-semibold text-ink tracking-tight">Services We Cover in New Hampshire</h2>
      <p class="text-gray-600 mt-2">
        Browse by service to find contractors, compare ratings, and get free quotes.
      </p>
      <ul class="grid grid-cols-1 gap-4 sm:grid-cols-2 mt-6">
        {services.map((s) => (
          <li>
            <a
              href={`/${s.slug}`}
              class="flex flex-col gap-1 rounded-xl border border-line bg-white p-5 hover:border-blue-700 hover:shadow-sm transition-shadow duration-150"
            >
              <span class="text-base font-semibold text-ink">{s.name}</span>
              <span class="text-sm text-gray-500">{s.description}</span>
              <span class="text-xs text-blue-700 mt-1 font-medium">
                Avg cost: ${s.avg_cost_min.toLocaleString()}–${s.avg_cost_max.toLocaleString()}
              </span>
            </a>
          </li>
        ))}
      </ul>
    </section>

    <section class="mt-12">
      <h2 class="text-2xl font-semibold text-ink tracking-tight">New Hampshire Cities We Serve</h2>
      <p class="text-gray-600 mt-2">
        Select your city to browse contractors and compare quotes for any service.
      </p>
      <ul class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 mt-6">
        {cities.map((c) => (
          <li>
            <a
              href={`/basement-waterproofing/${c.slug}`}
              class="block rounded-lg border border-line bg-white px-4 py-3 text-sm text-blue-700 hover:border-blue-700"
            >
              {c.name}
            </a>
          </li>
        ))}
      </ul>
    </section>

    <FAQAccordion faqs={faqs} />
  </div>
</SiteLayout>
```

---

## Task 3: About Page

**Files:**
- Create: `src/pages/about.astro`

Note: Content is placeholder — owner fills in real text. Structure and schema are production-ready.

- [ ] **Step 1: Create `src/pages/about.astro`**

```astro
---
import SiteLayout from '../layouts/SiteLayout.astro'
import Breadcrumb from '../components/common/Breadcrumb.astro'
import Eyebrow from '../components/common/Eyebrow.astro'
---
<SiteLayout
  title="About CVS Contracting"
  description="CVS Contracting helps Maine and New Hampshire homeowners find licensed, reviewed local contractors for foundation repair, waterproofing, excavation, and snow removal."
  canonicalUrl="/about"
>
  <div class="container max-w-3xl py-16">
    <Breadcrumb items={[{ label: 'Home', href: '/' }, { label: 'About' }]} />

    <Eyebrow text="About Us" />
    <h1 class="text-3xl md:text-4xl font-bold text-ink tracking-tight mt-2">
      About CVS Contracting
    </h1>

    <div class="mt-8 space-y-6 text-gray-600 leading-relaxed">
      <p>
        <!-- TODO: Owner fills in — mission of the site, what CVS Contracting does, why it was created -->
        CVS Contracting is a contractor directory and referral service connecting homeowners
        across Maine and New Hampshire with licensed, vetted local businesses for foundation
        repair, basement waterproofing, excavation, and snow removal.
      </p>

      <p>
        <!-- TODO: Owner fills in — how listings work, data sourcing, quality standards -->
        Every listing in our directory is sourced from verified public business data.
        We display real ratings and review counts so you can make an informed decision
        before reaching out to a contractor.
      </p>
    </div>

    <section class="mt-12">
      <h2 class="text-2xl font-semibold text-ink tracking-tight">How It Works</h2>
      <ol class="mt-4 space-y-3 text-gray-600">
        <li class="flex gap-3">
          <span class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-700 text-xs font-bold text-white">1</span>
          <span>Search for your service and city — browse contractor listings with ratings, reviews, and contact info.</span>
        </li>
        <li class="flex gap-3">
          <span class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-700 text-xs font-bold text-white">2</span>
          <span>Click "Get Free Quotes" to request estimates from multiple contractors through our affiliate partners.</span>
        </li>
        <li class="flex gap-3">
          <span class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-700 text-xs font-bold text-white">3</span>
          <span>Compare quotes, check references, and hire the contractor that fits your project and budget.</span>
        </li>
      </ol>
    </section>

    <section class="mt-12">
      <h2 class="text-2xl font-semibold text-ink tracking-tight">Our Editorial Team</h2>
      <div class="mt-4 flex items-start gap-4 rounded-xl border border-line bg-gray-50 p-5">
        <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-blue-700 text-lg font-bold text-white">
          C
        </div>
        <div>
          <p class="font-semibold text-ink">CVS Contracting Editorial Team</p>
          <p class="text-sm text-gray-500 mt-0.5">Home improvement writers covering the Northeast US</p>
          <p class="text-sm text-gray-600 mt-2">
            Our editorial team researches contractor services, cost data, and home improvement
            topics across Maine and New Hampshire. Cost figures are sourced from HomeAdvisor,
            Angi, and Thumbtack regional data.
          </p>
          <a href="/about/editorial-team" class="text-sm text-blue-700 hover:underline mt-2 inline-block">
            View author profile
          </a>
        </div>
      </div>
    </section>

    <section class="mt-12">
      <h2 class="text-2xl font-semibold text-ink tracking-tight">Contact & Questions</h2>
      <p class="text-gray-600 mt-2">
        Have a question or feedback? <a href="/contact" class="text-blue-700 hover:underline">Use our contact form</a>.
        For affiliate and partnership inquiries, see our <a href="/affiliate-disclosure" class="text-blue-700 hover:underline">affiliate disclosure</a>.
      </p>
    </section>
  </div>
</SiteLayout>
```

---

## Task 4: Author Page (Editorial Team)

**Files:**
- Create: `src/pages/about/editorial-team.astro`

- [ ] **Step 1: Create `src/pages/about/editorial-team.astro`**

```astro
---
import SiteLayout from '../../layouts/SiteLayout.astro'
import Breadcrumb from '../../components/common/Breadcrumb.astro'
import Eyebrow from '../../components/common/Eyebrow.astro'

const schema = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  name: 'CVS Contracting Editorial Team',
  url: 'https://cvscontracting.com/about/editorial-team',
  worksFor: {
    '@type': 'Organization',
    name: 'CVS Contracting',
    url: 'https://cvscontracting.com',
  },
  description:
    'The CVS Contracting Editorial Team covers home improvement, contractor services, and cost guides for Maine and New Hampshire homeowners.',
}
---
<SiteLayout
  title="CVS Contracting Editorial Team"
  description="The CVS Contracting Editorial Team covers contractor services, cost guides, and home improvement topics across Maine and New Hampshire."
  canonicalUrl="/about/editorial-team"
>
  <script is:inline type="application/ld+json" set:html={JSON.stringify(schema)} slot="schema" />

  <div class="container max-w-3xl py-16">
    <Breadcrumb
      items={[
        { label: 'Home', href: '/' },
        { label: 'About', href: '/about' },
        { label: 'Editorial Team' },
      ]}
    />

    <Eyebrow text="Author" />
    <div class="mt-4 flex items-center gap-4">
      <div class="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-blue-700 text-2xl font-bold text-white">
        C
      </div>
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-ink tracking-tight">
          CVS Contracting Editorial Team
        </h1>
        <p class="text-sm text-gray-500 mt-1">Home improvement writers, Northeast US</p>
      </div>
    </div>

    <div class="mt-8 space-y-4 text-gray-600 leading-relaxed">
      <p>
        The CVS Contracting Editorial Team produces cost guides, how-to articles, and
        contractor comparison content for homeowners in Maine and New Hampshire.
      </p>
      <p>
        All cost data referenced in our articles is sourced from HomeAdvisor, Angi, and
        Thumbtack regional averages. Company listings are sourced from verified public
        business data and are never fabricated.
      </p>
      <p>
        Our editorial focus is transactional and local: helping Northeast homeowners make
        informed decisions when hiring contractors for foundation repair, basement
        waterproofing, excavation, and snow removal.
      </p>
    </div>

    <section class="mt-10 border-t border-line pt-8">
      <h2 class="text-xl font-semibold text-ink">Recent Articles</h2>
      <p class="text-sm text-gray-500 mt-2">
        <a href="/blog" class="text-blue-700 hover:underline">Browse all articles</a>
      </p>
    </section>
  </div>
</SiteLayout>
```

---

## Task 5: Contact Page with Tally Embed

**Files:**
- Create: `src/pages/contact.astro`

The Tally form URL is `https://tally.so/r/44zgNA`. Embed URL: `https://tally.so/embed/44zgNA`.

- [ ] **Step 1: Create `src/pages/contact.astro`**

```astro
---
import SiteLayout from '../layouts/SiteLayout.astro'
import Breadcrumb from '../components/common/Breadcrumb.astro'
import Eyebrow from '../components/common/Eyebrow.astro'
---
<SiteLayout
  title="Contact CVS Contracting"
  description="Questions about CVS Contracting, contractor listings, or affiliate partnerships? Send us a message using the contact form below."
  canonicalUrl="/contact"
>
  <div class="container max-w-2xl py-16">
    <Breadcrumb items={[{ label: 'Home', href: '/' }, { label: 'Contact' }]} />

    <Eyebrow text="Contact" />
    <h1 class="text-3xl md:text-4xl font-bold text-ink tracking-tight mt-2">
      Contact Us
    </h1>
    <p class="text-base text-gray-600 leading-relaxed mt-4">
      Have a question about a contractor listing, a correction to report, or a
      partnership inquiry? Use the form below and we'll get back to you.
    </p>

    <div class="mt-10 rounded-xl border border-line bg-gray-50 p-1 overflow-hidden">
      <iframe
        src="https://tally.so/embed/44zgNA?transparentBackground=1&hideTitle=1"
        width="100%"
        height="500"
        frameborder="0"
        marginheight="0"
        marginwidth="0"
        title="Contact form"
        loading="lazy"
      ></iframe>
    </div>

    <p class="mt-6 text-sm text-gray-500">
      For affiliate disclosure questions, see our
      <a href="/affiliate-disclosure" class="text-blue-700 hover:underline">affiliate disclosure page</a>.
    </p>
  </div>
</SiteLayout>
```

---

## Task 6: Update Nav — Locations Dropdown + About Link + Mobile CTA

**Files:**
- Modify: `src/components/layout/Nav.astro`

Current nav: logo | 4 service links | Get Free Quotes button.
Target nav: logo | 4 service links | Locations▾ | About | Get Free Quotes (+ mobile CTA).

- [ ] **Step 1: Replace `src/components/layout/Nav.astro`**

```astro
---
import config from '../../../site.config.ts'
import servicesData from '../../data/services.json'
import citiesData from '../../data/cities.json'
import type { ServiceEntry, CityEntry } from '../../types'
import CTAButton from '../common/CTAButton.astro'

const phase = parseInt(import.meta.env.PUBLIC_PHASE ?? '1')
const services = (servicesData as ServiceEntry[]).filter((s) => s.priority <= phase)

const allCities = citiesData as CityEntry[]
const maineCities = allCities.filter((c) => c.state === 'Maine' && c.phase <= phase).slice(0, 6)
const nhCities = allCities.filter((c) => c.state === 'New Hampshire' && c.phase <= phase).slice(0, 6)
---
<header class="sticky top-0 z-40 border-b border-line bg-paper/90 backdrop-blur">
  <nav class="container flex h-16 items-center justify-between" aria-label="Main">
    <a href="/" class="flex items-center gap-2 text-lg font-bold tracking-tight text-ink">
      {config.brand.name}
      <span class="hidden rounded-full border border-line bg-white px-2 py-0.5 text-xs font-medium text-gray-600 sm:inline">Maine & NH</span>
    </a>

    <!-- Desktop -->
    <ul class="hidden items-center gap-6 md:flex">
      {services.map((s) => (
        <li><a href={`/${s.slug}`} class="text-sm text-gray-700 hover:text-blue-700">{s.name}</a></li>
      ))}

      <!-- Locations dropdown -->
      <li class="relative">
        <details class="group">
          <summary class="flex cursor-pointer list-none items-center gap-1 text-sm text-gray-700 hover:text-blue-700">
            Locations
            <svg class="transition-transform duration-150 group-open:rotate-180" width="12" height="12" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">
              <path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z" />
            </svg>
          </summary>
          <div class="absolute right-0 top-full mt-2 w-72 rounded-xl border border-line bg-white p-4 shadow-lg">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <a href="/maine" class="text-xs font-semibold uppercase tracking-wide text-gray-900 hover:text-blue-700">Maine</a>
                <ul class="mt-2 space-y-1">
                  {maineCities.map((c) => (
                    <li>
                      <a href={`/basement-waterproofing/${c.slug}`} class="text-sm text-gray-600 hover:text-blue-700">{c.name}</a>
                    </li>
                  ))}
                  <li><a href="/maine" class="text-xs text-blue-700 hover:underline mt-1 inline-block">All Maine →</a></li>
                </ul>
              </div>
              <div>
                <a href="/new-hampshire" class="text-xs font-semibold uppercase tracking-wide text-gray-900 hover:text-blue-700">New Hampshire</a>
                <ul class="mt-2 space-y-1">
                  {nhCities.map((c) => (
                    <li>
                      <a href={`/basement-waterproofing/${c.slug}`} class="text-sm text-gray-600 hover:text-blue-700">{c.name}</a>
                    </li>
                  ))}
                  <li><a href="/new-hampshire" class="text-xs text-blue-700 hover:underline mt-1 inline-block">All NH →</a></li>
                </ul>
              </div>
            </div>
          </div>
        </details>
      </li>

      <li><a href="/about" class="text-sm text-gray-700 hover:text-blue-700">About</a></li>

      <li>
        <CTAButton href={services[0] ? `/${services[0].slug}` : '/'} class="px-4 py-2 text-sm">
          {config.affiliate.ctaText}
        </CTAButton>
      </li>
    </ul>

    <!-- Mobile hamburger -->
    <details class="relative md:hidden">
      <summary class="-mr-2 cursor-pointer list-none p-2" aria-label="Open menu">
        <svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" class="text-ink" aria-hidden="true">
          <path d="M224,128a8,8,0,0,1-8,8H40a8,8,0,0,1,0-16H216A8,8,0,0,1,224,128ZM40,72H216a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16ZM216,184H40a8,8,0,0,0,0,16H216a8,8,0,0,0,0-16Z" />
        </svg>
      </summary>
      <ul class="absolute right-0 top-full mt-2 w-64 rounded-xl border border-line bg-white py-2 shadow-md">
        {services.map((s) => (
          <li><a href={`/${s.slug}`} class="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-700">{s.name}</a></li>
        ))}
        <li class="border-t border-line mt-1 pt-1">
          <a href="/maine" class="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-700">Maine</a>
        </li>
        <li>
          <a href="/new-hampshire" class="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-700">New Hampshire</a>
        </li>
        <li class="border-t border-line mt-1 pt-1">
          <a href="/about" class="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-700">About</a>
        </li>
        <li class="px-4 py-3">
          <a
            href={services[0] ? `/${services[0].slug}` : '/'}
            class="block w-full rounded-md bg-blue-700 px-4 py-2 text-center text-sm font-semibold text-white hover:bg-blue-800"
          >
            {config.affiliate.ctaText}
          </a>
        </li>
      </ul>
    </details>
  </nav>
</header>

<style>
  details > summary::-webkit-details-marker { display: none; }
</style>
```

---

## Task 7: Update Footer — Live Locations Links + Columns

**Files:**
- Modify: `src/components/layout/Footer.astro`

Add: About, Contact, Privacy links. Make Maine/NH links live. Add top cities.

- [ ] **Step 1: Replace `src/components/layout/Footer.astro`**

```astro
---
import config from '../../../site.config.ts'
import servicesData from '../../data/services.json'
import type { ServiceEntry } from '../../types'

const phase = parseInt(import.meta.env.PUBLIC_PHASE ?? '1')
const services = (servicesData as ServiceEntry[]).filter((s) => s.priority <= phase)
const year = new Date().getFullYear()
---
<footer class="mt-20 bg-ink text-gray-300">
  <div class="container grid grid-cols-2 gap-8 py-12 md:grid-cols-5">
    <!-- Brand col -->
    <div class="col-span-2 md:col-span-1">
      <p class="text-lg font-bold text-white">{config.brand.name}</p>
      <p class="mt-2 text-sm text-gray-400">Find trusted local contractors across Maine and New Hampshire.</p>
    </div>

    <!-- Services col -->
    <nav aria-label="Footer services">
      <p class="text-sm font-semibold text-white">Services</p>
      <ul class="mt-3 space-y-2 text-sm">
        {services.map((s) => (
          <li><a href={`/${s.slug}`} class="hover:text-white">{s.name}</a></li>
        ))}
      </ul>
    </nav>

    <!-- Locations col -->
    <nav aria-label="Footer locations">
      <p class="text-sm font-semibold text-white">Locations</p>
      <ul class="mt-3 space-y-2 text-sm">
        <li><a href="/maine" class="hover:text-white">Maine</a></li>
        <li><a href="/new-hampshire" class="hover:text-white">New Hampshire</a></li>
        <li class="pt-1 text-xs text-gray-500">Top cities</li>
        <li><a href="/basement-waterproofing/portland-me" class="hover:text-white text-xs">Portland, ME</a></li>
        <li><a href="/basement-waterproofing/bangor-me" class="hover:text-white text-xs">Bangor, ME</a></li>
        <li><a href="/basement-waterproofing/manchester-nh" class="hover:text-white text-xs">Manchester, NH</a></li>
        <li><a href="/basement-waterproofing/nashua-nh" class="hover:text-white text-xs">Nashua, NH</a></li>
      </ul>
    </nav>

    <!-- Resources col -->
    <nav aria-label="Footer resources">
      <p class="text-sm font-semibold text-white">Resources</p>
      <ul class="mt-3 space-y-2 text-sm">
        <li><a href="/blog" class="hover:text-white">Cost Guides</a></li>
      </ul>
    </nav>

    <!-- Company col -->
    <nav aria-label="Footer company">
      <p class="text-sm font-semibold text-white">Company</p>
      <ul class="mt-3 space-y-2 text-sm">
        <li><a href="/about" class="hover:text-white">About</a></li>
        <li><a href="/contact" class="hover:text-white">Contact</a></li>
        <li><a href="/affiliate-disclosure" class="hover:text-white">Affiliate Disclosure</a></li>
      </ul>
    </nav>
  </div>

  <div class="border-t border-white/10">
    <div class="container flex flex-col gap-2 py-6 text-xs text-gray-500 md:flex-row md:items-center md:justify-between">
      <p>&copy; {year} {config.brand.name}. This site may receive compensation when you click affiliate links.</p>
      <p>*Insured status is self-reported by listed businesses.</p>
    </div>
  </div>
</footer>
```

---

## Task 8: Final Build Check

**Files:** None (verification only)

- [ ] **Step 1: Run TypeScript check**

```bash
cd /Users/usara/Desktop/Проекты/Сайты/cvscontracting && npx astro check
```
Expected: 0 errors

- [ ] **Step 2: Run production build**

```bash
cd /Users/usara/Desktop/Проекты/Сайты/cvscontracting && npm run build
```
Expected: Build completes, `dist/` contains `maine/index.html`, `new-hampshire/index.html`, `about/index.html`, `about/editorial-team/index.html`, `contact/index.html`

- [ ] **Step 3: Verify output files exist**

```bash
ls /Users/usara/Desktop/Проекты/Сайты/cvscontracting/dist/maine/ \
   /Users/usara/Desktop/Проекты/Сайты/cvscontracting/dist/new-hampshire/ \
   /Users/usara/Desktop/Проекты/Сайты/cvscontracting/dist/about/ \
   /Users/usara/Desktop/Проекты/Сайты/cvscontracting/dist/about/editorial-team/ \
   /Users/usara/Desktop/Проекты/Сайты/cvscontracting/dist/contact/
```
Expected: each directory contains `index.html`

---

## Self-Review Checklist

- [x] `/maine` — state page, cities filtered by state, FAQ, SEO title/desc, BreadcrumbList via `Breadcrumb` component
- [x] `/new-hampshire` — same pattern as Maine
- [x] `/about` — E-E-A-T structure, links to /about/editorial-team and /contact
- [x] `/about/editorial-team` — Person schema JSON-LD, links to /blog
- [x] `/contact` — Tally embed `https://tally.so/embed/44zgNA`, SiteLayout
- [x] Nav — Locations `<details>` dropdown, About link, mobile CTA added
- [x] Footer — Maine/NH now `<a>` links, 5-column layout, `<nav aria-label>` on each group
- [x] No trailing slashes in any canonical or href
- [x] No TypeScript placeholders — all imports use existing types
- [x] Cities in city grids link to `/basement-waterproofing/{city-slug}` (primary service, same pattern as homepage)
