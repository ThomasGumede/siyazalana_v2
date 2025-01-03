import os
from pathlib import Path
from decouple import config, Csv
from siyazalana.logging import *
from siyazalana.celery_conf import *

BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'accounts.Account'
AUTHENTICATION_BACKENDS = ['accounts.utilities.backends.EmailBackend']
LOGIN_URL = 'accounts:login'
SECRET_KEY = config('SECRET', 'django-insecure-*1&e92eo3**p^ts02_nxi=w5u#zm9v&&6ps=q50-6o32v)zcq3')

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'siyazalana_home',
    'events',
    'campaigns',
    'coupons',
    'payments',
    'fontawesomefree',
    'tailwind',
    'theme',
    'tinymce',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'siyazalana.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'siyazalana_home.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'siyazalana.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases




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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMINS = [('admin@siyazalana.org'),( 'support@siyazalana.org'), ('gumedethomas12@gmail.com') ]
MANAGERS = [('admin@siyazalana.org'), ('support@siyazalana.org'), ('gumedethomas12@gmail.com') ]

# Files
TICKETS_PDF_DIR = os.path.join(BASE_DIR, 'media/tickets/pdf')
TICKETS_BARCODE_DIR = os.path.join(BASE_DIR, 'media/tickets/barcodes')
TICKETS_QRCODE_DIR = os.path.join(BASE_DIR, 'media/tickets/qrcodes')

if not os.path.exists(TICKETS_PDF_DIR):
    os.makedirs(TICKETS_PDF_DIR)

if not os.path.exists(TICKETS_BARCODE_DIR):
    os.makedirs(TICKETS_BARCODE_DIR)

if not os.path.exists(TICKETS_QRCODE_DIR):
    os.makedirs(TICKETS_QRCODE_DIR)


TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = "/usr/bin/npm"
INTERNAL_IPS = [
    "127.0.0.1", '0.0.0.0'
]
PASSWORD_RESET_TIMEOUT = 14400

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5MB

TINYMCE_DEFAULT_CONFIG = {
    'content_style': '* { margin: 0 !important; padding: 0 !important; }',
    'theme_advanced_fonts': 'DM Sans=dm-sans,Arial=arial,helvetica,sans-serif',
    'height': "400px",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    # 'selector': 'textarea',
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks fullscreen insertdatetime media table paste help",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | a11ycheck ltr rtl | showcomments addcomment",
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@siyazalana.org'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'noreply@siyazalana.org'


TEST_MODE = config('YOCO_TEST_MODE')
# YOCO
if DEBUG or TEST_MODE == 'yes':
    YOCO_WEBHOOK_KEY = config('YOCO_TEST_WEBHOOK_KEY')
    YOCO_API_KEY = config('YOCO_TEST_API_KEY')
    ALLOWED_HOSTS=['*']

else:
    YOCO_WEBHOOK_KEY = config('YOCO_LIVE_WEBHOOK_KEY')
    YOCO_API_KEY = config('YOCO_LIVE_API_KEY')

if DEBUG:
    ALLOWED_HOSTS = []
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    STATIC_URL = 'static/'
    STATICFILES_DIRS = [
        BASE_DIR / 'static'
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
    
else:
    ALLOWED_HOSTS = ['siyazalana.org', 'www.siyazalana.org']
    CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1', 'https://localhost', 'https://siyazalana.org', 'https://www.siyazalana.org']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    X_FRAME_OPTIONS = "SAMEORIGIN"
    
    YOCO_WEBHOOK_KEY = config('YOCO_LIVE_WEBHOOK_KEY')
    YOCO_API_KEY = config('YOCO_LIVE_API_KEY')
    

    # SSL SETTINGS
    
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': "siyazalanadb",
                'USER': config("DB_USER"),
                'PASSWORD': config("DB_PASSWORD"),
                'HOST': config("DB_HOST",'localhost'),
                'PORT': '',
            }
        }
    
    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    
    SILENCED_SYSTEM_CHECKS = ['security.W019']
    
