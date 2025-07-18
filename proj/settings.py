"""
Django settings for proj project.

Generated by 'django-admin startproject' using Django 5.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)
DB_NAME = os.environ.get("DB_NAME")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv("SECRET_KEY", "insecure-default-key-for-learning")
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "restaurant",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "proj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "proj.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# 개발시
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.environ.get("DB_NAME"),
#         "USER": os.environ.get("DB_USER"),
#         "PASSWORD": os.environ.get("DB_PASSWORD"),
#         "HOST": os.environ.get("DB_HOST"),
#         "PORT": os.environ.get("DB_PORT"),
#         "OPTIONS": {
#             "charset": "utf8mb4",  # 문자셋을 utf8mb4 로 지정
#             "init_command": "SET NAMES utf8mb4",  # 커넥션 시 SET NAMES utf8mb4 실행
#         },
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("RDS_DB_NAME", os.getenv("DB_NAME", "default_db")),
        "USER": os.getenv("RDS_USERNAME", os.getenv("DB_USER", "default_user")),
        "PASSWORD": os.getenv(
            "RDS_PASSWORD", os.getenv("DB_PASSWORD", "default_password")
        ),
        "HOST": os.getenv("RDS_HOSTNAME", os.getenv("DB_HOST", "localhost")),
        "PORT": os.getenv("RDS_PORT", os.getenv("DB_PORT", "3306")),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET NAMES utf8mb4",
        },
    }
}

if os.environ.get("TEST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# Use Amazon S3 for storage for uploaded media files if not debugging
# S3_BUCKET = os.getenv("AWS_STORAGE_BUCKET_NAME")
# if os.environ.get("S3_BUCKET"):
#     STORAGES = {
#         "default": {
#             "BACKEND": "storages.backends.s3.S3Storage",
#             "OPTIONS": {
#                 "bucket_name": os.environ.get("S3_BUCKET"),
#                 "region_name": os.environ.get("S3_REGION", "ap-northeast-2"),
#                 "custom_domain": os.environ.get("S3_CUSTOM_DOMAIN"),
#                 "location": "media",
#                 "default_acl": "public-read",
#                 "querystring_auth": False,
#             },
#         },
#         "staticfiles": {
#             "BACKEND": "storages.backends.s3.S3Storage",
#             "OPTIONS": {
#                 "bucket_name": os.environ.get("S3_BUCKET"),
#                 "region_name": os.environ.get("S3_REGION", "ap-northeast-2"),
#                 "custom_domain": os.environ.get("S3_CUSTOM_DOMAIN"),
#                 "location": "static",
#                 "default_acl": "public-read",
#                 "querystring_auth": False,
#             },
#         },
#     }


AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
if AWS_STORAGE_BUCKET_NAME:
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-northeast-2")
    # Domain for S3 (e.g., mybucket.s3.ap-northeast-2.amazonaws.com)
    AWS_S3_CUSTOM_DOMAIN = os.getenv(
        "AWS_S3_CUSTOM_DOMAIN",
        f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com",
    )

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    # Local fallback
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
