# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Session'
        db.delete_table('deputados_session')

        # Adding model 'Legislature'
        db.create_table('deputados_legislature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_start', self.gf('django.db.models.fields.DateField')(null=True)),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('deputados', ['Legislature'])

        # Adding model 'Activity'
        db.create_table('deputados_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'])),
            ('mandate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Mandate'])),
            ('type1', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('type2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=3000)),
            ('legislature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Legislature'])),
            ('external_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('deputados', ['Activity'])

        # Deleting field 'Mandate.session'
        db.delete_column('deputados_mandate', 'session_id')

        # Adding field 'Mandate.legislature'
        db.add_column('deputados_mandate', 'legislature', self.gf('django.db.models.fields.related.ForeignKey')(default=12, to=orm['deputados.Legislature']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Session'
        db.create_table('deputados_session', (
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_start', self.gf('django.db.models.fields.DateField')(null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('deputados', ['Session'])

        # Deleting model 'Legislature'
        db.delete_table('deputados_legislature')

        # Deleting model 'Activity'
        db.delete_table('deputados_activity')

        # User chose to not deal with backwards NULL issues for 'Mandate.session'
        raise RuntimeError("Cannot reverse this migration. 'Mandate.session' and its values cannot be restored.")

        # Deleting field 'Mandate.legislature'
        db.delete_column('deputados_mandate', 'legislature_id')


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
        'deputados.government': {
            'Meta': {'object_name': 'Government'},
            'date_ended': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        'deputados.governmentpost': {
            'Meta': {'object_name': 'GovernmentPost'},
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
            'commissions': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'current_mandate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'current'", 'null': 'True', 'to': "orm['deputados.Mandate']"}),
            'current_party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Party']", 'null': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'favourite_word': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'jobs': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
            'literacy': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'blank': 'True'}),
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
