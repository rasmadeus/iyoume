from django.conf.urls import patterns, url
from iyoume.waybill import views as dr

urlpatterns = patterns('',
    url(r'^add/', dr.make_waybill),
    url(r'^del/', dr.remove_waybill),
    url(r'^find/', dr.search_waybill),
    url(r'^take/', dr.take_place),
    url(r'^trips/', dr.trips),
    url(r'^cancel_trip/', dr.cancel_trip),
    url(r'^passangers/', dr.passangers),
    url(r'^travel/', dr.travel),
)
