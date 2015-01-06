# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'room_room', (
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=250, primary_key=True)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'room', ['Room'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'room_room')


    models = {
        u'room.room': {
            'Meta': {'object_name': 'Room'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250', 'primary_key': 'True'})
        }
    }

    complete_apps = ['room']