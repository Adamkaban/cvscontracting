import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'
import tailwindcss from '@tailwindcss/vite'
import config from './site.config.ts'

import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  site: process.env.SITE_URL ?? config.seo.siteUrl,
  output: 'static',
  trailingSlash: 'never',

  integrations: [
    sitemap({
      filter: (page) => !page.includes('/affiliate-disclosure') && !page.includes('/claim'),
    }),
  ],

  vite: {
    plugins: [tailwindcss()],
  },

  adapter: cloudflare()
})