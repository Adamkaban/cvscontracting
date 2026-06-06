#!/usr/bin/env python3
"""
Normalize companies_filtered.csv → src/data/companies/*.json
Also generates src/data/cities.json and src/data/services.json
"""
import csv
import json
import os
import re
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC_DATA = ROOT / "src" / "data"
SRC_DATA.mkdir(parents=True, exist_ok=True)
(SRC_DATA / "companies").mkdir(exist_ok=True)

CSV_PATH = ROOT / "scripts" / "raw" / "companies_filtered.csv"

# ── City static data ──────────────────────────────────────────────────────────

CITY_DATA = {
    # (name, state_abbr): (county, population, lat, lng, zip, phase)
    ("Auburn", "ME"):       ("Androscoggin County", 24061, 44.0979, -70.2312, "04210", 1),
    ("Augusta", "ME"):      ("Kennebec County",     18899, 44.3106, -69.7795, "04330", 1),
    ("Bangor", "ME"):       ("Penobscot County",    31753, 44.8012, -68.7778, "04401", 1),
    ("Bar Harbor", "ME"):   ("Hancock County",       5518, 44.3876, -68.2042, "04609", 1),
    ("Biddeford", "ME"):    ("York County",         22582, 43.4926, -70.4534, "04005", 1),
    ("Brewer", "ME"):       ("Penobscot County",     9482, 44.7954, -68.7653, "04412", 1),
    ("Brunswick", "ME"):    ("Cumberland County",   20278, 43.9148, -69.9653, "04011", 1),
    ("Ellsworth", "ME"):    ("Hancock County",       9021, 44.5434, -68.4197, "04605", 1),
    ("Lewiston", "ME"):     ("Androscoggin County", 37121, 44.1003, -70.2148, "04240", 1),
    ("Portland", "ME"):     ("Cumberland County",   68408, 43.6615, -70.2553, "04101", 1),
    ("Presque Isle", "ME"): ("Aroostook County",     9268, 46.6812, -68.0152, "04769", 1),
    ("Rockland", "ME"):     ("Knox County",          7297, 44.1039, -69.1089, "04841", 1),
    ("Saco", "ME"):         ("York County",         19971, 43.5009, -70.4428, "04072", 1),
    ("Sanford", "ME"):      ("York County",         21270, 43.4393, -70.7739, "04073", 1),
    ("Scarborough", "ME"):  ("Cumberland County",   22363, 43.5784, -70.3242, "04074", 1),
    ("South Portland", "ME"): ("Cumberland County", 26352, 43.6415, -70.2759, "04106", 1),
    ("Waterville", "ME"):   ("Kennebec County",     15722, 44.5523, -69.6317, "04901", 1),
    ("Westbrook", "ME"):    ("Cumberland County",   19710, 43.6773, -70.3745, "04092", 1),
    ("Windham", "ME"):      ("Cumberland County",   19142, 43.8026, -70.4342, "04062", 1),
    ("Berlin", "NH"):       ("Coös County",          9695, 44.4684, -71.1853, "03570", 1),
    ("Concord", "NH"):      ("Merrimack County",    43976, 43.2081, -71.5376, "03301", 1),
    ("Derry", "NH"):        ("Rockingham County",   33109, 42.8812, -71.3223, "03038", 1),
    ("Dover", "NH"):        ("Strafford County",    31922, 43.1979, -70.8737, "03820", 1),
    ("Durham", "NH"):       ("Strafford County",    15490, 43.1340, -70.9264, "03824", 1),
    ("Exeter", "NH"):       ("Rockingham County",   15420, 42.9812, -70.9478, "03833", 1),
    ("Hanover", "NH"):      ("Grafton County",      11870, 43.7023, -72.2895, "03755", 1),
    ("Hooksett", "NH"):     ("Merrimack County",    14704, 43.0979, -71.4648, "03106", 1),
    ("Hudson", "NH"):       ("Hillsborough County", 25716, 42.7640, -71.4065, "03051", 1),
    ("Keene", "NH"):        ("Cheshire County",     23409, 42.9334, -72.2779, "03431", 1),
    ("Laconia", "NH"):      ("Belknap County",      16993, 43.5279, -71.4703, "03246", 1),
    ("Lebanon", "NH"):      ("Grafton County",      13151, 43.6423, -72.2518, "03766", 1),
    ("Londonderry", "NH"):  ("Rockingham County",   25837, 42.8651, -71.3737, "03053", 1),
    ("Manchester", "NH"):   ("Hillsborough County", 115644, 42.9956, -71.4548, "03101", 1),
    ("Merrimack", "NH"):    ("Hillsborough County", 27214, 42.8654, -71.5118, "03054", 1),
    ("Nashua", "NH"):       ("Hillsborough County", 91322, 42.7654, -71.4676, "03060", 1),
    ("Pelham", "NH"):       ("Hillsborough County", 14341, 42.7354, -71.3237, "03076", 1),
    ("Portsmouth", "NH"):   ("Rockingham County",   22187, 43.0718, -70.7626, "03801", 1),
    ("Rochester", "NH"):    ("Strafford County",    32403, 43.3048, -70.9748, "03867", 1),
    ("Salem", "NH"):        ("Rockingham County",   30768, 42.7876, -71.2012, "03079", 1),
    ("Windham", "NH"):      ("Rockingham County",   14904, 42.8065, -71.3007, "03087", 1),
}

