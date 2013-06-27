# coding=utf-8
__author__ = 'vic'

import json
import mechanize
from crud import MongoCRUD, MongoDriver
from LatLngUtil import PointOnEarth


def init_browser():
    # Browser
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-Agent',
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15. 0.1 FirePHP/0.7.1 AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19')]

    return br

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)

init_browser = init_browser()
level1_types = ['food', 'cafe', 'school', 'restaurant', 'night_club']
level2_types = ['shopping_mall', 'park', 'hair_care', 'museum', 'amusement_park', 'zoo']
app_keys = [ 'AIzaSyDZaHRpC3xQYFOBZlopW-awRSIKFKIjryM', 'AIzaSyAbXwgxk38zXdlfv1BVMcMVehZtnWEVewU']


class Browser():
    def __init__(self, url):
        self.url = url

    def get_html(self):
        br = init_browser.open(self.url)
        html = br.read()
        josn_html = json.loads(html)
        return josn_html


class GooglePlacesParser():

    def __init__(self):
        self.crud = MongoCRUD()

    def change_radius(self):
        radius = 500
        return radius

    def change_language(self):
        language = 'zh-TW'
        return language

    def get_url(self, key, location, type):
        url = 'https://maps.googleapis.com/maps/api/place/search/json?sensor=false'
        url += '&language=%s' % self.change_language()
        url += '&location=' + '%s,%s' % (location['lat'], location['lng'])
        url += '&radius=%s' % self.change_radius() # 500 m
        url += '&types=%s' % '|'.join(type)
        url += '&key=%s' % key
        url += '&pagetoken='
        return url

    def change_app_key(self):
        for app_key in app_keys:
            self.request_times = 0
            while self.request_times <= 1000:
                self.get_all_locations(app_key)

    def get_all_locations(self, app_key):
        all_locations = self.crud.read_all_locations()
        for location in all_locations:
            for type in [level1_types, level2_types]:
                self.url = self.get_url(app_key, location, type)
                print self.url
                self.parse_html(self.url)

    def parse_html(self, url):
        # Show the source
        br = Browser(url)
        josn_html = br.get_html()
        status = josn_html['status']
        if status == 'OK':
            results = josn_html['results']
            # insert to mongo
            self.crud.save_map_data_insert(results)
            self.request_times += 1
            if 'next_page_token' in josn_html:
                url = self.url + '%s' % josn_html['next_page_token']
                self.parse_html(url)
            else:
                pass
        else:
            return

# from datetime import datetime

if __name__ == "__main__":
    gpp = GooglePlacesParser()
    # border_location_right = {
    #     "lat": 24.970,
    #     "lng": 121.666
    # }
    # print gpp.get_url(app_keys[0], border_location_right, 'food')
    gpp.change_app_key()