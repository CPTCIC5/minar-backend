from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework'
    "corsheaders",
]

WSGI_APPLICATION = 'backends.wsgi.application'

SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL= 'users.User'
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    ]

CSRF_COOKIE_SECURE= False

ROOT_URLCONF = 'backends.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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



INTERNAL_IPS = [
    "127.0.0.1"
]
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if os.getenv("DB_NAME") and not DEBUG:  # use postgres if env variables are configured
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ["DB_USER"],
            "PASSWORD": os.environ["DB_PASSWORD"],
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ["DB_PORT"],  # 5432 by default
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL= "users.User"

EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_DEBUG = True


AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'kleenestarbucket'
AWS_S3_SIGNATURE_NAME = '53v4',
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            #'rest_framework.authentication.BasicAuthentication',  # enables simple command line authentication
            'rest_framework.authentication.SessionAuthentication'
        )
    }

CORS_ALLOW_HEADERS = [
    'X-CSRFToken',  # Add any other headers you need to allow
    'Content-Type',  # Include Content-Type header
]
CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    'https://kleenestar.vercel.app',
    'https://kleenestar-frontend.vercel.app',
    'https://dfssdfdf.hopto.org',
    'http://13.48.26.7',
    "https://193a-2405-201-3023-68e8-99ba-718-4d2c-e83b.ngrok-free.app",
    'http://localhost:3000',
    "http://localhost:8000",
    'http://localhost:5173',
    'https://polite-awake-bobcat.ngrok-free.app',
    'https://kleenestar-frontend.vercel.app',
    'https://kleenestar-frontend.onrender.com'
]

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
CSRF_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True