STATE_NAMES = {"ME": "Maine", "NH": "New Hampshire"}

# ── Helpers ───────────────────────────────────────────────────────────────────

def to_slug(text: str) -> str:
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9-]', '-', text.lower().strip())).strip('-')

def city_slug(name: str, state_abbr: str) -> str:
    return to_slug(name) + '-' + state_abbr.lower()

def haversine_km(lat1, lng1, lat2, lng2) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def normalize_phone(raw: str) -> str | None:
    if not raw or raw.strip() in ('Not provided', 'Not listed', 'N/A', '(N/A)', '.', ''):
        return None
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('1') and len(digits) == 11:
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return raw.strip() if raw.strip() else None

def extract_zip(address: str) -> str | None:
    m = re.search(r'\b(\d{5})\b', address)
    return m.group(1) if m else None

def service_slug(name: str) -> str:
    return name.strip().lower().replace(' ', '-')

# ── Build cities.json ─────────────────────────────────────────────────────────

def build_cities():
    all_cities = []
    city_list = [(name, abbr, *data) for (name, abbr), data in CITY_DATA.items()]

    for name, abbr, county, pop, lat, lng, zip_code, phase in city_list:
        slug = city_slug(name, abbr)
        all_cities.append({
            "name": name,
            "state": STATE_NAMES[abbr],
            "state_abbr": abbr,
            "slug": slug,
            "county": county,
            "population": pop,
            "lat": lat,
            "lng": lng,
            "zip": zip_code,
            "phase": phase,
        })

    # Compute nearby_cities: up to 5 closest within 80 km, same phase
    for city in all_cities:
        distances = []
        for other in all_cities:
            if other["slug"] == city["slug"]:
                continue
            d = haversine_km(city["lat"], city["lng"], other["lat"], other["lng"])
            if d <= 80:
                distances.append((d, other["slug"]))
        distances.sort()
        city["nearby_cities"] = [s for _, s in distances[:5]]

    all_cities.sort(key=lambda c: (c["state"], c["name"]))
    return all_cities

# ── Build services.json ───────────────────────────────────────────────────────

SERVICES = [
    {
        "name": "Foundation Repair",
        "slug": "foundation-repair",
        "description": "Expert foundation repair contractors for crack repair, underpinning, wall stabilization, and structural fixes.",
        "avg_cost_min": 2000,
        "avg_cost_max": 15000,
        "lead_value_min": 50,
        "lead_value_max": 150,
        "affiliate_url": "https://www.angi.com/companylist/foundation-repair.htm",
        "priority": 1,
        "keywords": ["foundation repair", "foundation contractor", "foundation crack repair", "foundation problems"]
    },
    {
        "name": "Excavation Contractors",
        "slug": "excavation-contractors",
        "description": "Licensed excavation contractors for site prep, grading, trenching, land clearing, and utility work.",
        "avg_cost_min": 1500,
        "avg_cost_max": 12000,
        "lead_value_min": 40,
        "lead_value_max": 120,
        "affiliate_url": "https://www.angi.com/companylist/excavating-contractors.htm",
        "priority": 1,
        "keywords": ["excavation contractors", "excavating contractor", "site excavation", "land excavation"]
    },
    {
        "name": "Basement Waterproofing",
        "slug": "basement-waterproofing",
        "description": "Trusted basement waterproofing contractors for interior drainage, sump pumps, exterior waterproofing, and encapsulation.",
        "avg_cost_min": 3000,
        "avg_cost_max": 10000,
        "lead_value_min": 60,
        "lead_value_max": 150,
        "affiliate_url": "https://www.angi.com/companylist/waterproofing.htm",
        "priority": 1,
        "keywords": ["basement waterproofing", "waterproofing contractor", "wet basement", "basement leak repair"]
    },
    {
        "name": "Snow Removal",
        "slug": "snow-removal",
        "description": "Commercial and residential snow removal services including plowing, salting, and seasonal contracts.",
        "avg_cost_min": 300,
        "avg_cost_max": 3000,
        "lead_value_min": 30,
        "lead_value_max": 80,
        "affiliate_url": "https://www.angi.com/companylist/snow-removal.htm",
        "priority": 1,
        "keywords": ["snow removal", "snow plowing", "snow removal service", "commercial snow removal"]
    },
]

