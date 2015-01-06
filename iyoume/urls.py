from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from room import views as room_views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('^markdown/', include( 'django_markdown.urls')),
    url(r'^room/', include('iyoume.room.urls')),
    url(r'^user/', include('iyoume.iyoume_user.urls')),
    url(r'^waybill/', include('iyoume.waybill.urls')),
    url(r'^$', room_views.build_main_room),
)
