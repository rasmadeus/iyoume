# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'room_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'\u041d\u0435\u0438\u0437\u0432\u0435\u0441\u0442\u043d\u0430\u044f \u043a\u043e\u043c\u043d\u0430\u0442\u0430', max_length=50)),
            ('subname', self.gf('django.db.models.fields.CharField')(default=u'\u041d\u0435\u0442 \u0442\u0430\u043a\u043e\u0439 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', max_length=100, blank=True)),
            ('contentTitle', self.gf('django.db.models.fields.CharField')(default=u'\u041e\u0431\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', max_length=20, blank=True)),
            ('doorsTitle', self.gf('django.db.models.fields.CharField')(default=u'\u0414\u0432\u0435\u0440\u0438 \u0438\u0437 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', max_length=20, blank=True)),
            ('visitorsTitle', self.gf('django.db.models.fields.CharField')(default=u'\u041f\u043e\u0441\u0435\u0442\u0438\u0442\u0435\u043b\u0438 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', max_length=20, blank=True)),
            ('content', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('_content_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'room', ['Room'])

        # Adding M2M table for field doors on 'Room'
        m2m_table_name = db.shorten_name(u'room_room_doors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_room', models.ForeignKey(orm[u'room.room'], null=False)),
            ('to_room', models.ForeignKey(orm[u'room.room'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_room_id', 'to_room_id'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'room_room')

        # Removing M2M table for field doors on 'Room'
        db.delete_table(db.shorten_name(u'room_room_doors'))


    models = {
        u'room.room': {
            'Meta': {'object_name': 'Room'},
            '_content_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'contentTitle': ('django.db.models.fields.CharField', [], {'default': "u'\\u041e\\u0431\\u0441\\u0442\\u0430\\u043d\\u043e\\u0432\\u043a\\u0430 \\u043a\\u043e\\u043c\\u043d\\u0430\\u0442\\u044b'", 'max_length': '20', 'blank': 'True'}),
            'doors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['room.Room']", 'symmetrical': 'False', 'blank': 'True'}),
            'doorsTitle': ('django.db.models.fields.CharField', [], {'default': "u'\\u0414\\u0432\\u0435\\u0440\\u0438 \\u0438\\u0437 \\u043a\\u043e\\u043c\\u043d\\u0430\\u0442\\u044b'", 'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'\\u041d\\u0435\\u0438\\u0437\\u0432\\u0435\\u0441\\u0442\\u043d\\u0430\\u044f \\u043a\\u043e\\u043c\\u043d\\u0430\\u0442\\u0430'", 'max_length': '50'}),
            'subname': ('django.db.models.fields.CharField', [], {'default': "u'\\u041d\\u0435\\u0442 \\u0442\\u0430\\u043a\\u043e\\u0439 \\u043a\\u043e\\u043c\\u043d\\u0430\\u0442\\u044b'", 'max_length': '100', 'blank': 'True'}),
            'visitorsTitle': ('django.db.models.fields.CharField', [], {'default': "u'\\u041f\\u043e\\u0441\\u0435\\u0442\\u0438\\u0442\\u0435\\u043b\\u0438 \\u043a\\u043e\\u043c\\u043d\\u0430\\u0442\\u044b'", 'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['room']