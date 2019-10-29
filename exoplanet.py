import json
from models import Counts
from common import data_request, is_orphan, has_hotterStar, get_planet_size
from constants import PLANET_SIZE


orphanCnt = 0
hottestStarTemp = 0
StarTempUnknown = 0
hottestStarPlanet = ""
sizeByYear = {}

try:
    data = data_request()
    if(len(data) > 0):
        planets = json.loads(data)
except (ValueError, KeyError, TypeError):
    print "JSON format error"

print "Total planets: %s" % len(planets)
for p in planets:
    if(is_orphan(p)):
        orphanCnt += 1

    hotter = has_hotterStar(p, hottestStarTemp)
    if 'HostStarTempK' in hotter:
        hottestStartPlanet = hotter['PlanetIdentifier']
        hottestStarTemp = hotter['HostStarTempK']

    try:
        year = p['DiscoveryYear']
        if(sizeByYear.has_key(year)):
            counts = sizeByYear[year]
        else:
            counts = Counts(year)
        planetSize = get_planet_size(p)
        if(planetSize == 0):
            counts.unknown_count += 1
        elif(planetSize < PLANET_SIZE["SMALL"]):
            counts.small_count += 1
        elif(planetSize < PLANET_SIZE["MEDIUM"]):
            counts.medium_count += 1
        else:
            counts.large_count += 1
        sizeByYear.update({year: counts})
    except (ValueError, KeyError):
        print "Unknown planet size %s  data: %s" % (year, p['RadiusJpt'])
        pass


print "Orphan planet count: %s" % orphanCnt
print "Planet orbiting Hottest Star is %s " % hottestStartPlanet
for k in sorted(sizeByYear.keys()):
    if(k == ""):
        print "%s small planets, %s medium planets, %s large planets, and %s unknown size had no year of discovery" % (
            sizeByYear[k].small_count, sizeByYear[k].medium_count, sizeByYear[k].large_count, sizeByYear[k].unknown_count)
    else:
        print "in %s we discoverd %s small planets, %s medium planets, %s large planets, and %s unknown size:" % (
            k, sizeByYear[k].small_count, sizeByYear[k].medium_count, sizeByYear[k].large_count, sizeByYear[k].unknown_count)
