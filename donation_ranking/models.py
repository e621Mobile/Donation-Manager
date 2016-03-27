from django.db import models
from django.utils import timezone
import random
import string

class DonationUser(models.Model):
	user = models.OneToOneField('RSS.User')
	
	def __unicode__(self):
		return self.user.__unicode__()

class ONG(models.Model):
	donation_user = models.ForeignKey('DonationUser', null=False, blank=False)
	name = models.CharField(max_length=32)
	
	def __unicode__(self):
		return self.name

class DonatorQuerySet(models.query.QuerySet):
	def extra_recent_donations_total(self,timedelta):
		print (timezone.now()+timedelta).strftime('%Y-%m-%d %H:%M:%S.%f:%z')
		
		return self.extra(select = {'recent_donations_total':"""
			SELECT SUM(ammount)
			FROM donation_ranking_donation
			WHERE
				donator_id = donation_ranking_donator.id
				AND
				donation_ranking_donation.time > '%s'
		"""%((timezone.now()+timedelta).strftime('%Y-%m-%d %H:%M:%S.%f:%z'))})

class DonatorManager(models.Manager):
	def get_queryset(self):
		return DonatorQuerySet(self.model, using=self._db)
	
	def extra_recent_donations_total(self,timedelta):
		return self.get_queryset().extra_recent_donations_total(timedelta);

class Donator(models.Model):
	ong = models.ForeignKey('ONG', null=False, blank=False)
	email = models.EmailField(blank=False, null=False)
	show_name = models.CharField(max_length=32, default="Anonymous");
	show_url = models.URLField(blank=True, default="");
	hash_id = models.CharField(max_length=32, unique=True, default="")
	highlight = models.DateTimeField(null=False, blank=False)
	
	objects = DonatorManager()
	
	def save(self, *args, **kwargs):
		while(len(self.hash_id)!=32):
			h = "".join([random.choice(string.letters + string.digits) for i in range(32)]);
			if(not Donator.objects.filter(hash_id=h).exists()):
					self.hash_id = h
					break
		super(Donator,self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.email

class Donation(models.Model):
	donator = models.ForeignKey('Donator', null=False, blank=False)
	ammount = models.IntegerField(default=0, null=False, blank=False);
	time = models.DateTimeField(null=False, blank=False)
	
	def __unicode__(self):
		return "%d from %s" % (self.ammount, self.donator.__unicode__())
