from django.conf.urls import patterns, url
from iyoume.room import views as room_views

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', room_views.RoomView.as_view(template_name = 'room.html')),
)


