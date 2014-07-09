# -*- coding: utf-8 -*-

import unittest

from nominatim import *


def result_has_osm_id(res, osm_id):
    for r in res:
        if r['osm_id'] == osm_id:
            return True
    return False

def address_has_city(address, city):
    if not isinstance(address, dict):
        return False
    if not 'city' in address:
        return False
    return address['city'] == city


class TestNominatim(unittest.TestCase):
    def test_geocoding_default_url(self):
        n = Nominatim()
        location = 'Helsinki'
        res = n.query(location)
        self.assertTrue(result_has_osm_id(res, '34914'))

    def test_geocoding_osm_url(self):
        n = Nominatim('http://nominatim.openstreetmap.org')
        location = 'Helsinki'
        res = n.query(location)
        self.assertTrue(result_has_osm_id(res, '34914'))

    def test_reverse_geocoding_default_url(self):
        n = NominatimReverse()
        lat = 60.1666277
        lon = 24.9435079
        res = n.query(lat=lat, lon=lon, zoom='city')
        self.assertTrue(isinstance(res, dict))
        self.assertTrue('address' in  res)
        self.assertTrue(address_has_city(res['address'], 'Helsinki'))

    def test_reverse_geocoding_osm_url(self):
        n = NominatimReverse('http://nominatim.openstreetmap.org')
        lat = 60.1666277
        lon = 24.9435079
        res = n.query(lat=lat, lon=lon, zoom='city')
        self.assertTrue(isinstance(res, dict))
        self.assertTrue('address' in  res)
        self.assertTrue(address_has_city(res['address'], 'Helsinki'))

    def test_reverse_geocoding_from_osm_id_default_url(self):
        n = NominatimReverse()
        osm_id = '184705'
        osm_type = 'R'
        res = n.query(osm_id=osm_id, osm_type=osm_type, zoom='city')
        self.assertTrue(isinstance(res, dict))
        self.assertTrue('address' in  res)
        self.assertTrue(address_has_city(res['address'], 'Helsinki'))

    def test_reverse_geocoding_from_osm_id_osm_url(self):
        n = NominatimReverse('http://nominatim.openstreetmap.org')
        osm_id = '184705'
        osm_type = 'R'
        res = n.query(osm_id=osm_id, osm_type=osm_type, zoom='city')
        self.assertTrue(isinstance(res, dict))
        self.assertTrue('address' in  res)
        self.assertTrue(address_has_city(res['address'], 'Helsinki'))

    def test_invalid_osm_type(self):
        n = NominatimReverse()
        with self.assertRaises(NominatimException):
            osm_id = '184705'
            osm_type = 'X'
            res = n.query(osm_id=osm_id, osm_type=osm_type, zoom='city')