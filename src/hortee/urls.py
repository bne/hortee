from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('hortee.main.views',
    url(r'^$', 'default'),
)

urlpatterns += patterns('hortee.tracktor.views',
    url(r'^list/$', '_list', name="tracktor-list"),  
    url(r'^map/$', '_map', name="tracktor-map"),      
    url(r'^actor/add/$', 'add_actor'),
    url(r'^actor/delete/$', 'delete_actor'),    
    url(r'^list/(?P<id>\d+)/$', 'list_events'),
    url(r'^event/add/$', 'add_event'),  
    url(r'^event/delete/$', 'delete_event'),    
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {
        'template_name': 'user/login.html'}, 'auth-login'),
    url(r'^logout/$', 'logout_then_login', name='auth-logout'),
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
