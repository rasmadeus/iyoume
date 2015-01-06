# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Room.subname'
        db.delete_column(u'room_room', 'subname')

        # Deleting field 'Room.visitorsTitle'
        db.delete_column(u'room_room', 'visitorsTitle')

        # Deleting field 'Room.doorsTitle'
        db.delete_column(u'room_room', 'doorsTitle')

        # Deleting field 'Room.contentTitle'
        db.delete_column(u'room_room', 'contentTitle')

        # Adding field 'Room.description_meta'
        db.add_column(u'room_room', 'description_meta',
                      self.gf('django.db.models.fields.CharField')(default=u'\u041f\u043e\u043f\u0443\u0442\u0447\u0438\u043a, \u043f\u0430\u0441\u0441\u0430\u0436\u0438\u0440, \u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c, \u043f\u0435\u0440\u0435\u0432\u043e\u0437\u043a\u0438, iyoume', max_length=200),
                      keep_default=False)

        # Adding field 'Room.title'
        db.add_column(u'room_room', 'title',
                      self.gf('django.db.models.fields.CharField')(default=3, max_length=200),
                      keep_default=False)

        # Adding field 'Room.slogan'
        db.add_column(u'room_room', 'slogan',
                      self.gf('django.db.models.fields.CharField')(default=u'\u041f\u043e\u043f\u0443\u0442\u0447\u0438\u043a\u0438 \u0432\u0441\u0435\u0445 \u0441\u0442\u0440\u0430\u043d - \u043e\u0431\u044a\u0435\u0434\u0435\u043d\u044f\u0439\u0442\u0435\u0441\u044c!', max_length=300),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Room.subname'
        db.add_column(u'room_room', 'subname',
                      self.gf('django.db.models.fields.CharField')(default=u'\u041d\u0435\u0442 \u0442\u0430\u043a\u043e\u0439 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Room.visitorsTitle'
        db.add_column(u'room_room', 'visitorsTitle',
                      self.gf('django.db.models.fields.CharField')(default=u'\u041f\u043e\u0441\u0435\u0442\u0438\u0442\u0435\u043b\u0438 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Room.doorsTitle'
        db.add_column(u'room_room', 'doorsTitle',
                      self.gf('django.db.models.fields.CharField')(default=u'\u0414\u0432\u0435\u0440\u0438 \u0438\u0437 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Room.contentTitle'
        db.add_column(u'room_room', 'contentTitle',
                      self.gf('django.db.models.fields.CharField')(default=u'\u041e\u0431\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', max_length=20, blank=True),
                      keep_default=False)

        # Deleting field 'Room.description_meta'
        db.delete_column(u'room_room', 'description_meta')

        # Deleting field 'Room.title'
        db.delete_column(u'room_room', 'title')

        # Deleting field 'Room.slogan'
        db.delete_column(u'room_room', 'slogan')


    models = {
        u'room.room': {
            'Meta': {'object_name': 'Room'},
            '_content_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'description_meta': ('django.db.models.fields.CharField', [], {'default': "u'\\u041f\\u043e\\u043f\\u0443\\u0442\\u0447\\u0438\\u043a, \\u043f\\u0430\\u0441\\u0441\\u0430\\u0436\\u0438\\u0440, \\u0432\\u043e\\u0434\\u0438\\u0442\\u0435\\u043b\\u044c, \\u043f\\u0435\\u0440\\u0435\\u0432\\u043e\\u0437\\u043a\\u0438, iyoume'", 'max_length': '200'}),
            'doors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['room.Room']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slogan': ('django.db.models.fields.CharField', [], {'default': "u'\\u041f\\u043e\\u043f\\u0443\\u0442\\u0447\\u0438\\u043a\\u0438 \\u0432\\u0441\\u0435\\u0445 \\u0441\\u0442\\u0440\\u0430\\u043d - \\u043e\\u0431\\u044a\\u0435\\u0434\\u0435\\u043d\\u044f\\u0439\\u0442\\u0435\\u0441\\u044c!'", 'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['room']