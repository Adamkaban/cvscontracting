export interface CityEntry {
  name: string
  state: string
  state_abbr: string
  slug: string
  county: string
  population: number
  lat: number
  lng: number
  zip: string
  nearby_cities: string[]
  phase: 1 | 2 | 3
}

export interface ServiceEntry {
  name: string
  slug: string
  description: string
  avg_cost_min: number
  avg_cost_max: number
  lead_value_min: number
  lead_value_max: number
  affiliate_url: string
  priority: 1 | 2
  keywords: string[]
  keywords_lsi?: string[]
  description_variants?: string[]
  pageTitle?: string
  metaDescription?: string
}

export interface CompanyEntry {
  name: string
  slug: string
  city_slug: string
  service_slug: string
  address: string
  zip: string
  phone: string | null
  rating: number
  review_count: number
  google_maps_url: string | null
  website: string | null
  logo_url: string | null
  claimed: boolean
  featured: boolean
  years_in_business?: number
  insured?: boolean
  bbb_rating?: string
  service_area?: string
  blurb?: string
}
