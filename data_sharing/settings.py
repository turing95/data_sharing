"""
Django settings for data_sharing project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _
from config import *
import os
import sentry_sdk

if DEBUG is False:
    sentry_sdk.init(
        dsn="https://3b6bbd0cdf536a6d594ea98600b72a0d@o4506563455221760.ingest.sentry.io/4506563455418368",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.microsoft',
    'custom_google_provider',
    'custom_microsoft_provider',
    'web_app',
    'djstripe',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'web_app.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'web_app.middleware.timezone.TimezoneMiddleware'
]
if DEBUG is True:
    MIDDLEWARE.append('web_app.middleware.QueryLoggingMiddleware')
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

ROOT_URLCONF = 'data_sharing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'web_app.context_processors.custom_context',
            ],
        },
    },
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",
                       "django.contrib.staticfiles.finders.AppDirectoriesFinder")

STATICFILES_DIRS = [
    BASE_DIR / "static"

]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LOGIN_URL = '/accounts/login/'

ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend'
]
WSGI_APPLICATION = 'data_sharing.wsgi.application'
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}

AUTH_USER_MODEL = 'web_app.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGES = (
    ('en-us', _("English")),
    ('it', _("Italian")),
)
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
SOCIALACCOUNT_STORE_TOKENS = True
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'
LOGIN_REDIRECT_URL = 'spaces'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_ADAPTER = 'web_app.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'web_app.adapters.SocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email'

        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    },

    "microsoft": {
        "APPS": [
            {
                "client_id": AZURE_CLIENT_ID,
                "secret": AZURE_CLIENT_SECRET
            },

        ],
        # modify scopes requested during login
        'SCOPE': [
            "User.Read",  # access to user's account information
            "offline_access"  # provide a refresh_token when the user logs in
        ],
        'AUTH_PARAMS': {
            "prompt": "select_account",
        }
    },
    'custom_google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.install',
            'https://www.googleapis.com/auth/drive.readonly'

        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
            "prompt": "consent",
        }
    },
    "custom_microsoft": {
        "APPS": [
            {
                "client_id": AZURE_CLIENT_ID,
                "secret": AZURE_CLIENT_SECRET
            },

        ],
        # modify scopes requested during login
        'SCOPE': [
            "User.Read",  # access to user's account information
            "Files.Read.All",
            "Files.ReadWrite.All",  # access to user's files
            "Sites.Read.All",  # access to user's sites
            "Sites.ReadWrite.All",  # access to user's sites
            "offline_access"  # provide a refresh_token when the user logs in
        ],
        'AUTH_PARAMS': {
            "prompt": "select_account",
        }
    }
}

# TODO: this is against security best practices, according to allauth docs
SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
RESEND_SMTP_PORT = 587
RESEND_SMTP_USERNAME = 'resend'
RESEND_SMTP_HOST = 'smtp.resend.com'
EMAIL_USE_TLS = True
NO_REPLY_EMAIL = 'noreply@kezyy.com'
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

CONTACT_EMAIL = "service@kezyy.com"
