# CVS Contracting — Astro 5 Infrastructure Base

Стек: Astro 5, Tailwind v4 (@tailwindcss/vite), TypeScript strict.
Версии и init-команды — в .claude/rules/dev.md.

Инфраструктурная база. **НЕ сайт и НЕ шаблоны страниц.**
Три модуля: конфиг, SEO-инфраструктура, базовый layout.
Поверх этой базы будут добавляться шаблоны страниц отдельно.

---

## Что НЕ входит (отличия от мультишаблонного паттерна)

- **Нет i18n** — сайт монолингвальный (en), никаких `[lang]/`, LanguagePicker, Hreflang
- **Нет template configs** — один сайт, один тип конфига
- **Нет Google Fonts** — только Geist self-hosted via `@fontsource/geist`
- **Affiliate URLs** не в `site.config.ts` — они уже в `src/data/services.json` (поле `affiliate_url`)
- `robots.txt` — **статический файл** `public/robots.txt`, не динамический endpoint

---

## Файловая структура (только этот промт)

```
site.config.ts                         ← единый конфиг сайта
src/
  styles/
    global.css                         ← Tailwind v4 + Geist + CSS vars
  components/
    seo/
      SEOHead.astro                    ← title, meta, canonical, og, noindex
    schema/
      LocalBusinessSchema.astro        ← JSON-LD LocalBusiness (массив компаний)
      FAQSchema.astro                  ← JSON-LD FAQPage
      OrganizationSchema.astro         ← JSON-LD Organization + WebSite (только home)
    common/
      Breadcrumb.astro                 ← визуальный UI + JSON-LD BreadcrumbList
  layouts/
    BaseLayout.astro                   ← <html lang="en">, head, slot
  pages/
    affiliate-disclosure.astro         ← FTC required, noindex
public/
  robots.txt                           ← статический файл
```

---

## 1. site.config.ts

Файл в корне проекта. Содержит ТОЛЬКО то, чего нет в data-файлах.
Affiliate URLs живут в `src/data/services.json` — здесь их нет.

```ts
// site.config.ts
const config = {

  // ─── БРЕНД ───────────────────────────────────────────
  brand: {
    name: "CVS Contracting",
    slug: "cvs-contracting",
    logo: "/images/logo.svg",
  },

  // ─── SEO ─────────────────────────────────────────────
  // SITE_URL из .env перекрывает siteUrl при сборке.
  // В компонентах: import.meta.env.SITE_URL ?? config.seo.siteUrl
  seo: {
    siteUrl: "https://cvscontracting.com",  // без / в конце
    titleTemplate: "%s | CVS Contracting",
    defaultDescription:
      "Find trusted contractors for foundations, basement waterproofing, excavation, and snow removal across Northeast USA.",
    ogImage: "/images/og-default.jpg",
  },

  // ─── ТЕМА ────────────────────────────────────────────
  // Значения берутся из design.md — не менять произвольно.
  theme: {
    primaryColor:   "#1D4ED8",  // blue-700  — CTAs, links
    accentColor:    "#15803D",  // green-700 — verified, ratings
    warningColor:   "#F59E0B",  // amber-500
    starColor:      "#FBBF24",  // amber-400
    borderColor:    "#E5E7EB",  // gray-200
    cardBg:         "#F9FAFB",  // gray-50
    fontBody:       "Geist",    // self-hosted, @fontsource/geist
    fontHeading:    "Geist",    // same font, weight 700
  },

  // ─── AFFILIATE (общие настройки) ─────────────────────
  // Конкретные URLs живут в src/data/services.json → поле affiliate_url.
  // Здесь только неизменяемые константы.
  affiliate: {
    linkRel:           "nofollow sponsored",
    ctaText:           "Get Free Quotes",
    disclosurePage:    "/affiliate-disclosure",
    footerDisclosure:  "This site may receive compensation when you click affiliate links.",
  },

};

export default config;
export type SiteConfig = typeof config;
```

---

## 2. astro.config.mjs

Полная спека в `.claude/rules/dev.md`. Здесь только правило интеграции с конфигом:

