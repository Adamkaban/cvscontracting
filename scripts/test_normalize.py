import normalize as n

def check(name, got, want):
    assert got == want, f"{name}: got {got!r} want {want!r}"
    print("ok", name)

# slugify
check("slug1", n.slugify("Aqua-Guard Waterproofing LLC"), "aqua-guard-waterproofing-llc")
check("slug2", n.slugify("J&D Construction, Inc."), "jd-construction-inc")

# parse_years
check("yr1", n.parse_years("30 years"), 30)
check("yr2", n.parse_years("30"), 30)
check("yr3", n.parse_years(""), None)
check("yr4", n.parse_years("Contact business"), None)
check("yr5", n.parse_years("250 years"), None)  # implausible -> None

# norm_insured
check("ins1", n.norm_insured("Yes"), True)
check("ins2", n.norm_insured("yes."), True)
check("ins3", n.norm_insured("Self-reported, homeowners should verify"), None)
check("ins4", n.norm_insured("undefined"), None)
check("ins5", n.norm_insured("No"), None)

# norm_bbb
check("bbb1", n.norm_bbb("A+"), "A+")
check("bbb2", n.norm_bbb("A"), "A")
check("bbb3", n.norm_bbb("No Rating"), None)
check("bbb4", n.norm_bbb(""), None)

# clean_area
check("area1", n.clean_area("undefined"), None)
check("area2", n.clean_area("Nationwide in the United States"), None)
check("area3", n.clean_area("Cumberland County"), "Cumberland County")

# domain_from_url
check("dom1", n.domain_from_url("https://www.groundworks.com"), "groundworks.com")
check("dom2", n.domain_from_url(""), None)

# make_blurb (no em-dash, structured only)
b = n.make_blurb("basement-waterproofing", "Portland", "Cumberland County", 30)
check("blurb1", b, "Basement waterproofing in Portland, serving Cumberland County, 30+ yrs experience")
assert "—" not in b, "blurb must not contain em-dash"
print("ok blurb-no-emdash")

# quality_score monotonic
assert n.quality_score(4.8, 100) > n.quality_score(4.8, 5)
assert n.quality_score(4.9, 50) > n.quality_score(4.0, 50)
print("ok quality_score")

print("ALL PASS")
