"""
Django settings for gamificacion project.
Configurado para MongoDB (mongoengine) + CORS + Render deployment.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────
#  SEGURIDAD
# ─────────────────────────────────────────────
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-cambia-esto-en-produccion-12345678",
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]   # Render asigna un dominio dinámico; "*" lo cubre todo.

# ─────────────────────────────────────────────
#  APLICACIONES
# ─────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "telemetria",
]

# ─────────────────────────────────────────────
#  MIDDLEWARE
# ─────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",   # ← debe ir primero
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "gamificacion.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "gamificacion.wsgi.application"

# ─────────────────────────────────────────────
#  BASE DE DATOS
#  Django no usa SQL; desactivamos la DB por
#  defecto y conectamos MongoDB vía mongoengine.
# ─────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.dummy",
    }
}

import mongoengine

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://localhost:27017/gamificacion_db",   # sobreescribir en Render con variable de entorno
)

mongoengine.connect(host=MONGO_URI)

# ─────────────────────────────────────────────
#  CORS
# ─────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True

# ─────────────────────────────────────────────
#  DJANGO REST FRAMEWORK
# ─────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# ─────────────────────────────────────────────
#  INTERNACIONALIZACIÓN
# ─────────────────────────────────────────────
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
#  ARCHIVOS ESTÁTICOS (WhiteNoise para Render)
# ─────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
