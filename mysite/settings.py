#users:
#tomek Tomek12345!
#marcin Marcin12345!
#andrzej Jarmark12345!
# app name : portfolio



from pathlib import Path
import os



LOGIN_URL = 'register:login'  # The URL where users are redirected if they're not logged in
LOGIN_REDIRECT_URL = '/register/'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=p=21v*-_ax0st9k=z=6=pb&7)f41pegok55ycqnjk#n%m07yf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#added 0.0.0.0. for linux
ALLOWED_HOSTS = ['localhost', '127.0.0.1','0.0.0.0']

X_FRAME_OPTIONS = 'SAMEORIGIN'


#RUN MONGODB SERVER
#C:\Program Files\MongoDB\Server\7.0\bin
#λ mongod --dbpath "C:\Users\cryse\OneDrive\Pulpit\Investment-Portfolio\stock_data\data\db
# second terminal ->mongosh --host localhost --port 27017
# third terminal node search eninge: node database_search.js

#db['2024-01-07'].find()
#test> show dbs
#admin   80.00 KiB
#config  72.00 KiB
#local   72.00 KiB
#use admin
#show collections
#db['2024-01-07'].find()
# Application definition
#app portfolio
#HN06CGD9HU1ROZ91
#set JSON to api data once a day and store data in DB

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portfolio',
    'register',
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

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'portfolio', 'templates'),
                 os.path.join(BASE_DIR, 'register', 'templates'),
                 ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'ENGINE': 'djongo',
#         'NAME': 'stock_data',
#     }
# }
# Use SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use Djongo for production with MongoDB
if 'djongo' in DATABASES['default']['ENGINE']:
    DATABASES['default']['ENGINE'] = 'djongo'
    DATABASES['default']['NAME'] = 'stock_data'
    # Add other Djongo-related settings...


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#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