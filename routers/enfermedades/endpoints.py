from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import date
from datetime import date, timedelta
from services.influx_connector import query_influx
from typing import List, Dict, Any
from services.supabase_connector import supabase
from .schema import RegistroEnfermedadResponse, ClimaEnfermedadResponse, EnfermedadClimaComparacionResponse
from constants.clima import SENSORES_CLIMA


router = APIRouter()

@router.get("/registro", response_model=RegistroEnfermedadResponse)
def obtener_registros_enfermedades(
    fecha_inicio: date,
    fecha_fin: date,
    cultivo: Optional[str] = None
):
    query = supabase.table("enfermedades_detectadas") \
        .select("id, fecha, ubicacion_id, severidad, observaciones, catalogo_enfermedades(nombre)") \
        .gte("fecha", fecha_inicio).lte("fecha", fecha_fin)

    if cultivo:
        query = query.eq("cultivo", cultivo)

    data = query.execute().data

    respuesta = []
    for row in data:
        respuesta.append({
            "id": row["id"],
            "fecha": row["fecha"],
            "ubicacion_id": row["ubicacion_id"],
            "cultivo": row.get("cultivo", ""),
            "severidad": row.get("severidad", ""),
            "observaciones": row.get("observaciones", ""),
            "enfermedad": row["catalogo_enfermedades"]["nombre"]
        })

    return {"registros": respuesta}

@router.get("/registro", response_model=RegistroEnfermedadResponse)
def get_enfermedades_registradas(
    fecha_inicio: date,
    fecha_fin: date,
    ubicacion_id: Optional[str] = None
):
    query = supabase.table("enfermedades_detectadas") \
        .select("*, catalogo_enfermedades(nombre)") \
        .gte("fecha", fecha_inicio) \
        .lte("fecha", fecha_fin)

    if ubicacion_id:
        query = query.eq("ubicacion_id", ubicacion_id)

    registros = query.execute().data

    respuesta = [{
        "id": r["id"],
        "fecha": r["fecha"],
        "ubicacion_id": r["ubicacion_id"],
        "enfermedad": r["catalogo_enfermedades"]["nombre"],
        "severidad": r["severidad"],
        "observaciones": r.get("observaciones", "")
    } for r in registros]

    return {"registros": respuesta}

################# HISTORICO DE ENFERMEDADES DETECTADAS##########

@router.get("/enfermedades/historico")
def enfermedades_historicas(mes: int = Query(..., ge=1, le=12), año: int = Query(..., ge=2020, le=2100)):
    """
    Retorna las enfermedades detectadas en un mes y año específico,
    junto con su descripción y tratamiento desde el catálogo.
    """
    # Rango de fechas del mes
    fecha_inicio = date(año, mes, 1)
    if mes == 12:
        fecha_fin = date(año + 1, 1, 1)
    else:
        fecha_fin = date(año, mes + 1, 1)

    # Consulta enfermedades detectadas en el rango
    detectadas = supabase.table("enfermedades_detectadas") \
        .select("*") \
        .gte("fecha", str(fecha_inicio)) \
        .lt("fecha", str(fecha_fin)) \
        .execute().data

    if not detectadas:
        return {"total": 0, "enfermedades": []}

    # Extraer IDs únicos detectados
    ids_enfermedades = list(set(d["enfermedad_id"] for d in detectadas))

    # Consultar catálogo
    catalogo = supabase.table("catalogo_enfermedades") \
        .select("*") \
        .in_("id", ids_enfermedades) \
        .execute().data

    catalogo_map = {item["id"]: item for item in catalogo}

    # Armar respuesta
    resultado = []
    for enf_id in ids_enfermedades:
        match = catalogo_map.get(enf_id)
        if match:
            resultado.append({
                "id": enf_id,
                "nombre": match.get("nombre"),
                "descripcion": match.get("descripcion"),
                "tratamiento": match.get("tratamiento"),
                "casos": sum(1 for d in detectadas if d["enfermedad_id"] == enf_id)
            })

    return {"total": len(resultado), "enfermedades": resultado}