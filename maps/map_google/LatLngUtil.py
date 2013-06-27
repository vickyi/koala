# -*- coding: utf-8 -*-
__author__ = 'vic'

import math
from math import sin, asin, cos, degrees #, radians, fabs, sqrt


class PointOnEarth:
    tolerance = 0.000000001# 公差
    R = 6371300.0

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

    def distanceTo(self, p):
        return self.radToDis(
            math.acos(
                math.cos(
                    self.degToRad(self.lat)
                ) * math.cos(
                    self.degToRad(p.lat)
                ) * math.cos(
                    self.degToRad(self.lng - p.lng)
                ) + math.sin(
                    self.degToRad(self.lat)
                ) * math.sin(
                    self.degToRad(p.lat)
                )
            )
        )

    def getAround(self, lat, lng, raidus):
        PI = math.pi
        latitude = lat
        longitude = lng

        degree = (24901 * 1609) / 360.0
        raidusMile = raidus

        dpmLat = 1 / degree
        radiusLat = dpmLat * raidusMile
        minLat = latitude - radiusLat
        maxLat = latitude + radiusLat

        mpdLng = degree * math.cos(latitude * (PI / 180))
        dpmLng = 1 / mpdLng
        radiusLng = dpmLng * raidusMile
        minLng = longitude - radiusLng
        maxLng = longitude + radiusLng
        print minLat, minLng
        print maxLat, maxLng

    def get_lat_lng(self, lat, lng, distance):
        EARTH_RADIUS = 6371.3
        dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat))
        dlng = degrees(dlng)        # 弧度转换成角度
        dlat = distance / EARTH_RADIUS
        dlng = degrees(dlat)     # 弧度转换成角度
        print "left:", lat + dlat, lng
        print "left-top    :", lat + dlat, lng - dlng
        print "right-top   :", lat + dlat, lng + dlng
        print "left-bottom :", lat - dlat, lng - dlng
        print "right-bottom:", lat - dlat, lng + dlng

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

    # def get_locations_all(self):
    #     locations = []
    #
    #     for i in range(0, 360, 90):
    #         location = {}
    #         p2 = self.getPointBydirection(i, 1)
    #         location['lat'] = p2.lat
    #         location['lng'] = p2.lng
    #         locations.append(location)
    #     return locations

    def get_location(self, direction=0, radius=0.5):
        p2 = self.getPointBydirection(direction, radius)
        return {'lat': p2.lat, 'lng': p2.lng}

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

if __name__ == "__main__":
    p = PointOnEarth(121.458, 24.960)
    # p.getAround(121.5598, 25.0910, 1000)
    # p.get_lat_lng(121.5598, 25.0910, 1)
    locations = p.get_locations()
    # p.get_location()
    for i in locations:
        print i.values