# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Day'
        db.create_table('dar_day', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('dar', ['Day'])

        # Adding model 'Entry'
        db.create_table('dar_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dar.Day'])),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'], null=True, blank=True)),
            ('speaker', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=10000)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('dar', ['Entry'])


    def backwards(self, orm):
        
        # Deleting model 'Day'
        db.delete_table('dar_day')

        # Deleting model 'Entry'
        db.delete_table('dar_entry')


    models = {
        'dar.day': {
            'Meta': {'object_name': 'Day'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'dar.entry': {
            'Meta': {'object_name': 'Entry'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dar.Day']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.MP']", 'null': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'speaker': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'deputados.mp': {
            'Meta': {'ordering': "['shortname']", 'object_name': 'MP'},
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'favourite_word': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'photo': ('deputados.thumbs.ImageWithThumbsField', [], {'max_length': '100', 'null': 'True', 'name': "'photo'", 'sizes': '((18, 25),)'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['dar']
