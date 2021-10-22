from .common import *

if NON_PROD:
    try:
        from .local import *
    except:
        print('Running Prod Settings')
else:
    # Enter your Production Settings here
    import dj_database_url
    INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS
    MIDDLEWARE.insert(1,  'whitenoise.middleware.WhiteNoiseMiddleware')
    DEBUG = False
    ALLOWED_HOSTS = ['t20-wc-2021.herokuapp.com']
    db_from_env = dj_database_url.config(conn_max_age=600)
    DATABASES['default'].update(db_from_env)
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
