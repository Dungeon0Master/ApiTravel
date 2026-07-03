"""
URLs de la app telemetria.
Se incluyen desde gamificacion/urls.py bajo el prefijo /api/
→ El endpoint final queda en: POST /api/telemetria/
"""

from django.urls import path
from .views import TelemetriaView

urlpatterns = [
    path("telemetria/", TelemetriaView.as_view(), name="telemetria"),
]
