# -*- coding: utf-8 -*-
import urllib2
from django.utils.http import urlquote_plus
import json


def GOOGLE_GEOCODE_URL():
    return 'http://maps.googleapis.com/maps/api/geocode/json?language=ru&sensor=false&address={address}'


class NoAddress(Exception):    
    def __str__(self):
        return u'No address'


def geo_info_about(address):
    url = GOOGLE_GEOCODE_URL().format(address=urlquote_plus(address))
    request = urllib2.Request(url)
    answer =  urllib2.urlopen(request).read()
    return json.loads(answer.decode('utf-8'))


def geo_coords(answer):
    if answer['status'] != 'OK':
        raise NoAddress()
    location = answer['results'][0]['geometry']['location']
    return [location['lng'], location['lat']]


def get_coords(address):
    return geo_coords(geo_info_about(address))




