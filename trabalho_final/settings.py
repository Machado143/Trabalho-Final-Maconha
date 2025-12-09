"""
Django settings for trabalho_final project - RENDER + CLOUDINARY
Versão Corrigida - Deploy-Ready
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config, Csv

# ============================================
# DIRETÓRIOS BASE
# ============================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SEGURANÇA
# ============================================
SECRET_KEY = config('SECRET_KEY', default='django-insecure-local-dev-key-CHANGE-IN-PRODUCTION')
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'trabalho-final-maconha.onrender.com'
]


# ============================================
# APLICAÇÕES INSTALADAS
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps do projeto
    'plantas',
    
    # Bibliotecas externas
    'django_bootstrap5',
    'rest_framework',
    'corsheaders',
    'cloudinary_storage',  # DEVE vir ANTES de 'cloudinary'
    'cloudinary',
]

# ============================================
# MIDDLEWARE
# ============================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trabalho_final.urls'

# ============================================
# TEMPLATES
# ============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'plantas.context_processors.notificacoes_nao_lidas',
            ],
        },
    },
]

WSGI_APPLICATION = 'trabalho_final.wsgi.application'

# ============================================
# BANCO DE DADOS
# ============================================
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Produção: PostgreSQL do Render
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desenvolvimento local: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ============================================
# VALIDAÇÃO DE SENHAS
# ============================================
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

# ============================================
# INTERNACIONALIZAÇÃO
# ============================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ============================================
# CLOUDINARY - ARMAZENAMENTO DE IMAGENS
# ============================================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configurar Cloudinary
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME', default=''),
    api_key=config('CLOUDINARY_API_KEY', default=''),
    api_secret=config('CLOUDINARY_API_SECRET', default=''),
    secure=True
)

# ============================================
# STORAGES - Django 4.2+ (Substitui DEFAULT_FILE_STORAGE)
# ============================================
STORAGES = {
    # Storage para uploads de mídia (Cloudinary)
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # Storage para arquivos estáticos (WhiteNoise)
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ============================================
# ARQUIVOS ESTÁTICOS (CSS, JS, Imagens)
# ============================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# ============================================
# ARQUIVOS DE MÍDIA (Uploads)
# ============================================
if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'


# ============================================
# DJANGO REST FRAMEWORK
# ============================================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer'
    )


# ============================================
# CORS (Cross-Origin Resource Sharing)
# ============================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",  # Para frontend React/Vue local
]

# Se estiver em produção, adicione seu domínio do Render
if not DEBUG:
    CORS_ALLOWED_ORIGINS.append(
        config('RENDER_EXTERNAL_URL', default='https://trabalho-final-maconha.onrender.com')
    )

CORS_ALLOW_CREDENTIALS = True

# ============================================
# AUTENTICAÇÃO
# ============================================
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# ============================================
# MENSAGENS
# ============================================
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ============================================
# UPLOAD DE ARQUIVOS
# ============================================
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB

# Tipos de arquivo permitidos (validação adicional)
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# ============================================
# SEGURANÇA - CONFIGURAÇÕES DE PRODUÇÃO
# ============================================
if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Headers de segurança
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Referrer Policy
    SECURE_REFERRER_POLICY = 'same-origin'

# ============================================
# LOGGING - Para Debug em Produção
# ============================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO' if not DEBUG else 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'cloudinary': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ============================================
# CACHE - Para Performance em Produção
# ============================================
if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# ============================================
# EMAIL - Configuração para Notificações (Opcional)
# ============================================
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@paidoverde.com')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================
# ADMIN
# ============================================
ADMIN_SITE_HEADER = "Pai do Verde - Administração"
ADMIN_SITE_TITLE = "Pai do Verde"
ADMIN_INDEX_TITLE = "Bem-vindo ao painel administrativo"

# ============================================
# OUTRAS CONFIGURAÇÕES
# ============================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Timezone aware datetime
USE_TZ = True

# Formato de data/hora para exibição
DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i'
SHORT_DATE_FORMAT = 'd/m/Y'

# ============================================
# CONFIGURAÇÕES ESPECÍFICAS DO PROJETO
# ============================================

# Número máximo de plantas por usuário (None = ilimitado)
MAX_PLANTAS_PER_USER = None

# Número máximo de comentários por dia (proteção contra spam)
MAX_COMMENTS_PER_DAY = 50

# Dias para exibir notificações antigas
NOTIFICATION_RETENTION_DAYS = 30

# ============================================
# DEBUG TOOLBAR - Apenas para Desenvolvimento
# ============================================
if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1', 'localhost']
    except ImportError:
        pass

# ============================================
# VALIDAÇÃO DE CONFIGURAÇÃO
# ============================================
def validate_cloudinary_config():
    """Valida se o Cloudinary está configurado corretamente"""
    cloud_name = config('CLOUDINARY_CLOUD_NAME', default='')
    api_key = config('CLOUDINARY_API_KEY', default='')
    api_secret = config('CLOUDINARY_API_SECRET', default='')
    
    if not all([cloud_name, api_key, api_secret]):
        import warnings
        warnings.warn(
            "⚠️ Cloudinary não está configurado! "
            "Configure CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY e CLOUDINARY_API_SECRET "
            "nas variáveis de ambiente.",
            RuntimeWarning
        )
        return False
    return True

# Executar validação ao iniciar
if not DEBUG:
    validate_cloudinary_config()