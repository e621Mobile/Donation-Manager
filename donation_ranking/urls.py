from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'donation_ranking.views.index'),
	url(r'^login/$', 'donation_ranking.views.login'),
	url(r'^ong/(?P<ong_name>[^/]+)/$', 'donation_ranking.views.ong'),
	url(r'^ong/(?P<ong_name>[^/]+)/json/$', 'donation_ranking.views.ong_json'),
	url(r'^ong/(?P<ong_name>[^/]+)/json/highlight/$', 'donation_ranking.views.ong_highlight_json'),
	url(r'^ong/(?P<ong_name>[^/]+)/add/$', 'donation_ranking.views.add_donation'),
	
	url(r'^donator_update/(?P<hash_id>[^/]+)/$', 'donation_ranking.views.donator_update'),
)
