import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'
import mdx from '@astrojs/mdx'
import tailwindcss from '@tailwindcss/vite'
import config from './site.config.ts'

export default defineConfig({
  site: process.env.SITE_URL ?? config.seo.siteUrl,
  output: 'static',
  trailingSlash: 'never',
  integrations: [
    mdx(),
    sitemap({
      filter: (page) => !page.includes('/affiliate-disclosure') && !page.includes('/claim'),
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
})
