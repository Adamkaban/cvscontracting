#!/usr/bin/env python3
"""
Download company logos from logo.dev → public/logos/{domain}.png
Update src/data/companies/*.json with local logo_url = /logos/{domain}.png
"""
import json
import re
import time
from pathlib import Path
import requests

LOGO_DEV_PUBLIC_KEY = 'pk_NFrl5GunTOeNhOmq-xZEIw'
ROOT = Path(__file__).parent.parent
LOGOS_DIR = ROOT / "public" / "logos"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)

SERVICES = [
    "basement-waterproofing",
    "foundation-repair",
    "snow-removal",
    "excavation-contractors",
]


def get_domain(logo_url: str) -> str | None:
    m = re.search(r'img\.logo\.dev/([^?]+)', logo_url)
    return m.group(1) if m else None


def download_logo(domain: str) -> bool:
    dest = LOGOS_DIR / f"{domain}.png"
    if dest.exists():
        return True

    url = f"https://img.logo.dev/{domain}?token={LOGO_DEV_PUBLIC_KEY}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200 and len(r.content) > 500:  # skip tiny placeholders
            dest.write_bytes(r.content)
            return True
        return False
    except Exception as e:
        print(f"  ERROR {domain}: {e}")
        return False


def main():
    # Collect all unique domains first
    all_data: dict[str, list] = {}
    domains: set[str] = set()

    for svc in SERVICES:
        path = ROOT / "src" / "data" / "companies" / f"{svc}.json"
        data = json.loads(path.read_text())
        all_data[svc] = data
        for company in data:
            lu = company.get("logo_url")
            if lu:
                domain = get_domain(lu)
                if domain:
                    domains.add(domain)

    print(f"Unique domains to download: {len(domains)}")

    # Download
    ok = 0
    fail = 0
    for i, domain in enumerate(sorted(domains), 1):
        dest = LOGOS_DIR / f"{domain}.png"
        if dest.exists():
            ok += 1
            continue
        success = download_logo(domain)
        if success:
            ok += 1
            print(f"  [{i}/{len(domains)}] OK  {domain}")
        else:
            fail += 1
            print(f"  [{i}/{len(domains)}] SKIP {domain} (placeholder or error)")
        time.sleep(0.1)  # polite rate limit

    print(f"\nDownloaded: {ok}, skipped/failed: {fail}")

    # Update JSON files with local paths
    updated = 0
    for svc in SERVICES:
        path = ROOT / "src" / "data" / "companies" / f"{svc}.json"
        data = all_data[svc]
        changed = False
        for company in data:
            lu = company.get("logo_url")
            if lu and lu.startswith("https://img.logo.dev/"):
                domain = get_domain(lu)
                if domain:
                    local_file = LOGOS_DIR / f"{domain}.png"
                    if local_file.exists():
                        company["logo_url"] = f"/logos/{domain}.png"
                        updated += 1
                        changed = True
                    else:
                        company["logo_url"] = None
                        changed = True
        if changed:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"Updated: {path.name}")

    print(f"Logo URLs updated: {updated}")


if __name__ == "__main__":
    main()
