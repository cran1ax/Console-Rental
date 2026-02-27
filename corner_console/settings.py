"""
Django settings for Corner Console — simplified for local development.
Just run:  python manage.py runserver
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-corner-console-demo-key-not-for-production'

DEBUG = True

# Accept any host on the local machine
ALLOWED_HOSTS = ['*']


# ── Installed apps ──────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    # Our app
    'core',
]


# ── Middleware ───────────────────────────────────────────────────────────────
# CorsMiddleware MUST come before CommonMiddleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',          # ← CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ── CORS — allow everything so React dev-server just works ─────────────────

CORS_ALLOW_ALL_ORIGINS = True


# ── URL / WSGI ──────────────────────────────────────────────────────────────

ROOT_URLCONF = 'corner_console.urls'
WSGI_APPLICATION = 'corner_console.wsgi.application'


# ── Templates ───────────────────────────────────────────────────────────────

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


# ── Database — plain SQLite, zero setup ─────────────────────────────────────

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ── Password validation (kept light for a demo) ────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]


# ── Internationalization ────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ── Static files ────────────────────────────────────────────────────────────

STATIC_URL = 'static/'


# ── Primary key type ────────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ── Django REST Framework ───────────────────────────────────────────────────
# Session auth  → works in the browser / DRF browsable API
# Token auth    → works for the React frontend (simple, no JWT expiry headaches)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}
