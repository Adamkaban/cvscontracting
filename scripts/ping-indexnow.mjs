import { readFileSync, existsSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

const KEY = 'f085818e2a7b4202b1c298c199f9a5e5'
const HOST = 'cvscontracting.com'
const DIST = resolve(__dirname, '../dist')

// Only run on CF Pages main branch (production deploy)
const isCFPages = process.env.CF_PAGES === '1'
const branch = process.env.CF_PAGES_BRANCH ?? ''
if (!isCFPages || branch !== 'main') {
  console.log(`IndexNow: skip (CF_PAGES=${process.env.CF_PAGES ?? 'unset'}, branch=${branch || 'unset'})`)
  process.exit(0)
}

// Parse sitemap index → collect all sitemap files
function extractLocs(xml) {
  return [...xml.matchAll(/<loc>(https?:\/\/[^<]+)<\/loc>/g)].map((m) => m[1])
}

const indexPath = resolve(DIST, 'sitemap-index.xml')
if (!existsSync(indexPath)) {
  console.error('IndexNow: sitemap-index.xml not found in dist/ — run build first')
  process.exit(1)
}

const indexXml = readFileSync(indexPath, 'utf8')
const sitemapFiles = extractLocs(indexXml)
  .map((url) => url.replace('https://cvscontracting.com/', ''))
  .map((path) => resolve(DIST, path))

const urls = []
for (const file of sitemapFiles) {
  if (!existsSync(file)) continue
  const xml = readFileSync(file, 'utf8')
  urls.push(...extractLocs(xml))
}

if (urls.length === 0) {
  console.log('IndexNow: no URLs found')
  process.exit(0)
}

console.log(`IndexNow: submitting ${urls.length} URLs to Bing/IndexNow...`)

const BATCH_SIZE = 500
let success = 0
let failed = 0

for (let i = 0; i < urls.length; i += BATCH_SIZE) {
  const batch = urls.slice(i, i + BATCH_SIZE)
  try {
    const res = await fetch('https://api.indexnow.org/IndexNow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ host: HOST, key: KEY, urlList: batch }),
    })
    if (res.ok || res.status === 202) {
      console.log(`  batch ${Math.floor(i / BATCH_SIZE) + 1}: ${res.status} OK (${batch.length} URLs)`)
      success += batch.length
    } else {
      const body = await res.text()
      console.warn(`  batch ${Math.floor(i / BATCH_SIZE) + 1}: ${res.status} ERROR — ${body.slice(0, 120)}`)
      failed += batch.length
    }
  } catch (err) {
    console.warn(`  batch ${Math.floor(i / BATCH_SIZE) + 1}: network error — ${err.message}`)
    failed += batch.length
  }
}

console.log(`IndexNow: done. submitted=${success} failed=${failed}`)
if (failed > 0) process.exit(1)
