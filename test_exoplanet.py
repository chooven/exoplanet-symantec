import unittest
from common import data_request, is_orphan, has_hotter_star, get_planet_size
from constants import PLANET_SIZE


class TestExoplanet(unittest.TestCase):

    def setUp(self):
        self.planet1 = {"PlanetIdentifier": "Kepler-1253 b",
                        "TypeFlag": 3,
                        "RadiusJpt": "",
                        "HostStarTempK": 5000}
        self.planet2 = {"PlanetIdentifier": "Kepler-1253 b",
                        "TypeFlag": 2,
                        "RadiusJpt": 0.0456,
                        "HostStarTempK": 4567}
        self.planet3 = {"PlanetIdentifier": "Kepler-1253 b",
                        "TypeFlag": 2,
                        "RadiusJpt": 1.0456,
                        "HostStarTempK": 4567}

    def tearDown(self):
        pass

    def test_is_orphan(self):
        result = is_orphan(self.planet1)
        self.assertTrue(result)

        result = is_orphan(self.planet2)
        self.assertFalse(result)

    def test_has_hotter_star(self):
        result = has_hotter_star(self.planet1, 4999)
        self.assertEqual(result['PlanetIdentifier'],
                          self.planet1['PlanetIdentifier'])

        result = has_hotter_star(self.planet1, 5001)
        self.assertFalse('HostStarTempK' in result)

    def test_get_planet_size(self):
        result = get_planet_size(self.planet1)
        self.assertEqual(result, PLANET_SIZE["UNKNOWN"])

        result = get_planet_size(self.planet2)
        self.assertNotEqual(result, PLANET_SIZE["SMALL"])


if __name__ == '__main__':
    unittest.main()
