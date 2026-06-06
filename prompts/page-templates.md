# CVS Contracting — Page Templates

**Предусловие:** инфраструктурная база из `prompts/astro-infrastructure.md` уже реализована.
Этот промт добавляет три шаблона страниц и всё что для них нужно.

Стек: Astro 5, Tailwind v4 (`@tailwindcss/vite`), TypeScript strict.
Версии пакетов и команды — в `.claude/rules/dev.md`.

---

## Три шаблона

| Шаблон | URL-паттерн | Источник данных |
|--------|-------------|-----------------|
| City-service | `/[service]/[city]-[state]` | JSON (программный, `getStaticPaths`) |
| Service hub | `/[service]` | Content Collection MDX + `services.json` |
| Blog post | `/blog/[slug]` | Content Collection MDX |

---

## Файловая структура (только этот промт)

```
src/
  content/
    config.ts                              ← Zod-схемы коллекций
    services/
      basement-waterproofing.mdx           ← sample hub content
    blog/
      basement-waterproofing-cost-guide.mdx ← sample blog post
  lib/
    intros.ts                              ← генератор unique intro для city pages
    faqs.ts                                ← генератор FAQ по service+city
  components/
    layout/
      Nav.astro
      Footer.astro
    city/
      CompanyCard.astro
      CompanyList.astro
      CTASidebar.astro
      CostSection.astro
      HowToChoose.astro
      NearbyCities.astro
    hub/
      ServiceHero.astro
      CostTable.astro
      WhenToHire.astro
      CityGrid.astro
    blog/
      BlogHeader.astro
      QuickAnswer.astro
      CTABox.astro
      AuthorBio.astro
    common/
      FAQAccordion.astro                   ← переиспользуется всеми шаблонами
    schema/
      ServiceSchema.astro                  ← добавить к инфраструктуре
      ArticleSchema.astro                  ← добавить к инфраструктуре
  layouts/
    SiteLayout.astro                       ← BaseLayout + Nav + Footer
  pages/
    [service]/
      index.astro                          ← service hub
      [city].astro                         ← city-service (programmatic)
    blog/
      index.astro                          ← blog listing
      [slug].astro                         ← blog post
```

---

## 1. Content Collections — src/content/config.ts

### Коллекция "services" (service hub)

Frontmatter schema через Zod:

```ts
const services = defineCollection({
  type: 'content',
  schema: z.object({
    serviceSlug: z.string(),           // "basement-waterproofing"
    title: z.string(),                 // "Basement Waterproofing Contractors in Northeast US"
    description: z.string().max(155),
    updatedDate: z.coerce.date(),
    howItWorks: z.object({
      steps: z.array(z.string()),      // ["Inspect foundation...", "Install drainage..."]
      timeline: z.string(),            // "1–3 days typical"
    }),
    whenToHire: z.object({
      signs: z.array(z.string()),      // warning signs list
      diyVsPro: z.string(),            // paragraph
    }),
    faqs: z.array(z.object({
      question: z.string(),
      answer: z.string(),              // {cityName} placeholder — заменяется на city
    })),
  }),
})
```

Тело файла (MDX body): полный текстовый гайд 1500–2500 слов. Рендерится как prose.

### Коллекция "blog"

```ts
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().max(155),
    author: z.string(),                // "CVS Contracting Editorial Team"
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date(),
    service: z.string(),               // service slug
    category: z.enum(['cost-guide', 'how-to', 'comparison']),
    ogImage: z.string().optional(),
    faqs: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).optional(),
  }),
})
```

---

## 2. src/lib/intros.ts

Генерирует уникальный intro-параграф для каждой комбинации city × service.
Никаких copy-paste — обязательно использовать все переменные.

```ts
import type { CityEntry, ServiceEntry } from '../types'

export function getPopulationTier(pop: number): string {
  if (pop > 50_000) return 'large city'
  if (pop > 15_000) return 'mid-size city'
  return 'small community'
}

export function getClimateContext(stateAbbr: string): string {
  const map: Record<string, string> = {
    ME: 'harsh Maine winters with freeze-thaw cycles that stress foundations',
    NH: "New Hampshire's cold winters and seasonal frost heave",
  }
  return map[stateAbbr] ?? 'Northeast winters with significant freeze-thaw cycles'
}

export function generateCityIntro(city: CityEntry, service: ServiceEntry): string {
  const tier = getPopulationTier(city.population)
  const climate = getClimateContext(city.state_abbr)
  // Возвращает уникальный параграф, использующий:
  // city.name, city.county, city.state, tier, climate, service.name
  // Минимум 30% уникального текста vs. других городов.
}
```