```js
import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'
import tailwindcss from '@tailwindcss/vite'
import config from './site.config.ts'

export default defineConfig({
  site: process.env.SITE_URL ?? config.seo.siteUrl,
  output: 'static',
  trailingSlash: 'never',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()]
  }
})
```

`process.env.SITE_URL` — переменная из `.env` для staging-окружений.

---

## 3. src/styles/global.css

Tailwind v4 через `@import`, Geist через `@fontsource/geist`, CSS-переменные из `site.config.ts`.
Значения хардкодятся из конфига — CSS не читает TS-файл напрямую.

```css
/* src/styles/global.css */

/* Geist self-hosted — Latin subset, font-display: swap встроен в пакет */
@import "@fontsource/geist/latin-400.css";
@import "@fontsource/geist/latin-600.css";
@import "@fontsource/geist/latin-700.css";

/* Tailwind v4 */
@import "tailwindcss";

/* ─── Дизайн-токены ────────────────────────────────────── */
/* Значения из site.config.ts → theme + design.md */
@theme {
  --color-brand:        #1D4ED8;   /* blue-700 */
  --color-brand-dark:   #1E40AF;   /* blue-800 */
  --color-success:      #15803D;   /* green-700 */
  --color-warning:      #F59E0B;   /* amber-500 */
  --color-stars:        #FBBF24;   /* amber-400 */
}

/* ─── CSS-переменные (для JS-компонентов и нестандартных случаев) ── */
:root {
  --color-primary:    #1D4ED8;
  --color-accent:     #15803D;
  --font-body:        "Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-heading:     "Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono:        ui-monospace, "SFMono-Regular", Menlo, monospace;

  /* Layout */
  --container-max:    72rem;
  --content-max:      65ch;

  /* Spacing */
  --spacing-xs:  0.25rem;
  --spacing-sm:  0.5rem;
  --spacing-md:  1rem;
  --spacing-lg:  1.5rem;
  --spacing-xl:  2rem;
  --spacing-2xl: 3rem;

  /* Border radius */
  --radius-sm:   0.25rem;
  --radius-md:   0.5rem;
  --radius-lg:   0.75rem;
  --radius-xl:   1rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm:  0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md:  0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg:  0 10px 15px -3px rgb(0 0 0 / 0.1);

  /* Transitions — CSS only, no JS animations */
  --transition-fast:   150ms ease;
  --transition-normal: 250ms ease;
}

/* ─── Утилиты ──────────────────────────────────────────── */
.container {
  width: 100%;
  max-width: var(--container-max);
  margin-inline: auto;
  padding-inline: 1rem;
}

@media (min-width: 640px) {
  .container { padding-inline: 1.5rem; }
}

@media (min-width: 1024px) {
  .container { padding-inline: 2rem; }
}

.section {
  padding-block: var(--spacing-2xl);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## 4. src/components/seo/SEOHead.astro

### Пропсы

```ts
interface Props {
  title: string          // без бренда — шаблон применяется автоматически
  description?: string   // fallback: config.seo.defaultDescription
  canonicalUrl?: string  // fallback: siteUrl + Astro.url.pathname (без trailing slash)
  ogImage?: string       // fallback: config.seo.ogImage
  noindex?: boolean      // default: false
}
```

### Что генерирует

- `<title>` через `config.seo.titleTemplate` (подставить `%s`)
- `<meta name="description">` — max 155 символов
- `<link rel="canonical">` — HTTPS, без trailing slash, без query string
- `<meta name="robots">`:
  - По умолчанию: `index, follow`
  - Если `noindex=true`: `noindex, nofollow`
- Open Graph теги:
  - `og:title` — финальный title (с брендом)
  - `og:description`
  - `og:image` — абсолютный URL
  - `og:url` — canonical URL
  - `og:type: "website"`
  - `og:site_name: config.brand.name`
- Twitter Card:
  - `twitter:card: "summary_large_image"`
  - `twitter:title`, `twitter:description`, `twitter:image`
- Preload Geist font (woff2, Latin 400):
  ```astro
  import geistFontUrl from '@fontsource/geist/files/geist-latin-400-normal.woff2?url';
  ```
  ```html
  <link rel="preload" href={geistFontUrl} as="font" type="font/woff2" crossorigin>
  ```

### Правило canonical

```ts
const siteUrl = import.meta.env.SITE_URL ?? config.seo.siteUrl;
const rawPath  = canonicalUrl ?? Astro.url.pathname;
const cleanPath = rawPath.replace(/\/$/, '') || '/';    // убрать trailing slash
const canonical = siteUrl + cleanPath;
```

---

## 5. Schema-компоненты

Все — JSON-LD. Никакого microdata. Рендерят `<script type="application/ld+json">`.

### src/components/schema/LocalBusinessSchema.astro

Пропсы:
```ts
interface Props {
  companies: Array<{
    name: string
    address: string
    zip: string
    phone: string
    rating: number
    review_count: number
  }>
  cityName: string       // "Portland"
  stateAbbr: string      // "ME"
}
```

Генерирует массив объектов `@type: "LocalBusiness"` (один `<script>` с `@graph`):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "LocalBusiness",
      "name": "...",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "...",
        "addressLocality": "Portland",
        "addressRegion": "ME",
        "postalCode": "04101"
      },
      "telephone": "...",
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": 4.7,
        "reviewCount": 48
      }
    }
  ]
}
```

