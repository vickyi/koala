#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (c) 2013 V zhang <dolphinzhang1987@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created on 2013-6-9

@author: V
'''

import os

# from koala.core.config import Config
#
# base = os.path.dirname(os.path.abspath(__file__))
# user_conf = os.path.join(base, 'test.yaml')
# if not os.path.exists(user_conf):
#     user_conf = os.path.join(base, 'map_google.yaml')
# user_config = Config(user_conf)
#
# starts = [str(start.uid) for start in user_config.job.starts]
#
# mongo_host = user_config.job.mongo.host
# mongo_port = user_config.job.mongo.port
# db_name = user_config.job.db
#
# instances = user_config.job.instances

# level1_types = ['food', 'restaurant',  'amusement_park', 'park']
# level2_types = ['cafe', 'school', 'night_club', 'zoo']
# level3_types = ['shopping_mall', 'hair_care', 'museum']

le1 = ["accounting", "airport", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station", "campground", "car_dealer", "car_rental", "car_repair", "car_wash"]
le2 = ["casino", "cemetery", "church", "city_hall", "clothing_store", "convenience_store", "courthouse", "dentist", "department_store", "doctor", "electrician", "electronics_store", "embassy", "establishment", "finance", "fire_station", "florist", "funeral_home", "furniture_store"]
le3 = ["gas_station", "general_contractor", "grocery_or_supermarket", "gym","hardware_store", "health", "hindu_temple", "home_goods_store", "hospital", "insurance_agency", "jewelry_store", "laundry", "lawyer", "library", "liquor_store", "local_government_office", "locksmith", "lodging", "meal_delivery"]
le4 = ["meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "painter", "parking", "pet_store", "pharmacy", "physiotherapist", "place_of_worship", "plumber", "police", "post_office", "real_estate_agency", "roofing_contractor"]
le5 = ["rv_park", "shoe_store", "spa", "stadium", "storage", "store", "subway_station", "synagogue", "taxi_stand", "train_station", "travel_agency", "university", "veterinary_care"]
le6 = ['food', 'restaurant',  'amusement_park', 'park', 'cafe', 'school', 'night_club', 'zoo', 'shopping_mall', 'hair_care', 'museum']
types = [le1, le2, le3, le4, le5]
app_keys = []
