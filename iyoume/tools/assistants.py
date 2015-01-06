# -*- coding: utf-8 -*-

__author__="rasmadeus"
__date__ ="$Jun 17, 2014 10:42:52 PM$"


GEO_EPSILON = 0.1


import math


def is_equals(first, second, tolerance=GEO_EPSILON):
    return math.fabs(first - second) <= tolerance


def send_sms(phone_number, text):
    import requests
    url = u'http://sms.ru/sms/send?api_id=965ae1bd-eefe-fb34-c5b4-13c45d1081e6&to=7{phone_number}&text={text}'
    return requests.get(url.format(phone_number=phone_number, text=text))


def only_known_user(f):
    def is_known(request):
        if request.user.is_authenticated():
            return f(request)
        else:
            from django import shortcuts
            return shortcuts.redirect('/')
    return is_known


def is_phone_number(phone_number):
    import re
    return len(phone_number) == 10 and len(re.findall('\d{10}', phone_number)) == 1


def set_style(field, placeholder):	
	field.widget.attrs['class'] = 'form-control'
	field.widget.attrs['placeholder'] = placeholder	