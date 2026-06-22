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

// Stable index from a string, so each city deterministically picks a template
// variant. Spreads cities across variants to keep intros >30% unique.
function pick<T>(seed: string, options: T[]): T {
  let h = 0
  for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0
  return options[h % options.length]
}

export function generateCityIntro(city: CityEntry, service: ServiceEntry): string {
  const tier = getPopulationTier(city.population)
  const climate = getClimateContext(city.state_abbr)
  const svc = service.name.toLowerCase()
  const pop = city.population.toLocaleString()

  // Opening sentence — variant by city slug.
  const opener = pick(city.slug + service.slug, [
    `${city.name} is a ${tier} of about ${pop} residents in ${city.county}, ${city.state}, where ${climate} make ${svc} a recurring concern for homeowners.`,
    `Set in ${city.county}, ${city.name} is a ${tier} home to roughly ${pop} people, and ${climate} keep demand for ${svc} steady across ${city.state}.`,
    `With a population near ${pop}, the ${tier} of ${city.name} sits in ${city.county} in ${city.state}, a region shaped by ${climate} that take a toll on local properties.`,
  ])

  // Second sentence — service-relevant, variant by city + service (unique per city, not per state).
  const detail = pick(city.slug + '-d-' + service.slug, [
    `Local conditions here mean ${svc} work often calls for contractors who understand the soil, drainage, and building stock specific to ${city.county}.`,
    `Homeowners in ${city.name} tend to hire ${svc} specialists familiar with how ${city.state}'s seasons affect foundations and grading.`,
    `Choosing a ${svc} contractor who works regularly in the ${city.name} area helps because local crews price and plan around ${city.county}'s ground conditions.`,
  ])

  // Closing — orients the reader to the page.
  const closer = `Below are vetted ${svc} companies serving ${city.name}, typical local cost ranges, and what to check before you hire.`

  return `${opener} ${detail} ${closer}`
}
