import type { CityEntry, CompanyEntry } from '../types'

export function getValidCitiesForService(
  cities: CityEntry[],
  companies: CompanyEntry[],
  phase: number,
): CityEntry[] {
  return cities.filter((c) => {
    if (c.phase > phase) return false
    const minReviews = c.population < 10000 ? 1 : 3
    return (
      companies.filter(
        (co) => co.city_slug === c.slug && co.rating >= 3.5 && co.review_count >= minReviews,
      ).length >= 3
    )
  })
}
