# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Room.url_name'
        db.add_column(u'room_room', 'url_name',
                      self.gf('django.db.models.fields.CharField')(default=23, max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Room.url_name'
        db.delete_column(u'room_room', 'url_name')


    models = {
        u'room.room': {
            'Meta': {'object_name': 'Room'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'description_meta': ('django.db.models.fields.CharField', [], {'default': "u'\\u041f\\u043e\\u043f\\u0443\\u0442\\u0447\\u0438\\u043a, \\u043f\\u0430\\u0441\\u0441\\u0430\\u0436\\u0438\\u0440, \\u0432\\u043e\\u0434\\u0438\\u0442\\u0435\\u043b\\u044c, \\u043f\\u0435\\u0440\\u0435\\u0432\\u043e\\u0437\\u043a\\u0438, iyoume'", 'max_length': '200'}),
            'doors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['room.Room']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slogan': ('django.db.models.fields.CharField', [], {'default': "u'\\u041f\\u043e\\u043f\\u0443\\u0442\\u0447\\u0438\\u043a\\u0438 \\u0432\\u0441\\u0435\\u0445 \\u0441\\u0442\\u0440\\u0430\\u043d - \\u043e\\u0431\\u044a\\u0435\\u0434\\u0435\\u043d\\u044f\\u0439\\u0442\\u0435\\u0441\\u044c!'", 'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['room']