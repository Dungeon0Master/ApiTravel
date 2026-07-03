"""
Views de la app telemetria.

Endpoint disponible
-------------------
POST /api/telemetria/
    Body JSON: { "pasos": <int>, "bpm": <float> }
    Respuesta: { "status": "ok", "id": "<mongo_id>", "fecha_registro": "<iso8601>" }
"""

import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import RegistroFisico


@method_decorator(csrf_exempt, name="dispatch")
class TelemetriaView(View):
    """
    Vista basada en clase ultra ligera.
    No usa DRF para minimizar dependencias; solo JsonResponse de Django.
    """

    def post(self, request, *args, **kwargs):
        # ── 1. Parsear el body ──────────────────────────────────────────
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse(
                {"status": "error", "detalle": "Body JSON inválido."},
                status=400,
            )

        # ── 2. Validar campos requeridos ────────────────────────────────
        pasos = data.get("pasos")
        bpm   = data.get("bpm")

        if pasos is None or bpm is None:
            return JsonResponse(
                {
                    "status": "error",
                    "detalle": "Los campos 'pasos' y 'bpm' son obligatorios.",
                },
                status=400,
            )

        if not isinstance(pasos, int) or pasos < 0:
            return JsonResponse(
                {"status": "error", "detalle": "'pasos' debe ser un entero >= 0."},
                status=400,
            )

        try:
            bpm = float(bpm)
            if bpm < 0:
                raise ValueError
        except (TypeError, ValueError):
            return JsonResponse(
                {"status": "error", "detalle": "'bpm' debe ser un número >= 0."},
                status=400,
            )

        # ── 3. Guardar en MongoDB ────────────────────────────────────────
        try:
            registro = RegistroFisico(pasos=pasos, bpm=bpm)
            registro.save()
        except Exception as exc:
            return JsonResponse(
                {"status": "error", "detalle": f"Error al guardar: {str(exc)}"},
                status=500,
            )

        # ── 4. Respuesta de confirmación ─────────────────────────────────
        return JsonResponse(
            {
                "status": "ok",
                "mensaje": "Registro guardado correctamente.",
                "id": str(registro.id),
                "fecha_registro": registro.fecha_registro.isoformat() + "Z",
            },
            status=200,
        )

    def get(self, request, *args, **kwargs):
        """Endpoint de salud: GET /api/telemetria/ → 200 OK"""
        return JsonResponse({"status": "activo", "endpoint": "POST /api/telemetria/"})
