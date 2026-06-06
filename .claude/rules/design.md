# Design Rules — CVS Contracting

## Dials
DESIGN_VARIANCE: 6 | MOTION_INTENSITY: 2 | VISUAL_DENSITY: 5

## Stack
Astro 5 + Tailwind v4 (`@tailwindcss/vite`) + Geist (self-hosted) + Phosphor Icons.
No React unless needed for interactive islands. No JS animations — CSS transitions only.

## Theme
Light only. No dark mode. Clean, trustworthy, local-business aesthetic — NOT startup/SaaS.

## Colors
- Base: white bg / gray-900 text
- Accent: `#1D4ED8` (blue-700) — CTAs, links
- Secondary: `#15803D` (green-700) — verified, ratings, positive signals
- Borders: gray-200 | Card bg: gray-50 | Warning: amber-500 | Stars: amber-400

## Typography
- Font: Geist (`@fontsource/geist`), `font-display: swap`, Latin subset, preloaded in `<head>`
- Fallback: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- H1: `text-3xl md:text-4xl font-bold text-gray-900 tracking-tight`
- H2: `text-2xl font-semibold text-gray-900 tracking-tight`
- Body: `text-base text-gray-600 leading-relaxed`
- Company name: `text-lg font-semibold text-gray-900`
- Rating: `font-mono text-amber-500` | Price: `font-semibold text-gray-900` | Phone: `font-mono text-gray-700`

## Layout

### Home
- Hero: asymmetric split — left 55% (headline + subline + city search), right 45% (real project photo). Single column mobile, photo below copy.
- Photo: `aspect-[4/3] rounded-xl overflow-hidden object-cover`, `loading="eager"`, WebP — LCP element. No people, no stock. Use real job photos or high-res stone/concrete texture.
- Service grid: basement-waterproofing as featured tile (`col-span-2 row-span-2`). Desktop: `grid-cols-3`. Mobile: single column. Never 6 equal cards.
- Below grid: top cities section → "How it works" (3 steps) + CTA

### Service Hub Page
- max-w-4xl centered, city grid `grid-cols-2 md:grid-cols-3 lg:grid-cols-4`, cost table full-width striped

### City-Service Page
- Desktop: 2-col — main 70% + sticky sidebar 30%
- Sidebar: `sticky top-6 bg-white border border-gray-200 rounded-xl p-6 shadow-sm`
  - "Get Free Quotes in {City}" — `text-lg font-semibold`
  - Cost range: `text-2xl font-bold text-gray-900`
  - CTA: `w-full bg-blue-700 hover:bg-blue-800 text-white font-semibold rounded-md px-6 py-3`
  - Below CTA: "Free quotes, no obligation" — `text-xs text-gray-500 text-center mt-2`
- FAQ: `<details>/<summary>`, no JS. Phosphor `CaretDown` rotates 180° on open via CSS only (`details[open] summary svg { transform: rotate(180deg) }`). Summary hover: blue-700. Answer: `text-gray-600 pb-4 leading-relaxed`. Divider: `border-t border-gray-200`.

### Company Card
- `border border-gray-200 rounded-lg p-4`
- Hover: `hover:border-gray-300 hover:shadow-sm hover:border-l-4 hover:border-l-blue-700 transition-shadow duration-150`
- Stars: Phosphor `Star`/`StarHalf` 16px, `fill-amber-400 text-amber-400`
- Review count: `text-sm text-gray-500` | Phone: `font-mono text-gray-700 text-sm`
- CTA: `bg-blue-700 text-white rounded-md px-4 py-2 text-sm`
- Mobile: stacked, CTA full-width

### CTA Button (primary)
`bg-blue-700 hover:bg-blue-800 text-white font-semibold rounded-md px-6 py-3`
Text: "Get Free Quotes" — always this on affiliate CTAs. Full-width on mobile.

### Blog Post
- max-w-2xl centered. Pull quotes: `bg-gray-50 border-l-4 border-blue-700 p-4`

## Icons
Phosphor Icons — **inline SVG only** (no npm, no React). Copy paths from phosphoricons.com.
- Weight: `regular` UI, `bold` CTAs. Size: 16px inline, 20px standalone, 24px feature.
- Do NOT install `@phosphor-icons/react`. No mixing families.

## Images
- Hero: `loading="eager"`, WebP, explicit w+h
- All others: `loading="lazy" decoding="async"`, explicit dimensions, locked aspect ratio (prevents CLS)
- Placeholder: `bg-gray-100 animate-pulse`
- Use Astro `<Image>` (auto WebP + srcset). Real project photos only.

## Breadcrumbs (all city/hub pages, above H1)
`Home > Service > City, State` — Phosphor `CaretRight` 12px `text-gray-400` separator.
Active page: `text-gray-900 font-medium`. Links: `text-blue-700 hover:underline text-sm`. Container: `text-sm mb-4`.

## Trust Signals (city pages, required)
Review count visible, phone visible without clicking, address visible, "Last updated: {date}", affiliate disclosure in footer.

## Mobile
All grids: single column. Cards: stacked. CTA: full-width. Sidebar: below main content (not hidden).

## Forbidden
- em-dash (—) — use comma or colon
- Dark backgrounds on content pages
- Hero with people
- Gradients on CTA buttons
- Carousels, sliders, chat widgets (Phase 1)
- Google Fonts or Inter — Geist only
- Animations except hover transitions + FAQ caret (CSS only)
- "Featured" badge without paid placement
- Emoji in UI
