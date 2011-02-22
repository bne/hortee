from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from hortee.tracktor import api

admin.autodiscover()

urlpatterns = patterns('hortee.main.views',
    url(r'^$', 'default', name='main-default'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout_then_login', name='main-logout'),
)

urlpatterns += patterns('',
    ('', include(api.api.urls)),
)

urlpatterns += patterns('hortee.tracktor.views',
    url(r'^list/$', 'actors', name='tracktor-list'),
)

urlpatterns += patterns('',
    (r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {
        'template': 'robots.txt', 'mimetype': 'text/plain' }),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {
        'url': '/static/img/favicon.ico' }),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

# development ststic files
urlpatterns += staticfiles_urlpatterns()