---

## 3. src/lib/faqs.ts

FAQ-вопросы специфичны для service, ответы инжектируют city.name.
5–7 вопросов на сервис, city.name встречается минимум в 2 ответах.

```ts
export function getCityServiceFAQs(
  city: CityEntry,
  service: ServiceEntry,
): Array<{ question: string; answer: string }> {
  // Возвращает массив FAQ — city.name подставляется в строки ответов.
  // Данные берутся из service-hub content collection (поле faqs[]).
  // Плейсхолдер {cityName} в MDX-файле → заменяется здесь.
}
```

---

## 4. Компоненты

Каждый компонент:
- Данные только через пропсы (не импортирует конфиг напрямую)
- Стили: Tailwind v4 utility классы (не scoped `<style>`)
- Цвета: строго из design.md — `#1D4ED8`, `#15803D`, gray-200/50/900

### src/components/layout/Nav.astro

Без пропсов. Читает `site.config.ts` + `services.json`.

Содержимое:
- Логотип (`config.brand.logo`) слева — ссылка на `/`
- Ссылки на все service hubs по имени
- Мобиль: hamburger меню (CSS only — `<details>/<summary>`, без JS)
- Нет LanguagePicker

### src/components/layout/Footer.astro

Без пропсов. Читает `site.config.ts`.

Содержимое:
- Логотип + copyright
- Ссылки на service hubs
- Ссылка на `/affiliate-disclosure` (обязательно — FTC)
- Disclosure текст: `config.affiliate.footerDisclosure`
- НЕТ: телефонов, адресов, fake "trust badges"

---

### src/components/city/CompanyCard.astro

Пропсы:
```ts
interface Props {
  company: {
    name: string
    address: string
    phone: string | null
    rating: number
    review_count: number
    google_maps_url: string | null
  }
  affiliateUrl: string   // из service.affiliate_url
  affiliateRel: string   // "nofollow sponsored"
}
```

Рендерит точно по спеке из `design.md` — Company Card section:
```
┌─────────────────────────────────────────────┐
│ ★★★★½ 4.7  · 48 reviews                   │
│ Aqua-Guard Waterproofing                    │
│ 123 Main St, Portland, ME 04101            │
│ (207) 555-0100          [Get Free Quotes →] │
└─────────────────────────────────────────────┘
```

- Border: `border border-gray-200 rounded-lg p-4`
- Hover: `hover:border-gray-300 hover:shadow-sm hover:border-l-4 hover:border-l-blue-700`
- Stars: Phosphor `Star`/`StarHalf` icons, 16px, `fill-amber-400 text-amber-400`
- Phone: `font-mono text-gray-700 text-sm`
- CTA: `bg-blue-700 text-white rounded-md px-4 py-2 text-sm` + `rel={affiliateRel}`
- CTA text: всегда "Get Free Quotes" — брать из `config.affiliate.ctaText`

### src/components/city/CompanyList.astro

Пропсы:
```ts
interface Props {
  companies: CompanyEntry[]
  cityName: string
  serviceName: string
  affiliateUrl: string
  affiliateRel: string
}
```

- H2: "Top {serviceName} Contractors in {cityName}"
- Рендерит `CompanyCard` для каждой компании
- После последней карточки: CTA-блок `"Get Free Quotes from {cityName} Contractors"` → affiliate link

### src/components/city/CTASidebar.astro

Пропсы:
```ts
interface Props {
  cityName: string
  costMin: number
  costMax: number
  affiliateUrl: string
  affiliateRel: string
}
```

Из `design.md` — sticky sidebar spec:
- `sticky top-6 bg-white border border-gray-200 rounded-xl p-6 shadow-sm`
- Headline: "Get Free Quotes in {cityName}" — `text-lg font-semibold`
- Cost: `${costMin.toLocaleString()}–${costMax.toLocaleString()}` — `text-2xl font-bold text-gray-900`
- CTA: `w-full bg-blue-700 hover:bg-blue-800 text-white font-semibold rounded-md px-6 py-3`
- Trust line: "Free quotes, no obligation" — `text-xs text-gray-500 text-center mt-2`
- Mobile: нет sticky, показывается выше main-контента (порядок через CSS order)

