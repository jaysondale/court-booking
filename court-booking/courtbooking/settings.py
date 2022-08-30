"""
Django settings for courtbooking project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from datetime import time
import os
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

ALLOWED_HOSTS = ['klm-court-booking.herokuapp.com', '127.0.0.1', 'courts.kennisislakemarina.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'booking',
    'user_manage.apps.UserManageConfig',
    'crispy_forms'
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

ROOT_URLCONF = 'courtbooking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'courtbooking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'root')


# Set User Model
AUTH_USER_MODEL = 'user_manage.User'

# System Parameters
FIRST_BOOKING = time(hour=7)
LAST_BOOKING = time(hour=20)
NUM_BOOKING_DAYS = 7

# Login redirect
LOGIN_REDIRECT_URL='calendar'

# Backend for email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if 'PASSWORD' in os.environ.keys():
    # Staging or production database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['DBNAME'],
            'USER': os.environ['DBUSER'],
            'PASSWORD': os.environ['PASSWORD'],
            'HOST': os.environ['DBHOST'],
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache_table',
        }
    }
else:
    # development database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# Deployment Settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

AWS_S3_REGION_NAME = 'ca-central-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = "virtual"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_EMAIL')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'

STATIC_URL = AWS_URL + 'static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = AWS_URL + 'media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

ADMIN_MEDIA_PREFIX = AWS_URL + 'admin/'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

LOGOUT_REDIRECT_URL = 'login'

django_heroku.settings(locals(), staticfiles=False)

# User session expiry after 10 minutes
SESSION_COOKIE_AGE = 10 * 60