from pathlib import Path
from .dbutils import *
import os

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_COOKIE_SECURE = False # For production if not have SSL

SECRET_KEY = 'django-insecure-t3wh9u9h4w&8$vn%*bxofwvqy(^*z*!^&u=7ia!^ecj7u^lkh1'

IS_PRODUCTION = True if 'PRODUCT_UTE_ONLINE_JUDGE' in os.environ else False

DEBUG = not IS_PRODUCTION

SESSION_COOKIE_SECURE = False

ALLOWED_HOSTS = ['*']

WEBSITE_HOST_NAME = '127.0.0.1:8000'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

# Celery backend ----------------------------------------------------------------------

broker_url = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379'
accept_content = ['application/json']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'UTC'


# Media backend ----------------------------------------------------------------------

MEDIA_ROOT = os.environ['MEDIA_ROOT'] if 'MEDIA_ROOT' in os.environ else 'ADMIN_DATA_MEDIA/'
print('MEDIA_ROOT = ' + MEDIA_ROOT)
MEDIA_URL = '/media/'


# Email backend ----------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_POST = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'uteojsptest@gmail.com'
EMAIL_HOST_PASSWORD = 'admin123zz'


# List admin ------------------------------------------------------------------------
LIST_SUPER_USER = [ 'admin', 'root' ]



# Application definition ----------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend.apps.BackendConfig',
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
     'http://localhost:3000'
]

ROOT_URLCONF = 'uteoj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'frontend'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'backend.models.submission.context_processors_subission_result_status',
            ],
        },
    },
]

WSGI_APPLICATION = 'uteoj.wsgi.application'


# Database ----------------------------------------------------------------------

print('PID = ' + str(os.getpid()))

if IS_PRODUCTION: #docker file
    print('-------------------------------- PRODUCTION STARTED ------------------------------')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'uteoj',
            'USER': 'root',
            'PASSWORD': 'hcmute.f18c1a3b9e1b16e36d26fc6420ac985d',
            'HOST': 'db',
            'PORT': '3306',
        }
    }
else:
    print('-------------------------------- DEBUG STARTED ------------------------------')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DATABASE_NAME,
            'USER': DATABASE_USER,
            'PASSWORD': DATABASE_PASSWORD,
            'HOST': DATABASE_HOST,
            'PORT': DATABASE_PORT,
        }
    }

# Password validation ----------------------------------------------------------------------

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


# Internationalization ----------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) ----------------------------------------------------------------------

STATIC_URL = '/static/'

STATIC_ROOT =os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/statics'),
]

# Judger file (CSS, JavaScript, Images) ----------------------------------------------------------------------
# Các thư mục này để biên dịch + chạy chương trình

COMPILE_ROOT = 'tmp/compile/'
RUNNING_ROOT = 'tmp/run/'


# Default primary key field type ----------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