### src/components/city/CostSection.astro

Пропсы:
```ts
interface Props {
  cityName: string
  stateName: string
  serviceName: string
  costMin: number
  costMax: number
}
```

Структура:
- H2: "Cost of {serviceName} in {cityName}, {stateName}"
- Avg cost range крупным шрифтом
- Маркированный список факторов влияния (4–5 пунктов, специфичных для этого сервиса)
- Disclaimer: "Avg cost data sourced from HomeAdvisor and Angi regional averages."

### src/components/city/HowToChoose.astro

Без пропсов — один компонент для всех городов.
Одинаковый контент = компонент (не дубль-контент).

- H2: "How to Choose a Contractor"
- 4–5 буллетов: лицензия, страховка, references, письменная смета, проверка отзывов
- Без affiliate ссылок внутри

### src/components/city/NearbyCities.astro

Пропсы:
```ts
interface Props {
  nearbySlugList: string[]  // city slugs из city.nearby_cities
  serviceSlug: string
  allCities: CityEntry[]    // для разрешения slug → name
}
```

- Текст: "Also serving nearby areas:"
- Ссылки: `/[serviceSlug]/[citySlug]`
- Рендерит только города у которых `phase <= currentPhase` И есть компании (≥3) для этого сервиса

---

### src/components/common/FAQAccordion.astro

Переиспользуется во всех шаблонах. Пропсы:
```ts
interface Props {
  faqs: Array<{ question: string; answer: string }>
  headingLevel?: 'h2' | 'h3'  // default: 'h2'
}
```

Реализация из `design.md`:
- `<details>/<summary>` — НИКАКОГО JS
- `<summary>`: `flex items-center justify-between cursor-pointer py-4 font-semibold text-gray-900`
- Phosphor `CaretDown` icon, rotate 180° CSS only: `details[open] summary svg { transform: rotate(180deg) }`
- Open state: summary цвет → blue-700
- Ответ: `text-gray-600 pb-4 leading-relaxed`
- Разделитель: `border-t border-gray-200`

---

### src/components/hub/ServiceHero.astro

Пропсы:
```ts
interface Props {
  serviceName: string
  description: string
  costMin: number
  costMax: number
  affiliateUrl: string
  affiliateRel: string
}
```

- H1: "{serviceName} Contractors in Northeast US"
- Subline: description из `services.json`
- Avg cost range заметным шрифтом
- CTA: "Get Free Quotes" → affiliate link

### src/components/hub/CostTable.astro

Пропсы:
```ts
interface Props {
  rows: Array<{ state: string; avgCost: string; range: string }>
}
```

Таблица из `content.md` — по штатам. Striped rows (нечётные: bg-gray-50).
Full-width, responsive (на мобиле — горизонтальный scroll).

### src/components/hub/WhenToHire.astro

Пропсы:
```ts
interface Props {
  signs: string[]
  diyVsPro: string
}
```

- H2: "When Do You Need {serviceName}?"
- Список признаков/симптомов
- Параграф DIY vs pro

### src/components/hub/CityGrid.astro

Пропсы:
```ts
interface Props {
  cities: CityEntry[]
  serviceSlug: string
  groupByState?: boolean  // default: true
}
```

- H2: "{serviceName} by City"
- Сгруппировано по штату (Maine → New Hampshire)
- Grid: `grid-cols-2 md:grid-cols-3 lg:grid-cols-4`
- Ссылки: `/[serviceSlug]/[citySlug]`

---

### src/components/blog/BlogHeader.astro

Пропсы:
```ts
interface Props {
  title: string
  description: string
  author: string
  pubDate: Date
  updatedDate: Date
  category: 'cost-guide' | 'how-to' | 'comparison'
}
```

- H1: title
- Category badge
- Author + "Last updated: {updatedDate}" — **видимо на странице** (E-E-A-T)
- Meta description как subline

### src/components/blog/QuickAnswer.astro

Пропсы: `items: string[]` (2–3 буллета TL;DR)

Стиль: `bg-gray-50 border-l-4 border-blue-700 p-4 rounded-r-lg`
Label: "Quick Answer" — `text-xs font-semibold uppercase text-blue-700`

### src/components/blog/CTABox.astro

Пропсы: `serviceSlug: string; serviceName: string`

