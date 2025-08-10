
from pathlib import Path
import environ
import os
import dj_database_url

# Environment variables setup
env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=jplr%ghen*v671grqi9g@1!ug10&4$v6^@$(gbp&hlnaptoiu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts for the application
ALLOWED_HOSTS = [
    "*"
]

CSRF_TRUSTED_ORIGINS = [
    "https://alx-project-nexus-1.onrender.com",
]

# Application definition
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom applications
    'users',          # User management and authentication
    'associations',   # Artisan associations
    'products',       # Product catalog
    'orders',         # Order processing
    'cart',          # Shopping cart functionality

    # Third-party packages
    'graphene_django',  # GraphQL API
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database configuration
# PostgreSQL database for production-grade performance
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': env('POSTGRES_DB'),
    #     'USER': env('POSTGRES_USER'),
    #     'PASSWORD': env('POSTGRES_PASSWORD'),
    #     'HOST': env('DB_HOST'),
    #     'PORT': env('DB_PORT'),
    # }
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# GraphQL configuration
GRAPHENE = {
    'SCHEMA': 'core.schema.schema',  # Main GraphQL schema
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',  # JWT authentication
    ],
}

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',  # JWT authentication
    'django.contrib.auth.backends.ModelBackend',  # Default Django auth
]

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / "staticfiles"

# # Whitenoise config
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'