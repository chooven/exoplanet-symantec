import requests
from models import Counts
import constants


def data_request():
    response = requests.get(constants.SITE_URL)
    if response.ok:
        return response.content
    else:
        return ""


def is_orphan(planet):
    try:
        if planet['TypeFlag'] == 3:
            return True
    except (ValueError, KeyError):
        pass
    return False


def has_hotter_star(planet, hottest_star_temp):
    hottest = {}
    try:
        host_temp = int(planet['HostStarTempK'])
        if host_temp > hottest_star_temp:
            hottest['HostStarTempK'] = planet['HostStarTempK']
            hottest["PlanetIdentifier"] = planet['PlanetIdentifier']
    except (ValueError, KeyError):
        pass

    return hottest


def get_planet_size(planet):
    size = 0.0

    try:
        radius = float(planet['RadiusJpt'])
        if radius >= 0:
            size = radius

    except (ValueError, KeyError, TypeError):
        pass
    return size