Inline CTA box: "Find {serviceName} Contractors in Your City"
Ссылка → `/[serviceSlug]` (service hub)
Стиль: `bg-blue-50 border border-blue-200 rounded-lg p-4`

### src/components/blog/AuthorBio.astro

Пропсы: `author: string`

Внизу поста. "{author} — Home Improvement Expert covering Northeast US."
E-E-A-T requirement.

---

## 5. Schema-компоненты (добавить к инфраструктуре)

### src/components/schema/ServiceSchema.astro

Пропсы:
```ts
interface Props {
  serviceName: string
  cityName?: string        // если есть — areaServed: City; иначе: region Northeast US
  stateAbbr?: string
}
```

```json
{
  "@type": "Service",
  "serviceType": "{serviceName}",
  "areaServed": {
    "@type": "City",
    "name": "{cityName}",
    "addressRegion": "{stateAbbr}"
  },
  "provider": {
    "@type": "Organization",
    "name": "CVS Contracting",
    "url": "https://cvscontracting.com"
  }
}
```

### src/components/schema/ArticleSchema.astro

Пропсы:
```ts
interface Props {
  title: string
  description: string
  author: string
  pubDate: Date
  updatedDate: Date
  url: string
  image?: string
}
```

`@type: "Article"` с `author.@type: "Person"`, `publisher.@type: "Organization"`.

---

## 6. src/layouts/SiteLayout.astro

Расширяет `BaseLayout`. Добавляет Nav + Footer.
Именованный слот `schema` проброшен в BaseLayout.

Пропсы:
```ts
interface Props {
  title: string
  description?: string
  ogImage?: string
  noindex?: boolean
}
```

```astro
---
import BaseLayout from './BaseLayout.astro'
import Nav from '../components/layout/Nav.astro'
import Footer from '../components/layout/Footer.astro'
const props = Astro.props
---
<BaseLayout {...props}>
  <slot name="schema" slot="schema" />
  <Nav />
  <main>
    <slot />
  </main>
  <Footer />
</BaseLayout>
```

---

## 7. src/pages/[service]/[city].astro — City-Service Page

### getStaticPaths

```ts
export async function getStaticPaths() {
  const cities    = (await import('../../data/cities.json')).default
  const services  = (await import('../../data/services.json')).default
  const phase     = parseInt(import.meta.env.PUBLIC_PHASE ?? '1')

  const paths = []

  for (const service of services.filter(s => s.priority <= phase)) {
    const companies = await import(`../../data/companies/${service.slug}.json`)
      .then(m => m.default)
      .catch(() => [])

    for (const city of cities.filter(c => c.phase <= phase)) {
      const cityCompanies = companies.filter(
        (co: CompanyEntry) => co.city_slug === city.slug && co.rating >= 3.5
      )
      // Правило data.md: < 3 компаний — страница не создаётся
      if (cityCompanies.length < 3) continue

      paths.push({
        params: { service: service.slug, city: city.slug },
        props:  { service, city, companies: cityCompanies },
      })
    }
  }

  return paths
}
```

### Структура страницы (из content.md)

```
Breadcrumb: Home > {service.name} > {city.name}, {state_abbr}

H1: {service.name} in {city.name}, {state_abbr}

Intro paragraph — generateCityIntro(city, service)

[2-col layout: 70% main, 30% sticky sidebar]

Main:
  CompanyList (companies, city, service)
  CostSection (city, service, costs)
  HowToChoose
  FAQAccordion (getCityServiceFAQs(city, service))
  NearbyCities (city.nearby_cities, service.slug)

Sidebar:
  CTASidebar (city, costs, affiliateUrl)
  [moves BELOW main on mobile — CSS order]
```

### SEO и Schema

Title: `{service.name} in {city.name}, {state_abbr} | CVS Contracting` — max 60 chars
Description: max 155 chars, включает: city, state, service, avg cost range

Schema в slot="schema":
- `ServiceSchema` (serviceName, cityName, stateAbbr)
- `LocalBusinessSchema` (companies, cityName, stateAbbr)
- `FAQSchema` (getCityServiceFAQs(city, service))
- `Breadcrumb` (рендерит и UI и JSON-LD)

Canonical: `https://cvscontracting.com/{service.slug}/{city.slug}` — без trailing slash

---

## 8. src/pages/[service]/index.astro — Service Hub

### getStaticPaths