### src/components/schema/FAQSchema.astro

Пропсы:
```ts
interface Props {
  faqs: Array<{ question: string; answer: string }>
}
```

Генерирует `@type: "FAQPage"` с массивом `mainEntity`.

### src/components/schema/OrganizationSchema.astro

Без пропсов — читает `site.config.ts`.
Генерирует `Organization` + `WebSite`.

Примечание по `SearchAction` в WebSite: добавить ТОЛЬКО когда поиск реально работает на сайте.
В Phase 1 — только `Organization` + `WebSite` без `potentialAction`.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "name": "CVS Contracting",
      "url": "https://cvscontracting.com",
      "logo": "https://cvscontracting.com/images/logo.svg",
      "description": "Find trusted contractors for foundations, basement waterproofing, excavation, and snow removal across Northeast USA"
    },
    {
      "@type": "WebSite",
      "url": "https://cvscontracting.com",
      "name": "CVS Contracting"
    }
  ]
}
```

---

## 6. src/components/common/Breadcrumb.astro

Рендерит **одновременно**: визуальный UI + JSON-LD `BreadcrumbList` в одном компоненте.

### Пропсы

```ts
interface Props {
  items: Array<{
    label: string   // "Basement Waterproofing"
    href?: string   // "/basement-waterproofing" — если нет, это текущая страница
  }>
}
```

Последний элемент = текущая страница (без `href`, не кликабельный).

### Визуальный UI (из design.md)

```html
<nav aria-label="Breadcrumb" class="text-sm mb-4">
  <!-- Home > Basement Waterproofing > Portland, ME -->
  <!-- Разделитель: Phosphor CaretRight icon, 12px, text-gray-400 -->
  <!-- Ссылки: text-blue-700 hover:underline -->
  <!-- Текущая страница: text-gray-900 font-medium (не ссылка) -->
</nav>
```

### JSON-LD BreadcrumbList

Встроен в тот же компонент как `<script type="application/ld+json">`.
Нумерация `position` начинается с 1.
`item` для последнего элемента = полный canonical URL текущей страницы.

---

## 7. src/layouts/BaseLayout.astro

### Пропсы

```ts
interface Props {
  title: string
  description?: string
  ogImage?: string
  noindex?: boolean
  // Данные для schema-компонентов передаются через именованные слоты
}
```

### Структура

```astro
---
import SEOHead from '../components/seo/SEOHead.astro'
import config from '../../site.config.ts'
import '../styles/global.css'
const { title, description, ogImage, noindex } = Astro.props
---
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <SEOHead
      title={title}
      description={description}
      ogImage={ogImage}
      noindex={noindex}
    />
    <slot name="schema" />   {/* ← schema JSON-LD инжектится здесь */}
  </head>
  <body class="bg-white text-gray-900 font-sans">
    <slot />
  </body>