# ── Build companies/[service].json ────────────────────────────────────────────

def build_companies(cities_by_slug: dict):
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    by_service: dict[str, list] = {}
    skipped = 0

    # Track slugs per service to ensure uniqueness
    slug_counters: dict[str, dict[str, int]] = {}

    for row in rows:
        svc = service_slug(row['service'])
        cname = row['city'].strip()
        state = row['state'].strip()
        cslug = city_slug(cname, state)

        if cslug not in cities_by_slug:
            skipped += 1
            continue

        rating_raw = row['google_rating'].strip()
        reviews_raw = row['google_reviews_count'].strip()
        try:
            rating = float(rating_raw)
        except ValueError:
            skipped += 1
            continue
        try:
            reviews = int(reviews_raw)
        except ValueError:
            reviews = 0

        if rating < 3.5 or reviews < 1:
            skipped += 1
            continue

        address = row['address'].strip()
        zip_code = extract_zip(address)
        if not zip_code:
            zip_code = cities_by_slug[cslug].get('zip', '')
        if not address or address.startswith('Serving'):
            address = f"{cname}, {state} {zip_code}".strip()

        phone = normalize_phone(row['phone'])

        company_name = row['company_name'].strip()
        base_slug = to_slug(company_name)

        # Unique slug per service
        if svc not in slug_counters:
            slug_counters[svc] = {}
        count = slug_counters[svc].get(base_slug, 0)
        slug_counters[svc][base_slug] = count + 1
        final_slug = base_slug if count == 0 else f"{base_slug}-{count}"

        logo_url = row.get('logo_url', '').strip() or None
        website = row.get('actual_website', '').strip() or None
        if website and 'angi.com' in website:
            website = None  # strip angi links from website field

        entry = {
            "name": company_name,
            "slug": final_slug,
            "city_slug": cslug,
            "service_slug": svc,
            "address": address,
            "zip": zip_code,
            "phone": phone,
            "rating": rating,
            "review_count": reviews,
            "google_maps_url": row.get('source_url', '').strip() or None,
            "website": website,
            "logo_url": logo_url,
            "claimed": False,
            "featured": False,
        }

        by_service.setdefault(svc, []).append(entry)

    print(f"Skipped: {skipped}")
    for svc, companies in by_service.items():
        print(f"  {svc}: {len(companies)} companies")

    return by_service

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Building cities.json...")
    cities = build_cities()
    cities_path = SRC_DATA / "cities.json"
    cities_path.write_text(json.dumps(cities, indent=2, ensure_ascii=False))
    print(f"  Written: {cities_path} ({len(cities)} cities)")

    print("Building services.json...")
    services_path = SRC_DATA / "services.json"
    services_path.write_text(json.dumps(SERVICES, indent=2, ensure_ascii=False))
    print(f"  Written: {services_path} ({len(SERVICES)} services)")

    cities_by_slug = {c['slug']: c for c in cities}

    print("Building companies JSON files...")
    companies = build_companies(cities_by_slug)
    for svc, entries in companies.items():
        out_path = SRC_DATA / "companies" / f"{svc}.json"
        out_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
        print(f"  Written: {out_path} ({len(entries)} entries)")

    # Summary: pages that will be generated
    print("\nPage coverage summary:")
    from collections import defaultdict
    page_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for svc, entries in companies.items():
        for e in entries:
            page_counts[svc][e['city_slug']] += 1

    total_pages = 0
    gaps = []
    for svc, city_map in sorted(page_counts.items()):
        publishable = sum(1 for c, n in city_map.items() if n >= 3)
        total_pages += publishable
        for c, n in city_map.items():
            if n < 3:
                gaps.append((c, svc, n))
        print(f"  {svc}: {publishable} publishable pages ({len(city_map)} cities total)")

    print(f"\nTotal publishable pages: {total_pages}")
    if gaps:
        print(f"Gaps (<3 companies, will NOT be generated):")
        for c, s, n in sorted(gaps):
            print(f"  {c} / {s}: {n}")

if __name__ == '__main__':
    main()
