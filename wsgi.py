import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'iyoume.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
