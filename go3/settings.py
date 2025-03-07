"""
    This file is part of Gig-o-Matic

    Gig-o-Matic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
Django settings for go3 project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import logging
import os
import sys
import environ
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages
from multiprocessing import set_start_method  # for task q

env = environ.Env(DEBUG=bool, SENDGRID_SANDBOX_MODE_IN_DEBUG=bool, CAPTCHA_THRESHOLD=float, 
                  CALFEED_DYNAMIC_CALFEED=bool, CACHE_USE_FILEBASED=bool, ALLOWED_HOSTS=list,
                  ROUTINE_TASK_KEY=int, SENTRY_DSN=str)
# reading .env file
environ.Env.read_env()

_testing = False
if len(sys.argv) > 1 and sys.argv[1] == "test":
    _testing = True
    logging.disable(logging.CRITICAL)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sentry_sdk
SENTRY_DSN = env("SENTRY_DSN", default=False)

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default=["localhost", "127.0.0.1"])

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = [
    "member.apps.MemberConfig",
    "band.apps.BandConfig",
    "motd.apps.MotdConfig",
    "gig.apps.GigConfig",
    "agenda.apps.AgendaConfig",
    "stats.apps.StatsConfig",
    "widget_tweaks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django.contrib.humanize",
    "django_q",
    "simple_history",
    "graphene_django",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "go3.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR + "/templates/",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

FORMAT_MODULE_PATH = ["go3.formats"]

WSGI_APPLICATION = "go3.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # The db() method is an alias for db_url().
    'default': env.db(default='sqlite:////tmp/my-tmp-sqlite.db')
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": os.path.join(BASE_DIR, "var", "go3.sqlite3"),
    # }
}

AUTH_USER_MODEL = "member.Member"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGES = [
    ("de", _("German")),
    ("en-US", _("English (US)")),
    ("en-GB", _("English (UK)")),
    ("fr", _("French")),
    ("it", _("Italian")),
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True


USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# for whitenoise
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login"

# Configure Django-q message broker
Q_CLUSTER = {
    "name": "DjangORM",
    "workers": 4,
    "timeout": 90,
    "retry": 120,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
    "sync": _testing,
    "catch_up": False,  # don't run scheduled tasks many times if we come back from an extended downtime
    "poll": 10, # turn down the poll rate - doesn't need to be 5 times per second!
}


# Local memory cache. To monitor djanqo-q, need to use filesystem or database
if env('CACHE_USE_FILEBASED', default=False):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# Email settings
DEFAULT_FROM_EMAIL_NAME = "Gig-o-Matic Superuser"
DEFAULT_FROM_EMAIL = "superuser@gig-o-matic.com"
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = env('SENDGRID_API_KEY', default='456')
SENDGRID_SANDBOX_MODE_IN_DEBUG = env('SENDGRID_SANDBOX_MODE_IN_DEBUG', default=True)
SENDGRID_TRACK_CLICKS_HTML = False

# Calfeed settings
DYNAMIC_CALFEED = env('CALFEED_DYNAMIC_CALFEED', default=False) # True to generate calfeed on demand; False for disk cache
DEFAULT_FILE_STORAGE = env('CALFEED_DEFAULT_FILE_STORAGE', default='django.core.files.storage.FileSystemStorage')
CALFEED_BASEDIR = env('CALFEED_CALFEED_BASEDIR', default='')

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Graphene GraphQL settings
GRAPHENE = {"SCHEMA": "go3.schema.schema"}

# if we're doing ETL from Go2, set this True
IN_ETL = False

# base URL
URL_BASE = env('URL_BASE',default='https://www.gig-o-matic.com')

# for calling routine tasks in go3.tasks
ROUTINE_TASK_KEY = env('ROUTINE_TASK_KEY',default=1)

# try:
#     from .settings_local import *
# except ImportError:
#     pass
