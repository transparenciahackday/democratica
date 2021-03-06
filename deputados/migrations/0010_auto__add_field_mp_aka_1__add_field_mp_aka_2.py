# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'MP.aka_1'
        db.add_column('deputados_mp', 'aka_1', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'MP.aka_2'
        db.add_column('deputados_mp', 'aka_2', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'MP.aka_1'
        db.delete_column('deputados_mp', 'aka_1')

        # Deleting field 'MP.aka_2'
        db.delete_column('deputados_mp', 'aka_2')


    models = {
        'deputados.activity': {
            'Meta': {'object_name': 'Activity'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'external_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Legislature']"}),
            'mandate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Mandate']"}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.MP']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'deputados.constituency': {
            'Meta': {'ordering': "['name']", 'object_name': 'Constituency'},
            'article': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'deputados.fact': {
            'Meta': {'object_name': 'Fact'},
            'fact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.FactType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.MP']"}),
            'value': ('django.db.models.fields.TextField', [], {'max_length': '2000'})
        },
        'deputados.facttype': {
            'Meta': {'object_name': 'FactType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'deputados.government': {
            'Meta': {'ordering': "['number']", 'object_name': 'Government'},
            'date_ended': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        'deputados.governmentpost': {
            'Meta': {'ordering': "['government__number']", 'object_name': 'GovernmentPost'},
            'date_ended': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'government': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Government']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.MP']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'deputados.legislature': {
            'Meta': {'object_name': 'Legislature'},
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'deputados.linkset': {
            'Meta': {'object_name': 'LinkSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'blog_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkedin_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'mp': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['deputados.MP']", 'unique': 'True'}),
            'radio_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tv_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'twitica_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'wikipedia_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'deputados.mandate': {
            'Meta': {'ordering': "['-legislature__number']", 'object_name': 'Mandate'},
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Constituency']"}),
            'date_begin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'has_activity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_registointeresses': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Legislature']"}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.MP']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Party']"})
        },
        'deputados.mp': {
            'Meta': {'ordering': "['shortname']", 'object_name': 'MP'},
            'aka_1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'aka_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'awards': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'commissions': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'current_jobs': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'current_mandate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'current'", 'null': 'True', 'to': "orm['deputados.Mandate']"}),
            'current_party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Party']", 'null': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'favourite_word': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'jobs': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'news': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'photo': ('democratica.deputados.thumbs.ImageWithThumbsField', [], {'max_length': '100', 'null': 'True', 'name': "'photo'", 'sizes': '((18, 25), (60, 79))'}),
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
        }
    }

    complete_apps = ['deputados']
