from os import environ
from os import path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ROOT = path.dirname(path.dirname(__file__))
DJANGO_ROOT = path.join(SITE_ROOT, '../parts/django')

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': path.join(SITE_ROOT, '../data/hortee.db'),
        'USER': '',
        'PASSWORD': '', 
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = False
USE_L10N = False
SHORT_DATE_FORMAT = 'Y-m-d'

SITE_ID = 1

MEDIA_ROOT = path.join(SITE_ROOT, 'hortee/static')
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '7z!33sc_z216mcp1*r)&$3rm3sr!x61fa84tg$1n68(cqe=e9w'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'main.UserProfile'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'main.middleware.UserAgentMiddleware',
)

ROOT_URLCONF = 'hortee.urls'

TEMPLATE_DIRS = (
    path.join(SITE_ROOT, 'hortee/templates'),
    path.join(DJANGO_ROOT, 'django/contrib/admindocs/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'tracktor',
    'main',
    'south',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'main.context_processors.page',
    'main.context_processors.debug',
    'tracktor.context_processors.tracktor',    
)

SESSION_KEY_DEFAULT_PLOT = 'default_plot'