```ts
export async function getStaticPaths() {
  const services = (await import('../../data/services.json')).default
  const phase    = parseInt(import.meta.env.PUBLIC_PHASE ?? '1')
  const hubs     = await getCollection('services')  // content collection

  return services
    .filter(s => s.priority <= phase)
    .map(service => ({
      params: { service: service.slug },
      props:  {
        service,
        hubContent: hubs.find(h => h.data.serviceSlug === service.slug),
      },
    }))
}
```

### Структура страницы (из content.md — Service Hub)

```
Breadcrumb: Home > {service.name}

H1: {service.name} Contractors in Northeast US

[MDX body rendered as prose — intro section]

ServiceHero (service metadata)

H2: How {service.name} Works
  [Из hubContent.data.howItWorks]

H2: Average Cost of {service.name}
  CostTable (rows по штатам — ME, NH)

H2: When Do You Need {service.name}?
  WhenToHire (hubContent.data.whenToHire)

H2: How to Choose a Contractor
  HowToChoose (shared component)

H2: {service.name} by City
  CityGrid (cities, service.slug)

H2: FAQ
  FAQAccordion (hubContent.data.faqs — без city injection)
```

### SEO и Schema

Title: `{service.name} Contractors in Northeast US | CVS Contracting`
Schema: `ServiceSchema` + `FAQSchema` + `Breadcrumb`

---

## 9. src/pages/blog/[slug].astro — Blog Post

### getStaticPaths

```ts
export async function getStaticPaths() {
  const posts = await getCollection('blog')
  return posts.map(post => ({
    params: { slug: post.slug },
    props:  { post },
  }))
}
```

### Структура страницы (из content.md — Blog Post)

```
Breadcrumb: Home > Blog > {post.data.title}

BlogHeader (title, author, pubDate, updatedDate, category)

QuickAnswer (2–3 TL;DR буллета — из первого H2 если не задано отдельно)

[MDX body — prose рендер]
  Внутри MDX: CostTable, CTABox импортируются как компоненты

FAQAccordion (post.data.faqs если есть)

AuthorBio (post.data.author)

CTA: "Find contractors in your city" → /[post.data.service]
```

### SEO и Schema

Title: `{post.data.title} | CVS Contracting`
Schema: `ArticleSchema` + `FAQSchema` (если faqs есть) + `Breadcrumb`

---

## 10. Sample Content

### src/content/services/basement-waterproofing.mdx

Frontmatter:
```yaml
serviceSlug: "basement-waterproofing"
title: "Basement Waterproofing Contractors in Northeast US"
description: "Find trusted basement waterproofing contractors in Maine and New Hampshire. Compare companies, costs, and get free quotes."
updatedDate: 2026-06-01
howItWorks:
  steps:
    - "Inspect foundation walls and floor for cracks, seepage, and hydrostatic pressure"
    - "Choose interior or exterior waterproofing method based on severity"
    - "Install drainage system (French drain or sump pump if needed)"
    - "Apply waterproof coating or membrane to walls"
    - "Final inspection and moisture testing"
  timeline: "1–3 days for interior; 3–5 days for exterior excavation"
whenToHire:
  signs:
    - "Water stains or white mineral deposits (efflorescence) on walls"
    - "Musty smell or visible mold in basement"
    - "Cracks in foundation walls — horizontal cracks are urgent"
    - "Water pooling after heavy rain or snowmelt"
    - "Bowing or buckling basement walls"
  diyVsPro: "Minor surface sealing is DIY-feasible, but persistent seepage, structural cracks, or high water table require a licensed contractor. Maine and NH freeze-thaw cycles accelerate damage if left unaddressed."
faqs:
  - question: "How much does basement waterproofing cost in {cityName}?"
    answer: "Basement waterproofing in {cityName} typically costs $3,000–$10,000 depending on the method. Interior drainage systems average $4,000–$7,000; exterior excavation runs $8,000–$15,000 for larger foundations."
  - question: "How long does basement waterproofing last in {cityName}?"
    answer: "Professional waterproofing in {cityName} lasts 10–25 years. Interior drain tile systems with transferable warranties offer the longest coverage."
  - question: "Do I need a permit for basement waterproofing in {cityName}?"
    answer: "Most interior waterproofing work in {cityName} doesn't require a permit. Exterior excavation that alters grading may need one — your contractor should confirm with the local building department."
  - question: "What's the difference between waterproofing and damp-proofing?"
    answer: "Damp-proofing resists soil moisture only — it's a coating applied at construction. Waterproofing handles hydrostatic water pressure and standing water, which is what most {cityName} homeowners actually need."
  - question: "Can I waterproof a basement from the inside?"
    answer: "Yes — interior waterproofing manages water that enters rather than blocking it at the source. It's less disruptive and 40–60% cheaper than exterior methods. Most contractors in {cityName} recommend interior systems for existing homes."
```

