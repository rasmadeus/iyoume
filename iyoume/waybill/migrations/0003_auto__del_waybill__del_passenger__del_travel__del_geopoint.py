# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Waybill'
        db.delete_table(u'waybill_waybill')

        # Deleting model 'Passenger'
        db.delete_table(u'waybill_passenger')

        # Deleting model 'Travel'
        db.delete_table(u'waybill_travel')

        # Removing M2M table for field passangers on 'Travel'
        db.delete_table(db.shorten_name(u'waybill_travel_passangers'))

        # Deleting model 'GeoPoint'
        db.delete_table(u'waybill_geopoint')


    def backwards(self, orm):
        # Adding model 'Waybill'
        db.create_table(u'waybill_waybill', (
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('place_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=4)),
            ('to_point', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_point', to=orm['waybill.GeoPoint'])),
            ('luggage_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('from_point', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_point', to=orm['waybill.GeoPoint'])),
            ('driver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'waybill', ['Waybill'])

        # Adding model 'Passenger'
        db.create_table(u'waybill_passenger', (
            ('place_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('luggage_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', to=orm['waybill.Waybill'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'waybill', ['Passenger'])

        # Adding model 'Travel'
        db.create_table(u'waybill_travel', (
            ('from_point', self.gf('django.db.models.fields.related.ForeignKey')(related_name='travel_from_point', to=orm['waybill.GeoPoint'])),
            ('to_point', self.gf('django.db.models.fields.related.ForeignKey')(related_name='travel_to_point', to=orm['waybill.GeoPoint'])),
            ('meeting_point', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'waybill', ['Travel'])

        # Adding M2M table for field passangers on 'Travel'
        m2m_table_name = db.shorten_name(u'waybill_travel_passangers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('travel', models.ForeignKey(orm[u'waybill.travel'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['travel_id', 'user_id'])

        # Adding model 'GeoPoint'
        db.create_table(u'waybill_geopoint', (
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'waybill', ['GeoPoint'])


    models = {
        
    }

    complete_apps = ['waybill']