"""
Django settings for Pubg_WebApp project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z-%_f7o3omh513p++l=!5w)!-tp10*-$_7ccpb$f06uz_u20cr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

config = {
    'mobile.FCM_API_KEY': os.environ.get('DJ_FCM_KEY', 'KEY'),
    'celery.broker_host': os.environ.get('CELERY_BROKER_HOST', 'rabbit'),

    'sms.backend': os.environ.get('DJ_SMS_BACKEND', ''),
    'sms.username': os.environ.get('DJ_SMS_USERNAME', ''),
    'sms.password': os.environ.get('DJ_SMS_PASSWORD', ''),
    'sms.sender_name': os.environ.get('DJ_SMS_SENDER_NAME', ''),
}
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #3rd party apps
    'rest_framework',
    'rest_framework.renderers',
    'rest_framework.authtoken',
    'accounts',
    'psycopg2',
    'rabbit',
    'html5lib',
    'asgiref',


]
SWAGGER_SETTINGS = {

    'VALIDATOR_URL': 'http://localhost:8100',

}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Pubg_WebApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Pubg_WebApp.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
# sms-sender
SEND_SMS_BACKEND = f"sms_sender.backends.{config['sms.backend']}"
SMS_LOGIN = config['sms.username']
SMS_PASSWORD = config['sms.password']
SMS_SENDER_NAME = config['sms.sender_name']

CELERY_BROKER_URL = 'amqp://guest:guest@{}//'.format(config['celery.broker_host'])
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

FCM_API_KEY = config['mobile.FCM_API_KEY']
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pubgbeta',

        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432'

        # 'USER': 'newuser',
        # 'PASSWORD': 'liderkgz',
        # 'HOST': 'localhost',
        # 'PORT': 5432

    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