Тело файла (MDX): полный гайд 1800–2200 слов о basement waterproofing в Northeast.
Включает: типы методов, сравнение interior vs exterior, признаки проблем, как выбрать подрядчика.

### src/content/blog/basement-waterproofing-cost-guide.mdx

Frontmatter:
```yaml
title: "Basement Waterproofing Cost in Maine and New Hampshire: 2026 Guide"
description: "Avg basement waterproofing cost in Maine and New Hampshire is $3,000–$10,000. See what affects price and how to get accurate quotes."
author: "CVS Contracting Editorial Team"
pubDate: 2026-06-01
updatedDate: 2026-06-01
service: "basement-waterproofing"
category: "cost-guide"
faqs:
  - question: "What is the average basement waterproofing cost in Maine?"
    answer: "Maine homeowners pay $3,500–$9,500 on average. Interior drainage systems run $3,500–$6,500; exterior excavation averages $8,000–$14,000 depending on linear footage."
  - question: "Is basement waterproofing worth it in New Hampshire?"
    answer: "Yes — NH's freeze-thaw cycles make untreated seepage worse each winter. Average repair costs increase 30–40% when structural damage sets in."
  - question: "Does homeowner's insurance cover basement waterproofing?"
    answer: "Standard HO policies don't cover gradual water intrusion, only sudden events. Waterproofing is typically a maintenance expense."
  - question: "How do I get an accurate quote for basement waterproofing?"
    answer: "Get 3 written quotes minimum. Each contractor should inspect in person — phone quotes are not reliable for waterproofing due to variation in foundation conditions."
```

Тело (MDX):
- QuickAnswer import + usage (3 key takeaways)
- H2 sections: Average Cost Breakdown, What Affects the Price, Interior vs Exterior Cost, How to Save Money, How to Get Quotes
- CostTable с Maine / New Hampshire строками
- CTABox → `/basement-waterproofing`
- 3–5 inline ссылок на city-service страницы (Portland ME, Manchester NH, Concord NH и т.д.)

---

## Порядок создания

1. `src/content/config.ts` — Zod schemas для обеих коллекций
2. `src/content/services/basement-waterproofing.mdx` — sample hub
3. `src/content/blog/basement-waterproofing-cost-guide.mdx` — sample blog
4. `src/lib/intros.ts` + `src/lib/faqs.ts`
5. `src/components/schema/ServiceSchema.astro` + `ArticleSchema.astro`
6. `src/components/common/FAQAccordion.astro`
7. `src/components/city/` — все 5 компонентов
8. `src/components/hub/` — все 4 компонента
9. `src/components/blog/` — все 4 компонента
10. `src/components/layout/Nav.astro` + `Footer.astro`
11. `src/layouts/SiteLayout.astro`
12. `src/pages/[service]/[city].astro`
13. `src/pages/[service]/index.astro`
14. `src/pages/blog/[slug].astro` + `src/pages/blog/index.astro`

---

## Критерий готовности

`npm run build` проходит без ошибок.

В `dist/`:
- `basement-waterproofing/index.html` — service hub
- `basement-waterproofing/portland-me/index.html` — city-service page (если есть данные)
- `blog/basement-waterproofing-cost-guide/index.html` — blog post

На city-service странице `<head>`:
- Title по паттерну `{Service} in {City}, {State} | CVS Contracting`
- Canonical без trailing slash
- JSON-LD: Service + LocalBusiness array + FAQPage + BreadcrumbList
- `<meta name="robots" content="index, follow">`

Визуальная проверка (dev server):
- CompanyCard рендерится с реальными данными
- Sticky sidebar виден на desktop, ниже main на mobile
- FAQ accordion открывается/закрывается без JS (только HTML details)
- Affiliate ссылки имеют `rel="nofollow sponsored"`
- Footer содержит ссылку на `/affiliate-disclosure`
