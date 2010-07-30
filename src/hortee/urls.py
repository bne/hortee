from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('hortee.main.views',
    url(r'^$', 'default', name='hortee-default'),
)

urlpatterns += patterns('hortee.tracktor.views',
    url(r'^list/$', 'list_actors', name='tracktor-list'),    
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
