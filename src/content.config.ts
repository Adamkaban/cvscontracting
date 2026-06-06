import { defineCollection, z } from 'astro:content'
import { glob } from 'astro/loaders'

// Service hub content — one MDX per service. Body = 1500–2500 word guide.
const services = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/services' }),
  schema: z.object({
    serviceSlug: z.string(), // must match a slug in services.json
    title: z.string(),
    description: z.string().max(155),
    updatedDate: z.coerce.date(),
    howItWorks: z.object({
      steps: z.array(z.string()),
      timeline: z.string(),
    }),
    whenToHire: z.object({
      signs: z.array(z.string()),
      diyVsPro: z.string(),
    }),
    // {cityName} placeholder in answers — injected per city on city pages,
    // replaced with a regional term on the hub page.
    faqs: z.array(
      z.object({
        question: z.string(),
        answer: z.string(),
      }),
    ),
  }),
})

const blog = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(155),
    author: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date(),
    service: z.string(), // service slug
    category: z.enum(['cost-guide', 'how-to', 'comparison']),
    ogImage: z.string().optional(),
    faqs: z
      .array(
        z.object({
          question: z.string(),
          answer: z.string(),
        }),
      )
      .optional(),
  }),
})

export const collections = { services, blog }
