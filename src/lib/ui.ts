export function initials(name: string): string {
  const words = name.replace(/[^A-Za-z0-9 ]/g, '').trim().split(/\s+/)
  if (words.length === 0) return '?'
  if (words.length === 1) return words[0].slice(0, 2).toUpperCase()
  return (words[0][0] + words[1][0]).toUpperCase()
}

const PALETTE = ['#1D4ED8', '#15803D', '#B45309', '#0F766E', '#7C3AED', '#BE185D']

export function monogramColor(name: string): string {
  let h = 0
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0
  return PALETTE[h % PALETTE.length]
}
