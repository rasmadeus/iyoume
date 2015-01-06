from django.conf.urls import patterns, url
from iyoume.iyoume_user import views as iyoume_user

urlpatterns = patterns('',
    url(r'^$', iyoume_user.registration_room),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^add_new_user/', iyoume_user.registration_room),
    url(r'^check_new_user/', iyoume_user.check_user),
    url(r'^restore_password/', iyoume_user.restore_password),
    url(r'^check_restore_user/', iyoume_user.try_restore_user),
    url(r'^login/', iyoume_user.login),
)
