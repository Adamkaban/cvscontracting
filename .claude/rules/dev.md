# Dev Setup — CVS Contracting

## Stack

| Package | Version | Note |
|---------|---------|------|
| astro | 5.x | |
| @astrojs/sitemap | latest | |
| @tailwindcss/vite | 4.x | use directly — NOT `@astrojs/tailwind` |
| typescript | 5.x | |

## Init

```bash
npm create astro@latest . -- --template minimal --typescript strict --no-git --no-install
npm install
npm install @astrojs/sitemap @tailwindcss/vite tailwindcss
```

## Commands

```bash
npm run dev          # localhost:4321
npm run build        # → dist/
npm run preview      # preview dist/
npx astro check      # TypeScript check — run before deploy
```

## Tailwind Setup

Config in `src/styles/global.css` — NOT `tailwind.config.js`. No PostCSS.
Import in layout: `import '../styles/global.css'`

## Cloudflare Pages Deploy

Flow: `git push origin main` → CF Pages detects push → CF builds + deploys automatically.
No manual deploy step. CF Dashboard → Pages → project → Build settings: command `npm run build`, output `dist`, Node 18+.

Before pushing: run `npm run build` locally to catch errors before CF sees them.

After deploy verify: `/` → 200, `/sitemap.xml` → 200, www → 301 non-www, http → 301 https.

## Environment Variables

```bash
PUBLIC_PHASE=1   # 1, 2, or 3
```

In Astro: `const phase = parseInt(import.meta.env.PUBLIC_PHASE ?? '1')`

## Common Issues

| Problem | Fix |
|---------|-----|
| Build fails — missing companies JSON | Guard: `.catch(() => ({ default: [] }))` on import |
| Sitemap missing city pages | Check `getStaticPaths()` returns all paths |
| Tailwind not working | `@import "tailwindcss"` in global.css AND imported in layout |
| TypeScript errors on JSON imports | `"resolveJsonModule": true` in tsconfig.json |
