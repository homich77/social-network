import datetime

import environ

BASE_DIR = environ.Path(__file__) - 2

env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SECRET_KEY = '3vp(2uups!961b_vo)tsvxa90pasqsuqnee!c%x!@4aa=2&xq0'

DEBUG = env.bool('DJANGO_DEBUG', True)

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_auth',
]

LOCAL_APPS = [
    'users.apps.UsersConfig',
    'posts',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default='sqlite:///' + str(BASE_DIR.path('db.sqlite3'))
    )
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# Custom auth model

AUTH_USER_MODEL = 'users.User'


# Rest settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

REST_USE_JWT = True

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_ALLOW_REFRESH': False,
}


# Celery

BROKER_URL = env('BROKER_URL', default='redis://localhost:6379/1')

CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default=BROKER_URL)


# Emailhunter

EMAILHUNTER_KEY = env(
    'EMAILHUNTER_KEY', default='e07175754f4da96e046e86414dc958b630424fc4'
)

EMAILHUNTER_URL = env(
    'EMAILHUNTER_URL', default='https://api.hunter.io/v2/email-verifier'
)

EMAILHUNTER_VALID_PARAMS = {
    'mx_records': True,
    'smtp_server': True,
    'gibberish': False,
    'accept_all': False,
    'webmail': False,
    'regexp': True,
    'disposable': False,
    'smtp_check': True,
}


# Clearbit

CLEARBIT_KEY = env(
    'CLEARBIT_KEY', default='sk_eaac6e9a7fea0cda77c9819432dc7a0d'
)
