"""
Django settings for post_inn project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from django.conf import settings
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'  # Путь к изображениям из браузера
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Путь к медиа на сервере

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['*']

TEST = 'ad'

LOGIN_URL = '/app/auth/login/'
LOGOUT_URL = '/app/auth/logout/'


# Откуда брать переопределенного пользователя
AUTH_USER_MODEL = 'accounts.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'notes',
    'fordev',
    'rest_framework',
    'drf_yasg',
    'django_summernote',
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

ROOT_URLCONF = 'post_inn.urls'

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
                'notes.context_processors.counter_obj',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.messages.context_processors.messages'
]

WSGI_APPLICATION = 'post_inn.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

IS_DEV_SERVER = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/static/'

if IS_DEV_SERVER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env(f'DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
        }
    }

    # STATICFILES_DIRS = (
    #     os.path.join(BASE_DIR, 'note_inn', 'static'),  # Путь к статике на сервере
    # )

    STATIC_ROOT = os.path.join(BASE_DIR, "static")

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env(f'DB_NAME_LOCALHOST'),
            'USER': env('DB_USER_LOCALHOST'),
            'PASSWORD': env('DB_PASSWORD_LOCALHOST'),
            'HOST': env('DB_HOST_LOCALHOST'),
            'PORT': env('DB_PORT_LOCALHOST'),
        }
    }

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'note_inn', 'static'),  # Путь к статике на сервере
    )

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'MAX_PAGE_SIZE': 3,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SWAGGER_SETTINGS = {
   # default inspector classes, see advanced documentation
   'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
   'DEFAULT_FIELD_INSPECTORS': [
      'drf_yasg.inspectors.CamelCaseJSONFilter',
      'drf_yasg.inspectors.ReferencingSerializerInspector',
      'drf_yasg.inspectors.RelatedFieldInspector',
      'drf_yasg.inspectors.ChoiceFieldInspector',
      'drf_yasg.inspectors.FileFieldInspector',
      'drf_yasg.inspectors.DictFieldInspector',
      'drf_yasg.inspectors.SimpleFieldInspector',
      'drf_yasg.inspectors.StringDefaultFieldInspector',
   ],
   'DEFAULT_FILTER_INSPECTORS': [
      'drf_yasg.inspectors.CoreAPICompatInspector',
   ],
   'DEFAULT_PAGINATOR_INSPECTORS': [
      'drf_yasg.inspectors.DjangoRestResponsePagination',
      'drf_yasg.inspectors.CoreAPICompatInspector',
   ],

   # default api Info if none is otherwise given; should be an import string to an openapi.Info object
   'DEFAULT_INFO': None,
   # default API url if none is otherwise given
   'DEFAULT_API_URL': None,

   'USE_SESSION_AUTH': True,  # add Django Login and Django Logout buttons, CSRF token to swagger UI page
   'LOGIN_URL': getattr(settings, 'LOGIN_URL', None),  # URL for the login button
   'LOGOUT_URL': getattr(settings, 'LOGOUT_URL', None),  # URL for the logout button
}
