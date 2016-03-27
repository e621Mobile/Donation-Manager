import datetime
import math
import os
import shutil
import subprocess
import tempfile
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum, Min, Max
from django.template import Context, loader
from django.utils import timezone
from donation_ranking.models import *


def login(request,username,password):
	user = authenticate(email=username, password=password)
	
	if(user != None):
		try:
			user.donationuser
			auth_login(request,user)
			return True
		except:
			return False
	else:
		return False


def is_logged_in(request):
	if(request.user.is_authenticated()):
		try:
			request.user.donationuser
			return True
		except:
			return False
	else:
		return False

def get_ongs(request):
	return ONG.objects.all().filter(donation_user__user__email=request.user.email).values('name')

def get_ong(request,name):
	ret = ONG.objects.all().filter(donation_user__user__email=request.user.email, name=name)
	
	if(ret.exists()):
		return ret[0];
	
	return None

def get_donators(request, ong_name, order="value"):
	ong = ONG.objects.all().filter(name=ong_name)
	
	if(not ong.exists()):
		return None
	ong = ong[0];
	
	d = timezone.now()
	begin = datetime.datetime(year=d.year,month=d.month,day=1,tzinfo=d.tzinfo)
	
	donators = ong.donator_set.all().extra_recent_donations_total(begin-d).annotate(total = Sum("donation__ammount"), first_donation = Min("donation__time"), last_donation = Max("donation__time"))
	
	if(order == "newest"):
		donators = donators.order_by("-last_donation")
	elif(order == "oldest"):
		donators = donators.order_by("first_donation")
	else:
		donators = donators.order_by("-total")
	
	return donators

def get_donators_highlight(request, ong_name):
	ong = ONG.objects.all().filter(name=ong_name)
	
	if(not ong.exists()):
		return None
	ong = ong[0];
	
	donators = ong.donator_set.filter(highlight__gte=timezone.now).exclude(show_url="", show_name="Anonymous").annotate(total = Sum("donation__ammount")).order_by("?")
	
	return donators

def add_donation(request, ong_name, email, ammount, time):
	ong = get_ong(request,ong_name);
	
	if(ong == None):
		return
	
	donator = ong.donator_set.filter(email=email)
	
	if(donator.exists()):
		donator = donator[0]
	else:
		donator = Donator()
		donator.ong = ong
		donator.email = email
		donator.highlight = timezone.now()
		donator.save()
		
		c = Context({
						'donator': donator,
						'host': settings.DOMAIN_NAME
					})
		
		msg = EmailMultiAlternatives('Thank you for your donation!!',loader.get_template('mail/new_donator.txt').render(c),'me@'+settings.DOMAIN_NAME,[donator.email])
		msg.send()
	
	donator.highlight = max(timezone.now(),donator.highlight) + datetime.timedelta(days = max(1.0,math.floor(float(ammount)/100.0)))
	donator.save()
	
	donation = Donation()
	donation.donator = donator
	donation.ammount = ammount
	donation.time = time
	
	donation.save()

def get_donator_info(request,hash_id):
	donator = Donator.objects.all().filter(hash_id=hash_id);
	
	if(not donator.exists()):
		return None
	
	donator = donator[0]
	
	return donator;

def update_donator_info(request,hash_id,show_name,show_url):
	donator = Donator.objects.all().filter(hash_id=hash_id);
	
	if(not donator.exists()):
		return;
	
	donator = donator[0]
	
	donator.show_name = show_name[:32]
	donator.show_url = show_url
	donator.save()
