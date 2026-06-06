/**
 * Favicon generation script.
 * Run: node scripts/generate-favicons.mjs
 * Requires: sharp (npm install --save-dev sharp)
 *
 * Outputs:
 *   public/favicon-16x16.png
 *   public/favicon-32x32.png
 *   public/apple-touch-icon.png   (180x180, no rounded corners — iOS applies them)
 *   public/android-chrome-192x192.png
 *   public/android-chrome-512x512.png
 *   public/favicon.ico            (contains 16x16 + 32x32 PNG images)
 */

import sharp from 'sharp'
import { readFileSync, writeFileSync } from 'fs'
import { fileURLToPath } from 'url'
import path from 'path'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const root = path.join(__dirname, '..')
const svgPath = path.join(root, 'public', 'favicon.svg')
const svgBuffer = readFileSync(svgPath)

const sizes = [
  { name: 'favicon-16x16.png', size: 16 },
  { name: 'favicon-32x32.png', size: 32 },
  { name: 'apple-touch-icon.png', size: 180 },
  { name: 'android-chrome-192x192.png', size: 192 },
  { name: 'android-chrome-512x512.png', size: 512 },
]

console.log('Generating favicon PNGs from favicon.svg...')

const pngBuffers = {}

for (const { name, size } of sizes) {
  const dest = path.join(root, 'public', name)
  const buf = await sharp(svgBuffer)
    .resize(size, size)
    .png({ compressionLevel: 9 })
    .toBuffer()
  writeFileSync(dest, buf)
  pngBuffers[size] = buf
  console.log(`  ✓ public/${name} (${size}x${size})`)
}

// Build favicon.ico containing 16x16 and 32x32 PNG images.
// ICO format: ICONDIR header + ICONDIRENTRY per image + raw PNG data.
function buildIco(images) {
  const count = images.length
  // Header: 6 bytes
  const header = Buffer.alloc(6)
  header.writeUInt16LE(0, 0)     // reserved
  header.writeUInt16LE(1, 2)     // type: 1 = ICO
  header.writeUInt16LE(count, 4) // number of images

  // Each ICONDIRENTRY is 16 bytes
  const entrySize = 16
  const dataOffset = 6 + entrySize * count

  const entries = []
  const dataChunks = []
  let offset = dataOffset

  for (const { size, png } of images) {
    const entry = Buffer.alloc(entrySize)
    const dim = size >= 256 ? 0 : size  // 0 = 256 per spec
    entry.writeUInt8(dim, 0)             // width
    entry.writeUInt8(dim, 1)             // height
    entry.writeUInt8(0, 2)              // color count (0 = no palette)
    entry.writeUInt8(0, 3)              // reserved
    entry.writeUInt16LE(1, 4)           // color planes
    entry.writeUInt16LE(32, 6)          // bits per pixel
    entry.writeUInt32LE(png.length, 8)  // size of image data
    entry.writeUInt32LE(offset, 12)     // offset to image data
    entries.push(entry)
    dataChunks.push(png)
    offset += png.length
  }

  return Buffer.concat([header, ...entries, ...dataChunks])
}

const icoImages = [
  { size: 16, png: pngBuffers[16] },
  { size: 32, png: pngBuffers[32] },
]
const icoBuf = buildIco(icoImages)
const icoDest = path.join(root, 'public', 'favicon.ico')
writeFileSync(icoDest, icoBuf)
console.log(`  ✓ public/favicon.ico (16x16 + 32x32)`)

// Safari pinned tab SVG: monochrome version (no background, just the C path in black)
const safariSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <path
    d="M 355 355 A 140 140 0 1 0 355 157"
    fill="none"
    stroke="black"
    stroke-width="72"
    stroke-linecap="round"
  />
</svg>`
writeFileSync(path.join(root, 'public', 'safari-pinned-tab.svg'), safariSvg)
console.log(`  ✓ public/safari-pinned-tab.svg`)

console.log('\nDone. All favicon assets generated.')
