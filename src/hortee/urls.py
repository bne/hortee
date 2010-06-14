from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from hortee.main import views

urlpatterns = patterns('',
    url(r'^$', views.default, name='hortee-default'),
)

urlpatterns += patterns('',                       
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)
	
# Debug pattern for serving media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
    )
