from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('hortee.main.views',
    url(r'^$', 'default', name='main-default'),
    url(r'^login/$', 'login', name='main-login'),
)

urlpatterns += patterns('hortee.tracktor.views',
    url(r'^map/$', 'plot_map', name='tracktor-map'),
    url(r'^plots/$', 'plot_list', name='tracktor-plots'),
    url(r'^plots/add/$', 'plot_add', name='tracktor-plot-add'),
    url(r'^plots/(?P<id>\d+)/edit/$', 'plot_edit', name='tracktor-plot-edit'),    
    url(r'^plots/(?P<id>\d+)/delete/$', 'plot_delete', name='tracktor-plot-delete'),    
        
    url(r'^actors/$', 'actor_list', name='tracktor-actors'),
    url(r'^actors/add/$', 'actor_add', name='tracktor-actor-add'),
    url(r'^actors/(?P<id>\d+)/delete/$', 'actor_delete', name='tracktor-actor-delete'),
    
    url(r'^actors/(?P<actor_id>\d+)/$', 'event_list', name='tracktor-events'),
    url(r'^actors/(?P<actor_id>\d+)/event/add/$', 'event_add', name='tracktor-event-add'),  
    url(r'^event/(?P<id>\d+)/edit/$', 'event_edit', name='tracktor-event-edit'),
    url(r'^event/(?P<id>\d+)/delete/$', 'event_delete', name='tracktor-event-delete'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout_then_login', name='main-logout'),
)

urlpatterns += patterns('',
    (r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {
        'template': 'robots.txt', 'mimetype': 'text/plain' }),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {
        'url': '/static/img/favicon.ico' }),
)

urlpatterns += patterns('',
    (r'^admin/(.*)', admin.site.root),
)
	
# Debug pattern for serving media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT }),
    )
