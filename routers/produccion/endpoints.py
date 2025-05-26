# routers/produccion/endpoints.py
from fastapi import APIRouter, Query
from typing import Optional
from datetime import date
from services.supabase_connector import obtener_total_producido

router = APIRouter()

@router.get("/total-mes")
def total_producido_mes(
    producto_id: Optional[str] = None,
    ubicacion_id: Optional[str] = None
):
    return obtener_total_producido(rango="mes", producto_id=producto_id, ubicacion_id=ubicacion_id)


@router.get("/por-invernadero")
def total_por_invernadero(
    fecha_inicio: date,
    fecha_fin: date,
    producto_id: Optional[str] = None
):
    return obtener_total_producido(rango="rango", producto_id=producto_id, agrupado_por="ubicacion", fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


@router.get("/comparar")
def comparar_invernaderos(
    invernadero_a: str,
    invernadero_b: str,
    fecha_inicio: date,
    fecha_fin: date,
    producto_id: Optional[str] = None
):
    return obtener_total_producido(
        rango="comparar",
        producto_id=producto_id,
        comparacion=[invernadero_a, invernadero_b],
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
