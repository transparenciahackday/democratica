# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MP'
        db.create_table('deputados_mp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='X', max_length=1)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('photo', self.gf('deputados.thumbs.ImageWithThumbsField')(max_length=100, null=True, name='photo', sizes=((18, 25),))),
            ('favourite_word', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('deputados', ['MP'])

        # Adding model 'Party'
        db.create_table('deputados_party', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tendency', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('info', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('has_mps', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('deputados', ['Party'])

        # Adding model 'FactType'
        db.create_table('deputados_facttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('deputados', ['FactType'])

        # Adding model 'Fact'
        db.create_table('deputados_fact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'])),
            ('fact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.FactType'])),
            ('value', self.gf('django.db.models.fields.TextField')(max_length=2000)),
        ))
        db.send_create_signal('deputados', ['Fact'])

        # Adding model 'Government'
        db.create_table('deputados_government', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('date_started', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_ended', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('deputados', ['Government'])

        # Adding model 'GovernmentPost'
        db.create_table('deputados_governmentpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('government', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Government'])),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'], null=True)),
            ('date_started', self.gf('django.db.models.fields.DateField')()),
            ('date_ended', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('deputados', ['GovernmentPost'])

        # Adding model 'Session'
        db.create_table('deputados_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_start', self.gf('django.db.models.fields.DateField')(null=True)),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('deputados', ['Session'])

        # Adding model 'Constituency'
        db.create_table('deputados_constituency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('article', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('deputados', ['Constituency'])

        # Adding model 'Caucus'
        db.create_table('deputados_caucus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Session'])),
            ('date_begin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('constituency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Constituency'])),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Party'])),
            ('has_activity', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_registointeresses', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('deputados', ['Caucus'])

        # Adding model 'Activity'
        db.create_table('deputados_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'])),
            ('caucus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Caucus'])),
            ('type1', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('type2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('session', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=3000)),
            ('external_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('deputados', ['Activity'])

        # Adding model 'LinkSet'
        db.create_table('deputados_linkset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mp', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deputados.MP'], unique=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('wikipedia_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebook_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('twitter_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('blog_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('website_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('linkedin_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('twitica_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('radio_url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('tv_url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('deputados', ['LinkSet'])


    def backwards(self, orm):
        
        # Deleting model 'MP'
        db.delete_table('deputados_mp')

        # Deleting model 'Party'
        db.delete_table('deputados_party')

        # Deleting model 'FactType'
        db.delete_table('deputados_facttype')

        # Deleting model 'Fact'
        db.delete_table('deputados_fact')

        # Deleting model 'Government'
        db.delete_table('deputados_government')

        # Deleting model 'GovernmentPost'
        db.delete_table('deputados_governmentpost')

        # Deleting model 'Session'
        db.delete_table('deputados_session')

        # Deleting model 'Constituency'
        db.delete_table('deputados_constituency')

        # Deleting model 'Caucus'
        db.delete_table('deputados_caucus')

        # Deleting model 'Activity'
        db.delete_table('deputados_activity')

        # Deleting model 'LinkSet'
        db.delete_table('deputados_linkset')


    models = {
        'deputados.activity': {
            'Meta': {'object_name': 'Activity'},
            'caucus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.Caucus']"}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'external_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deputados.MP']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'session': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'type1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
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

    complete_apps = ['deputados']
