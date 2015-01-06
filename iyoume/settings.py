"""
Django settings for iyoume project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wy%(s05xja*3&$+in-gi(!4%b8f(%vy+(9$nq*z9rx#pjxn+04'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'localflavor',
    'django_markdown',
    'markitup',
    'iyoume.room',
    'south',
    'iyoume.iyoume_user',
    'iyoume.waybill',
    'django_cron',
)

MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
CRON_CLASSES = [
    'iyoume.waybill.cron.OldWaybillsKiller',
]
TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'iyoume.urls'

WSGI_APPLICATION = 'iyoume.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'iyoumeru_db', 
    'USER': 'iyoumeru_root', 
    'PASSWORD': 'Nztenb3mNztenb3m', 
    'HOST': '127.0.0.1',
    'PORT': '',
    'OPTIONS': {
            'init_command': 'SET foreign_key_checks = 0;',
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = '/home/iyoumeru/domains/iyoume.ru/public_html/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/iyoumeru/domains/iyoume.ru/public_html/static/'
STATIC_URL = '/static/'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


TEMPLATE_DIRS = (
    'home/iyoumeru/projects/iyoume/templates/',
    'home/iyoumeru/projects/iyoume/templates/others/',
    'home/iyoumeru/projects/iyoume/templates/registration/',
    'home/iyoumeru/projects/iyoume/templates/rooms/',
    'home/iyoumeru/projects/iyoume/templates/blocks/',
    'home/iyoumeru/projects/iyoume/templates/waybill/',
    'home/iyoumeru/projects/iyoume/templates/form/',
)


