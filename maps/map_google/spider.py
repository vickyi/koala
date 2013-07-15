# coding=utf-8
__author__ = 'vic'

import json, time, sys, re
import mechanize
from crud import MongoCRUD
# from LatLngUtil import PointOnEarth
from conf import types, app_keys


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
init_browser = init_browser()


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
        self.keys = app_keys
        self.key = self.app_keys_pop()

    def app_keys_pop(self):
        if len(self.keys) > 0:
            key = self.keys.pop()
            return key
        else:
            print "*------*-*all app keys have been used*-*-----*"
            sys.exit()

    def change_radius(self):
        radius = 500
        return radius

    def change_language(self):
        language = 'zh-TW'
        return language

    def get_url(self, location, type):
        url = 'https://maps.googleapis.com/maps/api/place/search/json?sensor=false'
        url += '&language=%s' % self.change_language()
        url += '&location=' + '%s,%s' % (location['lat'], location['lng'])
        url += '&radius=%s' % self.change_radius() # 500 m
        url += '&types=establishment|%s' % '|'.join(type)
        url += '&key=%s' % self.key
        url += '&pagetoken='
        return url

    def run(self):
        all_locations = self.crud.read_all_locations()
        if len(self.keys) > 0:
            for location in all_locations:
                for type in types:
                    url = self.get_url(location, type)
                    print url
                    self.parse_html(url)
                self.crud.update_location_status(location['_id'])
        else:
            print "*------*-*all app keys have been used*-*-----*"
            sys.exit()

    def parse_html(self, url):
        # Show the source
        time.sleep(2)
        br = Browser(url)
        josn_response = br.get_html()
        status = josn_response['status']
        if status == 'OK':
            results = josn_response['results']
            # insert to mongo
            self.crud.save_map_data_insert(results)
            if 'next_page_token' in josn_response:
                pagetoken = '&pagetoken=%s' % josn_response['next_page_token']
                url = re.sub(r'&pagetoken=.*', pagetoken, url)
                self.parse_html(url)
            else:
                pass
        elif status == 'OVER_QUERY_LIMIT':
            self.key = self.app_keys_pop()
            url = re.sub(r'&key=.*&pagetoken', '&key=%s&pagetoken' % self.key, url)
            self.parse_html(url)
        else:
            return

if __name__ == "__main__":
    gpp = GooglePlacesParser()
    gpp.run()