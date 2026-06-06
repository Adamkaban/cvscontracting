#!/usr/bin/env python3
"""CSV -> enriched per-service company JSON for CVS Contracting."""
import csv, json, math, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_IN = ROOT / "scripts" / "raw" / "companies_filtered.csv"
CITIES = ROOT / "src" / "data" / "cities.json"
LOGO_DIR = ROOT / "public" / "logos"
OUT_DIR = ROOT / "src" / "data" / "companies"

SERVICE_MAP = {
    "basement waterproofing": "basement-waterproofing",
    "foundation repair": "foundation-repair",
    "snow removal": "snow-removal",
    "excavation contractors": "excavation-contractors",
}
SERVICE_TITLE = {
    "basement-waterproofing": "Basement waterproofing",
    "foundation-repair": "Foundation repair",
    "snow-removal": "Snow removal",
    "excavation-contractors": "Excavation contractors",
}
BAD_VALUES = {
    "", "undefined", "not provided", "not available", "n/a",
    "no information available", "contact business for details",
    "nationwide in the united states", "no rating", "nr", "none",
}

def slugify(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s

def parse_years(s):
    m = re.search(r"\d+", s or "")
    if not m:
        return None
    n = int(m.group())
    return n if 1 <= n <= 150 else None

def norm_insured(s):
    v = (s or "").strip().lower().rstrip(".")
    return True if v in {"yes", "y"} else None

def norm_bbb(s):
    v = (s or "").strip()
    return v if re.fullmatch(r"[A-F][+-]?", v) else None

def clean_area(s):
    v = (s or "").strip()
    if v.lower() in BAD_VALUES:
        return None
    if len(v) > 40:
        v = v[:40].rsplit(" ", 1)[0]
    return v or None

def domain_from_url(s):
    s = (s or "").strip()
    if not s:
        return None
    s = re.sub(r"^https?://", "", s).rstrip("/")
    s = re.sub(r"^www\.", "", s)
    s = s.split("/")[0].lower()
    return s or None

def make_blurb(service_slug, city, area, years):
    parts = [f"{SERVICE_TITLE[service_slug]} in {city}"]
    if area:
        parts.append(f"serving {area}")
    if years:
        parts.append(f"{years}+ yrs experience")
    return ", ".join(parts)

def quality_score(rating, reviews):
    return float(rating) * math.log10(int(reviews) + 1)

def load_cities():
    data = json.loads(CITIES.read_text())
    by_key = {}
    for c in data:
        by_key[(c["name"].strip().lower(), c["state_abbr"].strip().lower())] = c
    return by_key

def find_logo(*urls):
    for u in urls:
        d = domain_from_url(u)
        if d and (LOGO_DIR / f"{d}.png").exists():
            return f"/logos/{d}.png"
    return None

def main():
    cities = load_cities()
    rows = list(csv.DictReader(CSV_IN.open(encoding="utf-8")))
    buckets = {s: {} for s in SERVICE_MAP.values()}  # service -> {(slug,city): company}

    for r in rows:
        service = SERVICE_MAP.get((r.get("service") or "").strip().lower())
        if not service:
            continue
        try:
            rating = float(r.get("google_rating") or 0)
            reviews = int(float(r.get("google_reviews_count") or 0))
        except ValueError:
            continue
        if rating < 3.5 or reviews < 1:
            continue
        city_name = (r.get("city") or "").strip()
        state = (r.get("state") or "").strip()
        city = cities.get((city_name.lower(), state.lower()))
        if not city:
            continue
        name = (r.get("company_name") or "").strip()
        if not name:
            continue
        key = (slugify(name), city["slug"])
        if key in buckets[service]:
            continue  # dedupe by name+city, keep first
        years = parse_years(r.get("years_in_business"))
        area = clean_area(r.get("service_area"))
        phone = (r.get("phone") or "").strip()
        phone = phone if phone and phone.lower() != "not provided" else None
        website = (r.get("actual_website") or r.get("website") or "").strip() or None
        company = {
            "name": name,
            "slug": slugify(name),
            "city_slug": city["slug"],
            "service_slug": service,
            "address": (r.get("address") or "").strip(),
            "zip": (re.findall(r"\b\d{5}\b", r.get("address") or "") or [city.get("zip", "")])[-1],
            "phone": phone,
            "rating": round(rating, 1),
            "review_count": reviews,
            "google_maps_url": (r.get("source_url") or "").strip() or None,
            "website": website,
            "logo_url": find_logo(r.get("actual_website"), r.get("website"), r.get("logo_url")),
            "claimed": False,
            "featured": False,
            "_score": quality_score(rating, reviews),
        }
        if years is not None:
            company["years_in_business"] = years
        ins = norm_insured(r.get("insured"))
        if ins:
            company["insured"] = True
        bbb = norm_bbb(r.get("bbb_rating"))
        if bbb:
            company["bbb_rating"] = bbb
        if area:
            company["service_area"] = area
        company["blurb"] = make_blurb(service, city["name"], area, years)
        buckets[service][key] = company

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {}
    for service, items in buckets.items():
        # group by city, drop city-groups with < 3, sort by score
        by_city = {}
        for comp in items.values():
            by_city.setdefault(comp["city_slug"], []).append(comp)
        out = []
        dropped = 0
        for cs, comps in by_city.items():
            if len(comps) < 3:
                dropped += len(comps)
                continue
            comps.sort(key=lambda c: c["_score"], reverse=True)
            out.append(comps)
        flat = [c for grp in out for c in grp]
        for c in flat:
            c.pop("_score", None)
        (OUT_DIR / f"{service}.json").write_text(
            json.dumps(flat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        summary[service] = {"companies": len(flat), "cities": len(out), "dropped_lt3": dropped}

    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
