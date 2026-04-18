import json
from models import Counts
from common import data_request, is_orphan, has_hotter_star, get_planet_size
from constants import PLANET_SIZE


orphan_cnt = 0
hottest_star_temp = 0
star_temp_unknown = 0
hottest_star_planet = ""
size_by_year = {}

try:
    data = data_request()
    if len(data) > 0:
        planets = json.loads(data)
except (ValueError, KeyError, TypeError):
    print("JSON format error")

print(f"Total planets: {len(planets)}")
for p in planets:
    if is_orphan(p):
        orphan_cnt += 1

    hotter = has_hotter_star(p, hottest_star_temp)
    if 'HostStarTempK' in hotter:
        hottest_star_planet = hotter['PlanetIdentifier']
        hottest_star_temp = hotter['HostStarTempK']

    try:
        year = p['DiscoveryYear']
        if year in size_by_year:
            counts = size_by_year[year]
        else:
            counts = Counts(year)
        planet_size = get_planet_size(p)
        if planet_size == 0:
            counts.unknown_count += 1
        elif planet_size < PLANET_SIZE["SMALL"]:
            counts.small_count += 1
        elif planet_size < PLANET_SIZE["MEDIUM"]:
            counts.medium_count += 1
        else:
            counts.large_count += 1
        size_by_year.update({year: counts})
    except (ValueError, KeyError):
        print(f"Unknown planet size {year}  data: {p['RadiusJpt']}")


print(f"Orphan planet count: {orphan_cnt}")
print(f"Planet orbiting Hottest Star: {hottest_star_planet}")
for k in sorted(size_by_year.keys(), key=lambda x: (x == "", x if x != "" else 0)):
    if k == "":
        print(f"{size_by_year[k].small_count} small planets, {size_by_year[k].medium_count} medium planets, {size_by_year[k].large_count} large planets, and {size_by_year[k].unknown_count} unknown size had no year of discovery")
    else:
        print(f"in {k} we discoverd {size_by_year[k].small_count} small planets, {size_by_year[k].medium_count} medium planets, {size_by_year[k].large_count} large planets, and {size_by_year[k].unknown_count} unknown size:")
