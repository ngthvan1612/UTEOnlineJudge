from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_COOKIE_SECURE = False # For production if not have SSL

SESSION_COOKIE_SAMESITE = None

SECRET_KEY = 'django-insecure-t3wh9u9h4w&8$vn%*bxofwvqy(^*z*!^&u=7ia!^ecj7u^lkh1'

IS_PRODUCTION = True if 'PRODUCT_UTE_ONLINE_JUDGE' in os.environ else False

DEBUG = not IS_PRODUCTION

SESSION_COOKIE_SECURE = False

ALLOWED_HOSTS = ['*']

WEBSITE_HOST_NAME = '127.0.0.1:8000'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

X_FRAME_OPTIONS = 'SAMEORIGIN'

NUMBER_OF_DECIMAL = 2


# Celery backend ----------------------------------------------------------------------

broker_url = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379'
accept_content = ['application/json']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'Asia/Ho_Chi_Minh'

# Media backend ----------------------------------------------------------------------

if DEBUG:
    MEDIA_ROOT = '../../uteoj_data/media'
    PROBLEM_ROOT = '../../uteoj_data/problems'
    USER_ROOT = '../../uteoj_data/user'
    IMPORT_USER_ROOT = '../../uteoj_data/importuser'
    MEDIA_URL = '/media/'
else:
    MEDIA_ROOT = '/uteoj_data/media'
    PROBLEM_ROOT = '/uteoj_data/problems'
    USER_ROOT = '/uteoj_data/user'
    IMPORT_USER_ROOT = '/uteoj_data/importuser'
    MEDIA_URL = '/media/'


# Email backend ----------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


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
    'rest_framework.authtoken',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', 
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_WHITELIST = [
     'http://localhost:8000'
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
                'backend.models.problem.context_processors_problem_type',
                'backend.models.usersetting.context_processors_user_setting',
            ],
        },
    },
]

WSGI_APPLICATION = 'uteoj.wsgi.application'


# Database ----------------------------------------------------------------------

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
    from .dbutils import *
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

PASSWORD_HASHERS = [
    'backend.auth.password_hasher.UTEOJ_PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher'
]

# Internationalization ----------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

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

if DEBUG:
    COMPILE_ROOT = '../../tmp/compile/'
    RUNNING_ROOT = '../../tmp/run/'
else:
    try:
        os.system('mkdir -p /uteoj_temp/compile/')
        os.system('mkdir -p /uteoj_temp/run/')
    except: pass
    COMPILE_ROOT = '/uteoj_temp/compile/'
    RUNNING_ROOT = '/uteoj_temp/run/'

# User chạy chương trình
import pwd, grp

COMPILER_UID = pwd.getpwnam('uteoj_compiler').pw_gid
COMPILER_GID = grp.getgrnam('uteoj_compiler').gr_gid

RUN_UID = pwd.getpwnam('uteoj_run').pw_gid
RUN_GID = grp.getgrnam('uteoj_run').gr_gid

# Default primary key field type ----------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

