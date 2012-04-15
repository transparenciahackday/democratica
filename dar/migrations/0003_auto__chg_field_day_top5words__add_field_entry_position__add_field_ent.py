# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Day.top5words'
        db.alter_column('dar_day', 'top5words', self.gf('django.db.models.fields.TextField')(null=True))

        # Adding field 'Entry.position'
        db.add_column('dar_entry', 'position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Entry.raw_text'
        db.add_column('dar_entry', 'raw_text', self.gf('django.db.models.fields.TextField')(default=0, max_length=100000), keep_default=False)

        # Adding field 'Entry.html'
        db.add_column('dar_entry', 'html', self.gf('django.db.models.fields.TextField')(default='', max_length=300000, blank=True), keep_default=False)

        # Adding field 'Entry.data'
        db.add_column('dar_entry', 'data', self.gf('django.db.models.fields.TextField')(default='{}', null=True), keep_default=False)

        # Changing field 'Entry.speaker'
        db.alter_column('dar_entry', 'speaker', self.gf('django.db.models.fields.CharField')(max_length=200))


    def backwards(self, orm):
        
        # Changing field 'Day.top5words'
        db.alter_column('dar_day', 'top5words', self.gf('django_extensions.db.fields.json.JSONField')(null=True))

        # Deleting field 'Entry.position'
        db.delete_column('dar_entry', 'position')

        # Deleting field 'Entry.raw_text'
        db.delete_column('dar_entry', 'raw_text')

        # Deleting field 'Entry.html'
        db.delete_column('dar_entry', 'html')

        # Deleting field 'Entry.data'
        db.delete_column('dar_entry', 'data')

        # Changing field 'Entry.speaker'
        db.alter_column('dar_entry', 'speaker', self.gf('django.db.models.fields.CharField')(max_length=100))


    models = {
        'dar.day': {
            'Meta': {'ordering': "['date']", 'object_name': 'Day'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'top5words': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True'})
        },
        'dar.entry': {
            'Meta': {'object_name': 'Entry'},
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True'}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dar.Day']"}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '300000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.MP']", 'null': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'raw_text': ('django.db.models.fields.TextField', [], {'max_length': '100000'}),
            'speaker': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'deputados.caucus': {
            'Meta': {'ordering': "['-session__number']", 'object_name': 'Caucus'},
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Constituency']"}),
            'date_begin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'has_activity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_registointeresses': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.MP']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Party']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Session']"})
        },
        'deputados.constituency': {
            'Meta': {'ordering': "['name']", 'object_name': 'Constituency'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'deputados.mp': {
            'Meta': {'ordering': "['shortname']", 'object_name': 'MP'},
            'current_caucus': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'current'", 'null': 'True', 'to': "orm['deputados.Caucus']"}),
            'current_party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Party']", 'null': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'favourite_word': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'news': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'photo': ('deputados.thumbs.ImageWithThumbsField', [], {'max_length': '100', 'null': 'True', 'name': "'photo'", 'sizes': '((18, 25), (60, 79))'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tweets': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True'})
        },
        'deputados.party': {
            'Meta': {'object_name': 'Party'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'has_mps': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tendency': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'deputados.session': {
            'Meta': {'object_name': 'Session'},
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['dar']
