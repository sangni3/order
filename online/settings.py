"""
Django settings for online project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e+lcw0=syvz4fc1)mcl2#x8b4x984#o95xe7r6y4ux@uv5=q0%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition


INSTALLED_APPS = [
    "simpleui",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'rest_framework',
    'corsheaders',
]
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')     #设置静态文件路径为主目录下的media文件夹
MEDIA_URL = '/media/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
SIMPLEUI_LOGO = '/static/shop.png'
SIMPLEUI_HOME_INFO = False
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

CORS_ALLOW_CREDENTIALS = True # 允许携带cookie
#直接允许所有主机跨域
CORS_ORIGIN_ALLOW_ALL = True #解决跨域

CORS_ORIGIN_WHITELIST = ('http://localhost:8080',)
# CORS_ALLOW_HEADERS = ('content-disposition', 'accept-encoding',
#                       'content-type', 'accept', 'origin', 'authorization')
# CORS_ALLOW_METHODS = (
#     'DELETE','GET','OPTIONS','PATCH','POST','PUT','VIEW')

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

ROOT_URLCONF = 'online.urls'

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

WSGI_APPLICATION = 'online.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'online',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'POST': '3306',
        'OPTIONS': {
                    'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"',
                    'charset': 'utf8mb4'
                }
    }
}

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

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MDEIA_ROOT = os.path.join(BASE_DIR, r'static\mdeia')

# 支付宝
ALIPAY_APP_ID = '2021000122610332'
APP_PRIVATE_KEY_STRING = open('{}/shop/app_private_key.txt'.format(BASE_DIR)).read()
ALIPAY_PUBLIC_KEY_STRING = open('{}/shop/alipay_public_key.txt'.format(BASE_DIR)).read()
ALIPAY_SIGN_TYPE = 'RSA2'
ALIPAY_SUBJECT = '点餐'