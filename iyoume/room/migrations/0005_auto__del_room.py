# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'room_room')

        # Removing M2M table for field doors on 'Room'
        db.delete_table(db.shorten_name(u'room_room_doors'))


    def backwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'room_room', (
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('slogan', self.gf('django.db.models.fields.CharField')(default=u'\u041f\u043e\u043f\u0443\u0442\u0447\u0438\u043a\u0438 \u0432\u0441\u0435\u0445 \u0441\u0442\u0440\u0430\u043d - \u043e\u0431\u044a\u0435\u0434\u0435\u043d\u044f\u0439\u0442\u0435\u0441\u044c!', max_length=300)),
            ('description_meta', self.gf('django.db.models.fields.CharField')(default=u'\u041f\u043e\u043f\u0443\u0442\u0447\u0438\u043a, \u043f\u0430\u0441\u0441\u0430\u0436\u0438\u0440, \u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c, \u043f\u0435\u0440\u0435\u0432\u043e\u0437\u043a\u0438, iyoume', max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
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


    models = {
        
    }

    complete_apps = ['room']