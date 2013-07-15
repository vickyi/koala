#-*-coding:utf-8-*-

__author__ = 'vic'

from pymongo import MongoClient, errors
import math
import string
import MySQLdb
from LatLngInit import map_location

distance = 1
EARTH_RADIUS = 6371

"""
计算商圈
"""

settings = {
    'digi':16,
    'add': 10,
    'plus': 7,
    'cha': 36,
    'center': {
        'lat': 34.957995,
        'lng': 107.050781,
        'isDef': True
    }
}

def MySQLConnect():
    return MySQLdb.connect(host="192.168.11.196", user="root",passwd="111111")

def intToStr(Num, radix):
    if Num<0:
        raise Exception
    _base = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _res = ''
    while 1:
        _d = Num % radix
        _res += _base[_d]
        Num = Num / radix
        if Num == 0:
            return _res

def decodeDP_POI(a):
    try:

        b = -1
        c = 0
        d = ""
        e = len(a)
        g = ord(a[e - 1])
        a = a[0:e-1]
        e-=1
        for f in xrange(e):
            h = string.atoi(a[f], settings['cha']) - settings['add']
            if h >= settings['add']:
                h -= settings['plus']
            d += intToStr(h,settings['cha'])
            if h > c:
                b = f
                c = h

        a = string.atoi(d[0:b],settings['digi'])
        b = string.atoi(d[b + 1:], settings['digi'])
        g = (a + b - g) / 2
        b = float(b - g) / 1E5
        return {
            'lat': b,
            'lng': float(g) / 1E5
        }
    except Exception,e:
        print e

def croodOffsetDecrypt(x,y):
    x = float(x)*100000%36000000
    y = float(y)*100000%36000000

    x1 = math.floor(-(((math.cos(y/100000))*(x/18000))+((math.sin(x/100000))*(y/9000)))+x)
    y1 = math.floor(-(((math.sin(y/100000))*(x/18000))+((math.cos(x/100000))*(y/9000)))+y)

    if x>0:
        xoff=1
    else:
        xoff=-1
    if y>0:
        yoff=1
    else:
        yoff=-1
    x2 = math.floor(-(((math.cos(y1/100000))*(x1/18000))+((math.sin(x1/100000))*(y1/9000)))+x+xoff)
    y2 = math.floor(-(((math.sin(y1/100000))*(x1/18000))+((math.cos(x1/100000))*(y1/9000)))+y+yoff)

    return [x2/100000.0,y2/100000.0]

class shop_nearby_shop:
    def __init__(self,shop_id,shop_name,nearby_shop_id,nearby_shop_name,distance):
        #"商家名称","导航","商家电话","商家介绍","Google latitude","Google longitude","商家大分类","商家小分类","国家","省份","城市","地区","地标与热点","地址","星级","人均消费","图片","Google maps","标签","标签2","连锁店","全部点评","很好","好","还行","差","很差","商区","口味/产品","环境","服务","别名","推荐产品","推荐菜","餐厅氛围","餐厅特色","付款方式","营业时间","交通","价格信息","附近店铺","Shop id"
        self.shop_id=shop_id
        self.shop_name=shop_name
        self.nearby_shop_id=nearby_shop_id
        self.nearby_shop__name=nearby_shop_name
        self.distance=distance

def toMYSQL(datas):
    conn = MySQLdb.connect(host='192.168.1.111', user='root',passwd='mysql@xcj',db='data_mining_xcj',port=3306)
    cursor = conn.cursor()
    for data in datas:
        cursor.execute("insert into shop_nearby(shop_id,shop_name,nearby_shop_id,nearby_shop_name,distance) values (?,?,?,?,?)",\
            (data.m_id,data.m_name,data.s_id,data.s_name,data.distince))
    cursor.close()
    conn.close()
    '''
    cursor.execute('select * from uu')
    results=cursor.fetchall()
    for su in results:
        print su[1]
    '''

def tosavetext(data):
    nearbyshops = "nearbyshops.data"
    info = file(nearbyshops,"a")
    info.write(data)
    info.write("\n")
    info.close


class MongoDriver():

    mongo_server = {"host": "124.207.209.57", "port": 27010}

    def __init__(self):
        pass

    def MongoConnection(self):
        """
        mongo_server: host , port
        @return:
        """
        return MongoClient(host=self.mongo_server['host'], port=self.mongo_server['port'])

mongoDriver = MongoDriver()
def get_geoWithin(domain, radius=1):
    con = mongoDriver.MongoConnection()
    db = con.map_data
    google_places = db.google_places
    lng_lat = [domain[3], domain[2]]#longitude, latitude
    # print lng_lat
    chain = 'Yes'
    datas = google_places.find({"geometry": {"$within":{"$center":[lng_lat, radius]}}}).count() #,"chain_store":chain
    datas = google_places.find({"geometry": {"$near":{"$geometry":{ type : "Point", "coordinates": [121.514633,25.054277]} },"$maxDistance": 1000 } }) #,"chain_store":chain
    # print datas


def get_geoMysql(domain):
    center = {"lng": domain[3], "lat": domain[2]}
    loc = map_location()
    border = loc.get_border(center)
    top = border[0]
    right = border[1]
    bottom = border[2]
    left = border[3]
    print "border==", border
    sql = 'SELECT external_id FROM app_scene_plus.base_scene WHERE city = "台北" and ((address_lat BETWEEN %s AND %s) AND ' \
          '(address_lng BETWEEN %s AND %s))' % (bottom["lat"] *1e6, top["lat"] *1e6, left["lng"] *1e6, right["lng"] *1e6)
    print sql
    con = MySQLConnect()
    mysql_cur = con.cursor()
    mysql_cur.execute(sql)
    mysql_rows = mysql_cur.fetchall()
    if len(mysql_rows) > 0:
        insert_sql = "INSERT INTO `app_scene_plus.base_domain_scene_association` (`domain_id`,`scene_id`,`type`) " \
              "VALUES (%s, %s, %s)"
        print "mysql_rows=", mysql_rows
        for row in mysql_rows:
            data = [domain[0], row[0], "2"]
            insertOne(mysql_cur, con, insert_sql, data)


def insertOne(mysql_cur, conn, sql, data):
    try:
        print tuple(data)
        mysql_cur.execute(sql, tuple(data))
    except Exception, e:
        print 'insert Exception:', e
    conn.commit()


def getDomains():
    con = MySQLConnect()
    mysql_cur = con.cursor()
    sql = "SELECT * FROM app_scene_plus.taiwan_domain where address_lat >  0 and address_lat >  0"
    mysql_cur.execute(sql)
    mysql_rows = mysql_cur.fetchall()
    return mysql_rows

def get_border(lng, lat):
    dlat = round(distance/EARTH_RADIUS, 9)
    dlat = round(math.degrees(dlat), 9)

    dlng = round(2 * math.asin(math.sin(distance / (2 * EARTH_RADIUS)) / math.cos(lat)),  9)
    dlng = round(math.degrees(dlng), 9)

    left_top = {"lat": lat + dlat, "lng": lng - dlng}
    right_top = {"lat": lat + dlat, "lng":lng + dlng}
    left_bottom = {"lat": lat - dlat, "lng":lng - dlng}
    right_bottom = {"lat": lat - dlat, "lng": lng + dlng}
    return left_top, right_top, left_bottom, right_bottom

if __name__ == '__main__':
    domains = getDomains()
    if domains:
        for domain in domains:
            get_geoMysql(domain)