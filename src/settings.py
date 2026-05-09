from pathlib import Path
from decouple import config  
import os 
from django.contrib.messages import constants as messages
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SITE_DOMAIN = config('SITE_DOMAIN')
SITE_NAME = config('SITE_NAME')

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast = bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_cleanup.apps.CleanupConfig',
    'crispy_forms',
    'crispy_bootstrap4',
    'accounts',
    'store',
    'cart',
    'orders',
    'coupons',
    'apis',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

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

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR ,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER') ,
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# Password validation
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
from django.utils.translation import gettext_lazy
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en' , gettext_lazy('English')),
    ('ar' , gettext_lazy('Arabic')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR , 'locale')
]

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR , 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR , 'SRC/static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR , 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP Configration Email :
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT',cast = int) 
EMAIL_USE_TLS = config('EMAIL_USE_TLS' ,cast=bool) 

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

AUTH_USER_MODEL = "accounts.Account"

# Message Tags
MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

# Cart Session ID
CART_SESSION_ID = 'cart'

# Cache
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

CACHES = {
    'default': {
        'BACKEND':'django_redis.cache.RedisCache',
        'LOCATION':f'redis://{REDIS_HOST}:6379/1',
        'OPTIONS':{
            'CLIENT_CLASS':'django_redis.client.DefaultClient'
        },
        'TIMEOUT': 300 ,
    }
}

# Celery
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'


# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'BLACKLIST_AFTER_ROTATION': True ,
}



