from supabase import create_client
from os import getenv
from datetime import date
from utils.fecha import primer_dia_mes, hoy

url = getenv("SUPABASE_URL")
key = getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def obtener_total_producido(
    rango="mes",
    producto_id: str = None,
    ubicacion_id: str = None,
    fecha_inicio: date = None,
    fecha_fin: date = None,
    agrupado_por: str = None,
    comparacion: list = None
):
    base = supabase.table("produccion")

    # Filtro de fechas
    if rango == "mes":
        fecha_inicio = primer_dia_mes()
        fecha_fin = hoy()
    elif rango == "comparar":
        pass  # Ya vienen definidas

    query = base.select("*").gte("fecha", str(fecha_inicio)).lte("fecha", str(fecha_fin))

    if producto_id:
        query = query.eq("producto_id", producto_id)

    if ubicacion_id:
        query = query.eq("ubicacion_id", ubicacion_id)

    if comparacion:
        query = query.in_("ubicacion_id", comparacion)

    data = query.execute().data

    if agrupado_por == "ubicacion":
        resultado = {}
        for row in data:
            ubicacion = row["ubicacion_id"]
            resultado[ubicacion] = resultado.get(ubicacion, 0) + row["cantidad"]
        return resultado

    elif comparacion:
        resultado = {}
        for row in data:
            ubicacion = row["ubicacion_id"]
            resultado[ubicacion] = resultado.get(ubicacion, 0) + row["cantidad"]
        return resultado

    else:
        total = sum(row["cantidad"] for row in data)
        unidad = data[0]["unidad_id"] if data else "kg"
        return {"total_kg": total, "unidad": unidad}
