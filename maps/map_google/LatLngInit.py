# -*- coding: utf-8 -*-
__author__ = 'vic'

from LatLngUtil import PointOnEarth
from crud import MongoCRUD
import decimal


class map_location:

    border_location_top = {
        "lat": 25.210,
        "lng": 121.560
    }

    border_location_right = {
        "lat": 24.970,
        "lng": 121.666
    }

    border_location_base = {
        "lat": 24.970,
        "lng": 121.456
    }

    def init_location(self, location, degree):
        location['province'] = 'Taiwan'
        location['city'] = 'Taipei'
        location['status'] = '0'
        location['degree'] = degree
        return location

    def get_location_x(self, direction=90, radius=0.5):
        """
        东经
        lng change
        """
        loc = self.border_location_base
        locations = []
        location = loc
        locations.append(self.init_location(loc, direction))
        while location['lng'] <= self.border_location_right['lng']:
            location = self.get_direction_base(location, direction, radius)
            locations.append(self.init_location(location, direction))
            # radius += 1
        return locations

    def get_location_y(self):
        """
        北纬
        lat change
        @return:
        """
        direction = 0
        radius = 1
        locations = []
        location = self.border_location_base
        while location['lat'] <= self.border_location_top['lat']:
            location = self.get_direction_base(location, direction, radius)
            locations.append(self.init_location(location, direction))
            # radius += 1
        print 'y_locations==', locations
        self.save(locations)

    def get_direction_base(self, location_base, direction=0, radius=0.5):
        """
        """
        p = PointOnEarth(location_base['lng'], location_base['lat'])
        location = p.get_location(direction, radius)
        if location:
            return location

    def save(self, results):
        mcrud = MongoCRUD()
        mcrud.save_circle_centers(results)

    def get_location_border(self):
        """
            location，其中包含此地方的经过地址解析的纬度(lat)、经度(lng)值
        """
        locations = self.get_location_x(direction=90, radius=1)
        self.save(locations)
        for location in locations:
            self.get_location_y()

if __name__ == "__main__":
    loc = map_location()
    loc.get_location_border()
