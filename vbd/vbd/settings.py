# -*- coding=utf-8 -*-

"""
Django settings for vbd project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

HERE = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gokv-=uwxyrr!qlcqsr72xxj1)vw_ky=p3yl#fgp+2r%g*y^$i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if __file__.find('/Users/xieyanyang') >= 0 else False
#DEBUG = False

#这个是给后续的LOGGING模块使用的
#LOG_LEVEL = 'DEBUG' if __file__.find('/Users/xieyanyang') >= 0 else 'INFO'
LOG_LEVEL='INFO'

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [ '*', '127.0.0.1']

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'captcha',
    'authen',
    'dashboard',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'vbd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'common-templates')),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # 自定义session处理方法. 可以将期望的数据加入到context中.
                'authen.context_processor.fillup_user_into_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'vbd.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
     'default': {
          'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
          'NAME': 'vbd',  # Or path to database file if using sqlite3.
          'USER': 'root',  # Not used with sqlite3.
          'PASSWORD': '111111',  # Not used with sqlite3.
          'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
          #'HOST': '54.169.51.181',
          'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
     }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(HERE,'static').replace('\\','/')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
   os.path.join(HERE,'common-static/').replace('\\','/'),
)

LOG_FILE = BASE_DIR + "/vbd.log"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'request_handler': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,  
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
       'logfile': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console':{
            'level':LOG_LEVEL,
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'console_db':{
            'level':'ERROR',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'ERROR',
            'propagate': True,
        },
        #注意: 这里要写你的模块的名称
        'dashboard': {
            'handlers': ['logfile', 'console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'authen': {
            'handlers': ['logfile', 'console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django.db': {
            # # django also has database level logging
            'handlers': ['console_db'],
            
            # if level is DEBUG, then sql will be showed into console
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake1',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
    'memcache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # 'LOCATION': 'unix:/home/billvsme/memcached.sock',
        'LOCATION': '127.0.0.1:11211',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
}

#注册用户敏感词过滤
ADMIN_RESERVED = ['admin', 'login', 'logout', ]
LAW_RESERVED = ['porn', 'sex', 'fuck', 'shit']
RESERVED = ADMIN_RESERVED + LAW_RESERVED

#email
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'yanyang.xie@gmail.com'
SERVER_EMAIL = 'yanyang.xie@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yanyang.xie@gmail.com'
EMAIL_HOST_PASSWORD = '****'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Add a scheduler job to get status
from apscheduler.scheduler import Scheduler
from dashboard.op_views import period_scrapy_component_status
sched = Scheduler()
sched.add_interval_job(period_scrapy_component_status, seconds=30)
sched.start()

#kubenetes hosts
kube_server_ssh_user='root'
kube_server_ssh_port = 22
kube_server_ssh_key_file = '/Users/xieyanyang/work/ttbj/ttbj-keypair.pem'
