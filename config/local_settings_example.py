# Copy this file to local_settings.py and configure it

import os
import datetime

BASE_URL = "http://127.0.0.1:5000/"

DEBUG = True
PRODUCTION = False

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ["*"]

DATABASES_LOCAL = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "thrive_db",
        "USER": "user",
        "PASSWORD": "pass",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "TEST": {"NAME": "thrive_test_db"},
    },
}

EMAIL_HOST = "mail.arnatech.id"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "admin@arnatech.id"
EMAIL_HOST_PASSWORD = "hkZ01uVfAqQj95ip"


DATABASES = DATABASES_LOCAL


USE_S3 = False
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
AWS_ACCESS_KEY_ID = "FQYH52PFVIJ97EH7NX37"
AWS_SECRET_ACCESS_KEY = "NUHTUy3LwmwkWCGOZPGRPB6jo56QDgNfMpldeCIi"
AWS_STORAGE_BUCKET_NAME = "escrow-sg"
AWS_S3_ENDPOINT_URL = "https://%s.ap-south-1.linodeobjects.com" % (
    AWS_STORAGE_BUCKET_NAME
)
AWS_S3_SIGNATURE_VERSION = "s3v4"


# default JWT
JWT_SECRET_KEY = "barakadut"
JWT_ALGORITHMS = ["HS256"]

# JWT for auth token
AUTH_JWT_SECRET_KEY = "barakadut123"
AUTH_JWT_ALGORITHMS = ["HS256"]

# JWT for refresh token
REFRESH_JWT_SECRET_KEY = "barakadut890"
REFRESH_JWT_ALGORITHMS = ["HS256"]
