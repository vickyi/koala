# -*- coding: utf-8 -*-
__author__ = 'vic'

import math
from math import sin, asin, cos, degrees #, radians, fabs, sqrt


class PointOnEarth:
    tolerance = 0.0000001# 公差
    R = 6371.3

    def __init__(self, lng=0.0, lat=0.0):
        """
        "lat" :  latitude 纬度
        赤道是最长的纬线，长约4万千米

        "lng" : longitude 经度
        """
        self.lng = lng
        self.lat = lat

    def radToDeg(self, radian):
        return radian * 180.0 / math.pi

    def degToRad(self, degree):
        return math.pi * degree / 180.0

    def disToRad(self, distance):
        return distance / self.R

    def radToDis(self, radian):
        return radian * self.R

    # def distanceTo(self, p):
    #     return self.radToDis(
    #         math.acos(
    #             math.cos(
    #                 self.degToRad(self.lat)
    #             ) * math.cos(
    #                 self.degToRad(p.lat)
    #             ) * math.cos(
    #                 self.degToRad(self.lng - p.lng)
    #             ) + math.sin(
    #                 self.degToRad(self.lat)
    #             ) * math.sin(
    #                 self.degToRad(p.lat)
    #             )
    #         )
    #     )

    def getPointBydirection(self, direction, distance):
        """

        @param direction:
        @param distance:
        @return:
        """
        direct = self.degToRad(direction)
        r = self.disToRad(distance)
        lng = self.degToRad(self.lng)
        lat = self.degToRad(self.lat)
        lonDiff = 0.0
        p = PointOnEarth()
        s = math.sin(r) * math.sin(r) * math.cos(direct) + math.cos(r) * math.cos(r)
        sinLatX = (s * math.cos(lat) - math.cos(r) * math.cos(lat + r)) / math.sin(r)

        if -sinLatX * sinLatX + 1.0 < self.tolerance * self.tolerance:
            if (math.pi / 2) < direct < (math.pi * 3 / 2):
                p.lat = -math.pi / 2
            else:
                p.lat = math.pi / 2
            lonDiff = 0.0
        else:
            p.lat = math.asin(sinLatX)
            if (math.cos(lat) * math.cos(lat) < self.tolerance * self.tolerance):#Point p is polar.
                lonDiff = math.pi - direct
            else: # Point p is not polar.
                cosLonDiff = (math.cos(r) - math.sin(p.lat) * math.sin(lat)) / (math.cos(p.lat) * math.cos(lat))
                if -cosLonDiff * cosLonDiff + 1.0 < self.tolerance * self.tolerance:
                    if cosLonDiff > 0.0:
                        lonDiff = 0.0
                    else:
                        lonDiff = math.pi
                else:
                    lonDiff = math.acos(cosLonDiff)
                    if direct > math.pi:
                        lonDiff = -lonDiff
        p.lng = lng + lonDiff
        while p.lng > math.pi or p.lng < -math.pi:
            if p.lng > 0.0:
                p.lng = p.lng - math.pi * 2
            else:
                p.lng = p.lng + math.pi * 2
        p.lng = self.radToDeg(p.lng)
        p.lat = self.radToDeg(p.lat)
        return p

    def get_location(self, direction=0, radius=0.5):
        p2 = self.getPointBydirection(direction, radius)
        return {'lat': round(p2.lat, 8), 'lng': round(p2.lng, 8)}

    def test_get_location(self, direction=0, radius=0.5):
        border_location_right = {
            "lat": '25.028',
            "lng": '121.666'
        }
        t_location = {
            "lat": 25.028,
            "lng": 121.666
        }
        print '%s,%s' % (t_location['lat'], t_location['lng'])
        print ','.join(border_location_right.values())

    def get_circle(self, lat, lng, distance):
        EARTH_RADIUS = 6371
        dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat))
        dlng = degrees(dlng)        # 弧度转换成角度

if __name__ == "__main__":
    p = PointOnEarth(121.458, 24.960)
