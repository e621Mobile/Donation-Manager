# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DonationUser'
        db.create_table(u'donation_ranking_donationuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['RSS.User'], unique=True)),
        ))
        db.send_create_signal(u'donation_ranking', ['DonationUser'])

        # Adding model 'ONG'
        db.create_table(u'donation_ranking_ong', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('donation_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['donation_ranking.DonationUser'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'donation_ranking', ['ONG'])

        # Adding model 'Donator'
        db.create_table(u'donation_ranking_donator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ong', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['donation_ranking.ONG'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'donation_ranking', ['Donator'])

        # Adding model 'Donation'
        db.create_table(u'donation_ranking_donation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('donator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['donation_ranking.Donator'])),
            ('ammount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'donation_ranking', ['Donation'])


    def backwards(self, orm):
        # Deleting model 'DonationUser'
        db.delete_table(u'donation_ranking_donationuser')

        # Deleting model 'ONG'
        db.delete_table(u'donation_ranking_ong')

        # Deleting model 'Donator'
        db.delete_table(u'donation_ranking_donator')

        # Deleting model 'Donation'
        db.delete_table(u'donation_ranking_donation')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ong': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['donation_ranking.ONG']"})
        },
        u'donation_ranking.ong': {
            'Meta': {'object_name': 'ONG'},
            'donation_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['donation_ranking.DonationUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['donation_ranking']