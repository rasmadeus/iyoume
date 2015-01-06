# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GeoPoint'
        db.create_table(u'waybill_geopoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'waybill', ['GeoPoint'])

        # Adding model 'Waybill'
        db.create_table(u'waybill_waybill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('driver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('from_point', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_point', to=orm['waybill.GeoPoint'])),
            ('to_point', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_point', to=orm['waybill.GeoPoint'])),
            ('place_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=4)),
            ('luggage_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'waybill', ['Waybill'])

        # Adding model 'Passenger'
        db.create_table(u'waybill_passenger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', to=orm['waybill.Waybill'])),
            ('place_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('luggage_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'waybill', ['Passenger'])


    def backwards(self, orm):
        # Deleting model 'GeoPoint'
        db.delete_table(u'waybill_geopoint')

        # Deleting model 'Waybill'
        db.delete_table(u'waybill_waybill')

        # Deleting model 'Passenger'
        db.delete_table(u'waybill_passenger')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'waybill.geopoint': {
            'Meta': {'object_name': 'GeoPoint'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'waybill.passenger': {
            'Meta': {'object_name': 'Passenger'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'luggage_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': u"orm['waybill.Waybill']"}),
            'place_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'waybill.waybill': {
            'Meta': {'object_name': 'Waybill'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'from_point': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_point'", 'to': u"orm['waybill.GeoPoint']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'luggage_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'place_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'to_point': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_point'", 'to': u"orm['waybill.GeoPoint']"})
        }
    }

    complete_apps = ['waybill']