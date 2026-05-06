import os
from pathlib import Path

# 1. TEMEL DİZİN AYARI
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. GÜVENLİK AYARLARI
SECRET_KEY = 'django-insecure-test-key'
DEBUG = True

# BURAYI GÜNCELLEDİM:
ALLOWED_HOSTS = ['ascend.hasanbugragursoy.com', '.railway.app', 'localhost', '127.0.0.1']

# 3. UYGULAMALAR
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stories',
]

# 4. ARA KATMANLAR
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Statik dosyalar için bunu ekledim
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ascent_web.urls'

# 5. ŞABLONLAR
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'stories' / 'templates'],
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

# 6. VERİTABANI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. STATİK DOSYA AYARLARI
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'stories' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 8. MEDYA DOSYALARI
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Railway/Vercel Güvenlik Ayarı
CSRF_TRUSTED_ORIGINS = ['https://ascend.hasanbugragursoy.com']