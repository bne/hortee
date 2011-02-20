from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from hortee.main.views import DefaultView
from hortee.tracktor import api as tracktor_api

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', DefaultView.as_view(), name='main-default'),
)

urlpatterns += patterns('',
    (r'^api/', include(tracktor_api.url_patterns())),
)

urlpatterns += patterns('',
    (r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {
        'template': 'robots.txt', 'mimetype': 'text/plain' }),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {
        'url': '/static/img/favicon.ico' }),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout_then_login', name='main-logout'),
)

urlpatterns += patterns('',
    (r'^admin/(.*)', admin.site.urls),
)

# development ststic files
urlpatterns += staticfiles_urlpatterns()

