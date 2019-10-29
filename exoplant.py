import requests
import json


class Counts(object):
    small_count = 0
    medium_count = 0
    large_count = 0
    unknown_count = 0

    def __init__(self, year):
        self.year = year


response = requests.get(
    "https://gist.githubusercontent.com/joelbirchler/66cf8045fcbb6515557347c05d789b4a/raw/9a196385b44d4288431eef74896c0512bad3defe/exoplanets")
# print(response.status_code)
orphanCnt = 0
hotestStarTemp = 0
StarTempUnknown = 0
hotestStartPlanet = ""
sizeByYear = {}
try:
    planets = json.loads(response.content)
except (ValueError, KeyError, TypeError):
    print "JSON format error"
print(len(planets))
for p in planets:
    if p['TypeFlag'] == 3:
        orphanCnt += 1
    try:
        if p['HostStarTempK'] == '':
            StarTempUnknown += 1
        else:
            hostTemp = int(p['HostStarTempK'])
            if hostTemp > hotestStarTemp:
                hotestStarTemp = p['HostStarTempK']
                hotestStartPlanet = p['PlanetIdentifier']
    except (ValueError, KeyError):
        pass
    try:

        year = p['DiscoveryYear']
        if(sizeByYear.has_key(year)):
            counts = sizeByYear[year]
        else:
            counts = Counts(year)
        if(p['RadiusJpt'] == ""):
            counts.unknown_count += 1
        else:
            planetSize = float(p['RadiusJpt'])
            if(planetSize < 1):
                counts.small_count += 1
            elif(planetSize < 2):
                counts.medium_count += 1
            else:
                counts.large_count += 1
        sizeByYear.update({year: counts})
    except (ValueError, KeyError):
        print "Unknown planet size %s  data: %s" % (year, p['RadiusJpt'])
        pass


print "Orphan planet count: %s" % orphanCnt
print "Planet orbiting Hotest Star is %s " % hotestStartPlanet
print "Planets with unknown host star temp: %s " % StarTempUnknown
for k in sorted(sizeByYear.keys()):
    if(k == ""):
        print "%s small planets, %s medium planets, %s large planets, and %s unknown size had no year of discovery" % (
            sizeByYear[k].small_count, sizeByYear[k].medium_count, sizeByYear[k].large_count, sizeByYear[k].unknown_count)
    else:
        print "in %s we discoverd %s small planets, %s medium planets, %s large planets, and %s unknown size:" % (
            k, sizeByYear[k].small_count, sizeByYear[k].medium_count, sizeByYear[k].large_count, sizeByYear[k].unknown_count)
