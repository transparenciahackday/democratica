# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Fact'
        db.delete_table('deputados_fact')

        # Deleting model 'Caucus'
        db.delete_table('deputados_caucus')

        # Deleting model 'FactType'
        db.delete_table('deputados_facttype')

        # Deleting model 'Activity'
        db.delete_table('deputados_activity')

        # Adding model 'Mandate'
        db.create_table('deputados_mandate', (
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
        db.send_create_signal('deputados', ['Mandate'])

        # Deleting field 'MP.current_caucus'
        db.delete_column('deputados_mp', 'current_caucus_id')

        # Adding field 'MP.commissions'
        db.add_column('deputados_mp', 'commissions', self.gf('django.db.models.fields.TextField')(default='', max_length=5000, blank=True), keep_default=False)

        # Adding field 'MP.literacy'
        db.add_column('deputados_mp', 'literacy', self.gf('django.db.models.fields.TextField')(default='', max_length=5000, blank=True), keep_default=False)

        # Adding field 'MP.jobs'
        db.add_column('deputados_mp', 'jobs', self.gf('django.db.models.fields.TextField')(default='', max_length=5000, blank=True), keep_default=False)

        # Adding field 'MP.current_mandate'
        db.add_column('deputados_mp', 'current_mandate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='current', null=True, to=orm['deputados.Mandate']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Fact'
        db.create_table('deputados_fact', (
            ('fact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.FactType'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'])),
        ))
        db.send_create_signal('deputados', ['Fact'])

        # Adding model 'Caucus'
        db.create_table('deputados_caucus', (
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Session'])),
            ('has_registointeresses', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_begin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'])),
            ('has_activity', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Party'])),
            ('constituency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Constituency'])),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('deputados', ['Caucus'])

        # Adding model 'FactType'
        db.create_table('deputados_facttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('deputados', ['FactType'])

        # Adding model 'Activity'
        db.create_table('deputados_activity', (
            ('content', self.gf('django.db.models.fields.TextField')(max_length=3000)),
            ('mp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.MP'])),
            ('session', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('type1', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('type2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('external_id', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caucus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deputados.Caucus'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('deputados', ['Activity'])

        # Deleting model 'Mandate'
        db.delete_table('deputados_mandate')

        # Adding field 'MP.current_caucus'
        db.add_column('deputados_mp', 'current_caucus', self.gf('django.db.models.fields.related.ForeignKey')(related_name='current', null=True, to=orm['deputados.Caucus']), keep_default=False)

        # Deleting field 'MP.commissions'
        db.delete_column('deputados_mp', 'commissions')

        # Deleting field 'MP.literacy'
        db.delete_column('deputados_mp', 'literacy')

        # Deleting field 'MP.jobs'
        db.delete_column('deputados_mp', 'jobs')

        # Deleting field 'MP.current_mandate'
        db.delete_column('deputados_mp', 'current_mandate_id')


    models = {
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
            'Meta': {'ordering': "['-session__number']", 'object_name': 'Mandate'},
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
