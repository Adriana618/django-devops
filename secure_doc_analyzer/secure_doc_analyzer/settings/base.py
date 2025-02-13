"""
Django settings for secure_doc_analyzer project.

Generated by 'django-admin startproject' using Django 3.2.25.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
root = environ.Path(__file__) - 3
env = environ.Env(
    DEBUG=(bool, False),
    DATABASE_NAME=(str, "db_name"),
    DATABASE_USER=(str, "db_user"),
    DATABASE_PASSWORD=(str, "db_password"),
    DATABASE_HOST=(str, "db"),
    DATABASE_PORT=(str, "5432"),
    AWS_ACCESS_KEY_ID=(str, "aws_access_key"),
    AWS_SECRET_ACCESS_KEY=(str, "aws_secret_key"),
    AWS_S3_BUCKET=(str, "aws_bucket"),
    AWS_REGION=(str, "us-east-1")
)

env_file = os.path.join(root(), ".env")
if os.path.exists(env_file):
    env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="wññaoiewpawoierañsfjñodafnrñainñoew")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "documents",
    "accounts",
    "auditlog",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "10/minute", "user": "50/minute"},
}


ROOT_URLCONF = "secure_doc_analyzer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "secure_doc_analyzer.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_VALIDATION_MODULE = "django.contrib.auth.password_validation."

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": AUTH_VALIDATION_MODULE + "UserAttributeSimilarityValidator"},
    {"NAME": AUTH_VALIDATION_MODULE + "MinimumLengthValidator"},
    {"NAME": AUTH_VALIDATION_MODULE + "CommonPasswordValidator"},
    {"NAME": AUTH_VALIDATION_MODULE + "NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = env("AWS_S3_BUCKET")
AWS_REGION = env("AWS_REGION")

CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL", default="redis://127.0.0.1:6379/0"
)
CELERY_RESULT_BACKEND = env(
    "CELERY_RESULT_BACKEND", default="redis://127.0.0.1:6379/0"
)
