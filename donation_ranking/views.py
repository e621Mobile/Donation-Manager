import json
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import render
from django.template import RequestContext, loader
from django.utils import timezone
from donation_ranking import controller


def index(request):
	if(not controller.is_logged_in(request)):
		return HttpResponseRedirect(reverse("donation_ranking.views.login"))
	
	template = loader.get_template('html/donation_ranking/index.html')
	
	context = RequestContext(request, {
		'ongs': controller.get_ongs(request),
	})
	
	return HttpResponse(template.render(context))

def login(request):
	if(request.method=="POST"):
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
		
		if(controller.login(request, username, password)):
			return HttpResponseRedirect(reverse("donation_ranking.views.index"))
		else:
			template = loader.get_template('html/donation_ranking/login.html')
			
			context = RequestContext(request, {
													'user': request.user,
													'error': True,
													'non_subscribe_account': False,
										})
			
			return HttpResponse(template.render(context))
	else:
		template = loader.get_template('html/donation_ranking/login.html')
		
		context = RequestContext(request, {
												'user': request.user,
												'error': False,
												'non_subscribe_account': False,
									})
		
		return HttpResponse(template.render(context))

def ong(request,ong_name):
	ong = controller.get_ong(request, ong_name)
	
	if(ong == None):
		return HttpResponseRedirect(reverse("donation_ranking.views.index"))
	else:
		template = loader.get_template('html/donation_ranking/ong.html')
		
		context = RequestContext(request, {
			'ong': ong,
			'donators': controller.get_donators(request, ong_name, "value"),
		})
		
		return HttpResponse(template.render(context))

def ong_json(request, ong_name):
	order = request.GET.get('order',"")
	
	donators = controller.get_donators(request, ong_name, order)
	ret = []
	
	if(donators != None):
		for donator in donators:
			ret.append({
				"name": donator.show_name,
				"url": donator.show_url,
				"ammount": float(donator.total)/100,
				"first_donation": str(donator.first_donation),
				"last_donation": str(donator.last_donation),
				"recent_total": (float(donator.recent_donations_total)/100) if donator.recent_donations_total else 0.0,
			})
	
	return HttpResponse(json.dumps(ret))

def ong_highlight_json(request, ong_name):
	donators = controller.get_donators_highlight(request, ong_name)
	ret = []
	
	if(donators != None):
		for donator in donators:
			ret.append({
				"name": donator.show_name,
				"url": donator.show_url,
				"ammount": float(donator.total)/100,
			})
	
	return HttpResponse(json.dumps(ret))

def add_donation(request, ong_name):
	time = request.POST.get("time","").strip()
	if(not time):
		time = timezone.now()
	
	controller.add_donation(request, ong_name, request.POST.get("email", ""), request.POST.get("ammount", 0), time);
	return HttpResponseRedirect(reverse("donation_ranking.views.ong", kwargs={"ong_name":ong_name}))

def donator_update(request,hash_id):
	if(request.method == "GET"):
		donator = controller.get_donator_info(request, hash_id)
		
		if(donator == None):
			return HttpResponseRedirect(reverse("donation_ranking.views.index"))
		else:
			template = loader.get_template('html/donation_ranking/donator_update.html')
			
			context = RequestContext(request, {
				'donator': donator,
			})
			
			return HttpResponse(template.render(context))
	else:
		controller.update_donator_info(request, hash_id, request.POST.get("name", "Anonymous"), request.POST.get("url", ""))
		return HttpResponseRedirect(reverse("donation_ranking.views.donator_update", kwargs={"hash_id":hash_id}))
