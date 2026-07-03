"""
URL principal del proyecto gamificacion.
"""
from django.urls import path, include

urlpatterns = [
    path("api/", include("telemetria.urls")),
]
