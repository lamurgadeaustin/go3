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
import io
import logging
import os
import sys
from multiprocessing import set_start_method  # for task q
from urllib.parse import urlparse

import environ
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy

# import google.auth
# from google.cloud import secretmanager

env = environ.Env(DEBUG=bool, SENDGRID_SANDBOX_MODE_IN_DEBUG=bool, CAPTCHA_THRESHOLD=float,
                  CALFEED_DYNAMIC_CALFEED=bool, CACHE_USE_FILEBASED=bool, ALLOWED_HOSTS=list,
                  ROUTINE_TASK_KEY=int)
# reading .env file
environ.Env.read_env()

_testing = False
if len(sys.argv) > 1 and sys.argv[1] == "test":
    _testing = True
    logging.disable(logging.CRITICAL)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

if os.getenv("CI", None):
    # Create local settings if running with CI, for unit testing

    placeholder = (
        "SECRET_KEY=a\n"
        "GS_BUCKET_NAME=None\n"
        "DATABASE_URL=sqlite:////tmp/my-tmp-sqlite.db"
    )
    env.read_env(io.StringIO(placeholder))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default=["localhost", "127.0.0.1"])

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# [START cloudrun_django_csrf]
# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to Cloud Run. This code takes the URL and converts it to both these settings formats.
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    ALLOWED_HOSTS = ["*"]
# [END cloudrun_django_csrf]

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
# [START cloudrun_django_database_config]
# Use django-environ to parse the connection string
DATABASES = {"default": env.db()}

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5434

# [END cloudrun_django_database_config]

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
    ("de", gettext_lazy("German")),
    ("en-US", gettext_lazy("English (US)")),
    ("en-GB", gettext_lazy("English (UK)")),
    ("fr", gettext_lazy("French")),
    ("it", gettext_lazy("Italian")),
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

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
