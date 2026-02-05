import os
import environ
import dj_database_url

env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

# False if not in os.environ because of casting above
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')
TEMPLATE_DEBUG = env.bool('TEMPLATE_DEBUG')
DEBUG404 = env.bool('DEBUG404')


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
]

CUSTOM_APPS = [
    'index',
    'nominations',
    'events',
    'awards',
    'accounts',
    'votes',
    'blog'
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'crispy_bootstrap4'
]

INSTALLED_APPS += CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hag.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hag.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'hag_db',
#         'USER': 'hag_admin',
#         'PASSWORD': 'hag_pass',
#         # 'HOST': 'hag-awards.c8exrtbnydnr.us-east-2.rds.amazonaws.com',
#         # 'HOST': 'hag-awards.ccokylx2aobv.us-east-2.rds.amazonaws.com',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'hag.db'),
    # }
}

DATABASES['default'] = dj_database_url.parse(env.str('DATABASE_URL'))

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 1

# SECURITY SETTINGS
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('SECURE_CONTENT_TYPE_NOSNIFF')
SECURE_BROWSER_XSS_FILTER = env.bool('SECURE_BROWSER_XSS_FILTER')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS')
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD')
SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS')

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')
USE_X_FORWARDED_HOST = env.bool('USE_X_FORWARDED_HOST')

CORS_ALLOW_CREDENTIALS = env.bool('CORS_ALLOW_CREDENTIALS')
CORS_ORIGIN_ALLOW_ALL = env.bool('CORS_ORIGIN_ALLOW_ALL')
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST')

APPEND_SLASH = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'statics')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
# MEDIA_URL = '/media/'  
ADMIN_MEDIA_PREFIX = '/static/admin/'  

    

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATICFILES_ROOT = [os.path.join(BASE_DIR, 'static'),]


DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y/%m/%d')
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/adminlogin'
SESSION_COOKIE_AGE = 24 * 60 * 60
REGISTER_EXPIRED_DATE = 7 * 24 * 60 * 60

APPEND_SLASH = True

# send mail settings
NEW_USER_EMAIL_SUBJECT = "Humanitarian Awards Global"
ADMINS = [('Godfred Owusu', 'iamgodfredowusu@gmail.com'), ('Osanim Systems', 'osanimsystems@gmail.com'), ('HAG', 'humanitarianawardsgh@gmail.com')]
MANAGERS = ADMINS
EMAIL_ADMIN = '(Humanitarian Awards Global) <mailer@humanitarianawardsglobal.com>'
EMAIL_SUBJECT_PREFIX = "[www.humanitarianawardsglobal.com]"
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'HAG'
EMAIL_HOST_PASSWORD = env('MANDRILL_API_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# REDIS related settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'


# CELERY
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# CELERYBEAT_SCHEDULE = {
#     'check_infobip_sms_delivery_report': {
#         'task': 'infobip_sms_delivery_report',
#         'schedule': crontab(minute='*/1'),
#         # 'args': (16, 16)
#     },
    
# }
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_ENABLE_UTC=True
CELERY_TIMEZONE = TIME_ZONE

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'WARNING',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',

#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'WARNING',
#             'propagate': True,
#         },
#     },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
# }


# try:
#     from .local_settings import *
# except ImportError:
#     pass
