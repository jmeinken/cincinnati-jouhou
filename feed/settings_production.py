from settings_global import *

# LOGIN_URL = '/analyst_tools/login'
FORCE_SCRIPT_NAME = '/feed/'

STATIC_URL = '/feed/static/'

# CSRF_COOKIE_NAME = 'analyst_tools_csrftoken'
# SESSION_COOKIE_NAME = 'analyst_tools_sessionid'

# DEBUG = False
# ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cincinnati',
        'USER': 'cincinnati_site',
        'PASSWORD': 'c2pRgyWh4ato',
        'HOST': '127.0.0.1',
    }
}