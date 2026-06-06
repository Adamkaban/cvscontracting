// Hub FAQ answers contain a {cityName} placeholder. On city pages the placeholder
// is replaced with the real city name; on the hub page it is replaced with a
// regional term. FAQ source data lives in the service-hub content collection.

export interface FAQ {
  question: string
  answer: string
}

/**
 * City-service FAQs. Injects city.name into the hub FAQ template.
 * Note: signature deviates from the prompt — service.json has no faqs field,
 * so the hub collection's faqs[] are passed in (`hubFaqs`).
 */
export function getCityServiceFAQs(cityName: string, hubFaqs: FAQ[]): FAQ[] {
  return hubFaqs.map((f) => ({
    question: f.question.replace(/\{cityName\}/g, cityName),
    answer: f.answer.replace(/\{cityName\}/g, cityName),
  }))
}

/** Hub FAQs: replace {cityName} with a regional phrase (no specific city). */
export function getHubFAQs(hubFaqs: FAQ[], region = 'Maine and New Hampshire'): FAQ[] {
  return hubFaqs.map((f) => ({
    question: f.question.replace(/\{cityName\}/g, region),
    answer: f.answer.replace(/\{cityName\}/g, region),
  }))
}
