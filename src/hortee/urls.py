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
    
    url(r'^list/$', 'list_actors', name='tracktor-actors'),
    url(r'^actor/add/$', 'add_actor', name='tracktor-actor-add'),
    url(r'^actor/delete/(?P<id>\d+)/$', 'delete_actor', name='tracktor-actor-delete'),
    url(r'^list/(?P<id>\d+)/$', 'list_events', name='tracktor-events'),
    url(r'^list/(?P<id>\d+)/event/add/$', 'add_event', name='tracktor-event-add'),  
    url(r'^event/edit/(?P<id>\d+)/$', 'edit_event', name='tracktor-event-edit'),
    url(r'^event/delete/(?P<id>\d+)/$', 'delete_event', name='tracktor-event-delete'),
    url(r'^plots/$', 'plots', name='tracktor-plots'),
    url(r'^plots/delete/$', 'delete_plot', name='tracktor-delete_plot'),
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
