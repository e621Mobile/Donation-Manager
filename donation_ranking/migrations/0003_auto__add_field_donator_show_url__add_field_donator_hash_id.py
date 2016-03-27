# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Donator.show_url'
        db.add_column(u'donation_ranking_donator', 'show_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Donator.hash_id'
        db.add_column(u'donation_ranking_donator', 'hash_id',
                      self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=32),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Donator.show_url'
        db.delete_column(u'donation_ranking_donator', 'show_url')

        # Deleting field 'Donator.hash_id'
        db.delete_column(u'donation_ranking_donator', 'hash_id')


    models = {
        u'RSS.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'preffered_currency': ('django.db.models.fields.IntegerField', [], {})
        },
        u'donation_ranking.donation': {
            'Meta': {'object_name': 'Donation'},
            'ammount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'donator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['donation_ranking.Donator']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'donation_ranking.donationuser': {
            'Meta': {'object_name': 'DonationUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['RSS.User']", 'unique': 'True'})
        },
        u'donation_ranking.donator': {
            'Meta': {'object_name': 'Donator'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'hash_id': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ong': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['donation_ranking.ONG']"}),
            'show_name': ('django.db.models.fields.CharField', [], {'default': "'Anonymous'", 'max_length': '64'}),
            'show_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'donation_ranking.ong': {
            'Meta': {'object_name': 'ONG'},
            'donation_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['donation_ranking.DonationUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['donation_ranking']
