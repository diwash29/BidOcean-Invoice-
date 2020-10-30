"""
Django settings for invoices project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!ft!^sypv_uv&&h5yxpaodxv#r#78ot_7*aiknnqu1b##=rojh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'user_invoice.apps.UserInvoiceConfig',
    'account_management.apps.AccountManagementConfig',
    'leave.apps.LeaveConfig',
    'letter.apps.LetterConfig',
    'manage_user.apps.ManageUserConfig',
    'expenses.apps.ExpensesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django_crontab',
  
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

ROOT_URLCONF = 'invoices.urls'

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

WSGI_APPLICATION = 'invoices.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bido_invoice',
        'USER': 'postgres',
        'PASSWORD':'Sensor@1234',
        'HOST': '1.7.151.12',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

#STATIC_URL = '/static/'
STATIC_ROOT = '/projects/invoice/site/public/static'
STATIC_URL = '/static/'
STATICFILES_DIR = [
    os.path.join(BASE_DIR, 'static'),
]


MEDIA_URL  = '/media/'
#MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



CRISPY_TEMPLATE_PACK='bootstrap4'
LOGIN_REDIRECT_URL='user_invoice-home'
LOGIN_URL='login'
AUTH_USER_MODEL = 'manage_user.Userdetail'


CRONJOBS = [    
    # ('*/5 * * * *', 'user_invoice.cron.update_invoice'),
    ('*/28 * * * *', 'user_invoice.cron.update_invoice','>> /home/bds/NewDjango/biocean-invoice/user_invoice/file.log'),
 ]