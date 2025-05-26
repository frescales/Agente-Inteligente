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

@router.get("/patrones-clima", response_model=EnfermedadClimaComparacionResponse)
def patrones_clima(ubicacion_id: str, fecha_inicio: date, fecha_fin: date):
    # 1. Obtener enfermedades detectadas
    enfermedades = supabase.table("enfermedades_detectadas") \
        .select("id, fecha, ubicacion_id") \
        .eq("ubicacion_id", ubicacion_id) \
        .gte("fecha", fecha_inicio) \
        .lte("fecha", fecha_fin) \
        .execute().data

    fechas_con_enfermedad = {e["fecha"] for e in enfermedades}

    # 2. Preparar consulta a InfluxDB para sensores ambientales
    sensores = {
        "temperatura": "sensor.ambiente_temperatura_ambiente",
        "humedad": "sensor.ambiente_humedad_ambiente",
        "presion": "sensor.ambiente_presi_n_atmosf_rica",
        "lluvia": "binary_sensor.ambiente_sensor_lluvia",
        "luminosidad": "sensor.luminosidad_inv1"
    }

    resultados: Dict[str, Dict[str, List[float]]] = {s: {"con": [], "sin": []} for s in sensores}

    for sensor_nombre, entity_id in sensores.items():
        query = f'''
        from(bucket: "invernadero")
          |> range(start: {fecha_inicio}T00:00:00Z, stop: {fecha_fin + timedelta(days=1)}T00:00:00Z)
          |> filter(fn: (r) => r._measurement == "state" and r.entity_id == "{entity_id}")
          |> aggregateWindow(every: 1d, fn: mean)
          |> yield(name: "mean")
        '''

        data = query_influx(query)
        for d in data:
            fecha = d["_time"][:10]
            valor = d["_value"]
            if valor is None:
                continue
            if fecha in fechas_con_enfermedad:
                resultados[sensor_nombre]["con"].append(valor)
            else:
                resultados[sensor_nombre]["sin"].append(valor)

    # 3. Calcular promedios
    def promedio(lista):
        return round(sum(lista) / len(lista), 2) if lista else None

    comparaciones = []
    for sensor, valores in resultados.items():
        comparaciones.append({
            "sensor": sensor,
            "promedio_con_enfermedad": promedio(valores["con"]),
            "promedio_sin_enfermedad": promedio(valores["sin"])
        })

    return {"comparaciones": comparaciones}