</html>
```

Именованный слот `schema` — страницы кладут туда свои schema-компоненты.

---

## 8. public/robots.txt

**Статический файл** (не Astro endpoint). Создать вручную до первого деплоя.

```
User-agent: *
Disallow: /claim/
Sitemap: https://cvscontracting.com/sitemap-index.xml
```

Примечание: `@astrojs/sitemap` генерирует `sitemap-index.xml`, не `sitemap.xml`.
После подтверждения имени файла в `dist/` — сверить с тем, что здесь.

---

## 9. src/pages/affiliate-disclosure.astro

Требование FTC — dedicated page. `noindex: true` (не для SEO-трафика, только для compliance).

Минимальное содержание:
- H1: "Affiliate Disclosure"
- Объяснение: сайт получает комиссию от Angi / HomeAdvisor / Thumbtack
- Когда заработано (клик + покупка/лид)
- Это не влияет на позицию компаний в листингах
- Контактная информация для вопросов

Использует `BaseLayout` с `noindex={true}`.

---

## 10. Smoke-test страница — src/pages/index.astro

Минимальная страница только для проверки что build проходит.
Без дизайна.

Проверяет:
- `BaseLayout` рендерится
- `config` читается корректно
- `SEOHead` генерирует canonical без ошибок
- `Breadcrumb` рендерится

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro'
import OrganizationSchema from '../components/schema/OrganizationSchema.astro'
import Breadcrumb from '../components/common/Breadcrumb.astro'
import config from '../../site.config.ts'
---
<BaseLayout title="Contractor Services in Maine & Northeast US">
  <OrganizationSchema slot="schema" />
  <main class="container section">
    <Breadcrumb items={[{ label: "Home" }]} />
    <h1>{config.brand.name}</h1>
    <p>Affiliate CTA: {config.affiliate.ctaText}</p>
    <p>Phase 1: ME + NH</p>
  </main>
</BaseLayout>
```

---

## Порядок создания

1. `site.config.ts`
2. `astro.config.mjs` (обновить — добавить import config)
3. `src/styles/global.css`
4. `src/components/seo/SEOHead.astro`
5. `src/components/schema/OrganizationSchema.astro`
6. `src/components/schema/LocalBusinessSchema.astro`
7. `src/components/schema/FAQSchema.astro`
8. `src/components/common/Breadcrumb.astro`
9. `src/layouts/BaseLayout.astro`
10. `public/robots.txt`
11. `src/pages/affiliate-disclosure.astro`
12. `src/pages/index.astro`

---

## Критерий готовности

`npm run build` проходит без ошибок.

В `dist/`:
- `index.html` — содержит `<title>`, `<meta name="description">`, `<link rel="canonical">`, og-теги
- `affiliate-disclosure/index.html` — содержит `<meta name="robots" content="noindex"`>
- `sitemap-index.xml` — сгенерирован `@astrojs/sitemap`
- `robots.txt` — присутствует, содержит `Disallow: /claim/`

В `<head>` главной страницы:
- `<link rel="canonical" href="https://cvscontracting.com">` (без trailing slash)
- `<meta property="og:title">`, `og:description`, `og:image`, `og:url`
- `<meta name="twitter:card" content="summary_large_image">`
- `<link rel="preload" ... type="font/woff2">` для Geist
- JSON-LD `<script type="application/ld+json">` с Organization + WebSite
- `<meta name="robots" content="index, follow">`

---

## Что добавляется ПОЗЖЕ (не часть этого промта)

- Шаблоны страниц: city-service, service hub, blog post
- Компоненты: Hero, CompanyCard, CostTable, CTASidebar, Footer, Nav
- Данные: cities.json, services.json, companies/*.json
- IndexNow: UUID-ключ + ping после первого деплоя
- Phase env var (`PUBLIC_PHASE`) подключается в `getStaticPaths()` шаблонов
