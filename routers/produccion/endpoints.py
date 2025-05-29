# routers/produccion/endpoints.py
from fastapi import APIRouter, Query
from typing import Optional
from datetime import date
from datetime import date, timedelta, datetime
from services.supabase_connector import obtener_total_producido

router = APIRouter()


########## PRODUCCION MES#########
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


# routers/produccion/endpoints_proyeccion.py##

@router.get("/proyeccion-mensual")
def proyeccion_mensual():
    """
    Estima la cantidad de kilos de fresas que se producirán este mes
    usando el promedio diario hasta la fecha multiplicado por los días restantes.
    """
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    dias_transcurridos = (hoy - inicio_mes).days + 1

    produccion_actual = obtener_total_producido(rango="rango", fecha_inicio=inicio_mes, fecha_fin=hoy)
    total_kg_actual = produccion_actual.get("total_kg", 0)

    promedio_diario = total_kg_actual / dias_transcurridos if dias_transcurridos > 0 else 0
    dias_en_mes = (inicio_mes.replace(month=inicio_mes.month % 12 + 1, day=1) - timedelta(days=1)).day
    dias_restantes = dias_en_mes - hoy.day

    proyeccion = round(total_kg_actual + promedio_diario * dias_restantes)

    return {
        "produccion_actual_kg": total_kg_actual,
        "promedio_diario_kg": round(promedio_diario, 2),
        "dias_restantes": dias_restantes,
        "proyeccion_kg_mes": proyeccion
    }

##########PRODUCCION HISTORICO######################
@router.get("/total-historico")
def total_producido_historico(
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    producto_id: Optional[str] = None,
    ubicacion_id: Optional[str] = None
):
    return obtener_total_producido(
        rango="rango",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        producto_id=producto_id,
        ubicacion_id=ubicacion_id
    )


