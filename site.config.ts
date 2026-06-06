// site.config.ts
const config = {

  // ─── BRAND ───────────────────────────────────────────
  brand: {
    name: "CVS Contracting",
    slug: "cvs-contracting",
    logo: "/images/logo.svg",
  },

  // ─── SEO ─────────────────────────────────────────────
  // SITE_URL from .env overrides siteUrl at build time.
  // In components: import.meta.env.SITE_URL ?? config.seo.siteUrl
  seo: {
    siteUrl: "https://cvscontracting.com",  // no trailing slash
    titleTemplate: "%s | CVS Contracting",
    defaultDescription:
      "Find trusted contractors for foundations, basement waterproofing, excavation, and snow removal across Northeast USA.",
    ogImage: "/images/og-default.jpg",
  },

  // ─── THEME ───────────────────────────────────────────
  // Values come from design.md — do not change arbitrarily.
  theme: {
    primaryColor:   "#1D4ED8",  // blue-700  — CTAs, links
    accentColor:    "#15803D",  // green-700 — verified, ratings
    warningColor:   "#F59E0B",  // amber-500
    starColor:      "#FBBF24",  // amber-400
    borderColor:    "#E5E7EB",  // gray-200
    cardBg:         "#F9FAFB",  // gray-50
    fontBody:       "Geist",    // self-hosted, @fontsource/geist
    fontHeading:    "Geist",    // same font, weight 700
  },

  // ─── AFFILIATE (shared settings) ─────────────────────
  // Concrete URLs live in src/data/services.json → affiliate_url field.
  // Only immutable constants here.
  affiliate: {
    linkRel:           "nofollow sponsored",
    ctaText:           "Get Free Quotes",
    disclosurePage:    "/affiliate-disclosure",
    footerDisclosure:  "This site may receive compensation when you click affiliate links.",
  },

};

export default config;
export type SiteConfig = typeof config;
