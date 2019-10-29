import requests
from models import Counts


def data_request():
    response = requests.get(
        "https://gist.githubusercontent.com/joelbirchler/66cf8045fcbb6515557347c05d789b4a/raw/9a196385b44d4288431eef74896c0512bad3defe/exoplanets")
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


def has_hotterStar(planet, hottestStarTemp):
    hottest = dict()
    try:
        hostTemp = int(planet['HostStarTempK'])
        if(hostTemp > hottestStarTemp):
            hottest['HostStarTempK'] = planet['HostStarTempK']
            hottest["PlanetIdentifier"] = planet['PlanetIdentifier']
    except (ValueError, KeyError):
        pass

    return hottest


def get_planet_size(planet):
    size = 0.0
    try:
        if(planet['RadiusJpt'] >= 0):
            size = float(planet['RadiusJpt'])

    except(ValueError, KeyError):
        pass
    return size
