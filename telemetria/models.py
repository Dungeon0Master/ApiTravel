"""
Modelo MongoDB para el registro físico de telemetría.

Usamos mongoengine (Document) en lugar de django.db.models
para trabajar directamente con MongoDB sin ORM SQL.
"""

import mongoengine as me
from datetime import datetime


class RegistroFisico(me.Document):
    """
    Almacena un único evento de telemetría enviado desde la app Android.

    Campos
    ------
    pasos          : int   — Número de pasos registrados en el intervalo.
    bpm            : float — Frecuencia cardíaca en pulsaciones por minuto.
    fecha_registro : datetime — Timestamp UTC del momento de inserción.
    """

    pasos = me.IntField(required=True, min_value=0)
    bpm   = me.FloatField(required=True, min_value=0.0)
    fecha_registro = me.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "registros_fisicos",   # nombre de la colección en MongoDB
        "ordering": ["-fecha_registro"],     # más reciente primero
        "indexes": ["fecha_registro"],
    }

    def __str__(self):
        return f"RegistroFisico(pasos={self.pasos}, bpm={self.bpm}, fecha={self.fecha_registro})"
