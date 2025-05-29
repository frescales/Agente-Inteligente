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


#####CONECTOR GASTOS TOTALE##########

def obtener_costo_insumos(
    fecha_inicio: date,
    fecha_fin: date,
    invernadero_id: str = None
):
    # 1. Obtener todas las aplicaciones dentro del rango de fechas
    aplicaciones_query = supabase.table("insumos_aplicados") \
        .select("id") \
        .gte("fecha", str(fecha_inicio)) \
        .lte("fecha", str(fecha_fin))

    if invernadero_id:
        aplicaciones_query = aplicaciones_query.eq("ubicacion_id", invernadero_id)

    aplicaciones = aplicaciones_query.execute().data
    if not aplicaciones:
        return {"total_usd": 0.0, "registros": 0}

    # 2. Obtener los IDs de esas aplicaciones
    aplicacion_ids = [row["id"] for row in aplicaciones]

    # 3. Buscar todos los detalles vinculados
    detalles_query = supabase.table("detalle_insumos_aplicados") \
        .select("costo_total") \
        .in_("aplicacion_id", aplicacion_ids)

    detalles = detalles_query.execute().data
    total_usd = sum(item.get("costo_total", 0) for item in detalles)

    return {
        "total_usd": round(total_usd, 2),
        "registros": len(detalles),
        "aplicaciones_consultadas": len(aplicacion_ids)
    }



#####CONNECTOR INSUMOS POR MES USADOS##########

def obtener_consumo_por_insumo(fecha_inicio: date, fecha_fin: date) -> list:
    """
    Retorna el consumo total por insumo entre dos fechas.
    Se une detalle_insumos_aplicados con insumos y unidades para obtener nombre y unidad.
    """
    # 1. Obtener todas las aplicaciones en rango
    aplicaciones = supabase.table("insumos_aplicados") \
        .select("id") \
        .gte("fecha", str(fecha_inicio)) \
        .lte("fecha", str(fecha_fin)) \
        .execute().data

    if not aplicaciones:
        return []

    aplicacion_ids = [a["id"] for a in aplicaciones]

    # 2. Obtener los detalles asociados
    detalles = supabase.table("detalle_insumos_aplicados") \
        .select("insumo_id, cantidad") \
        .in_("aplicacion_id", aplicacion_ids) \
        .execute().data

    if not detalles:
        return []

    # 3. Agrupar por insumo
    consumo_por_insumo = {}
    for d in detalles:
        insumo_id = d["insumo_id"]
        cantidad = d.get("cantidad", 0)
        consumo_por_insumo[insumo_id] = consumo_por_insumo.get(insumo_id, 0) + cantidad

    # 4. Obtener nombres y unidades desde tabla insumos
    insumos_data = supabase.table("insumos").select("id, nombre, unidad_id").execute().data
    unidades_data = supabase.table("unidades").select("id, nombre").execute().data
    unidades_dict = {u["id"]: u["nombre"] for u in unidades_data}

    respuesta = []
    for insumo in insumos_data:
        iid = insumo["id"]
        if iid in consumo_por_insumo:
            respuesta.append({
                "insumo_id": iid,
                "nombre": insumo["nombre"],
                "unidad": unidades_dict.get(insumo["unidad_id"], "N/A"),
                "consumo_total": round(consumo_por_insumo[iid], 2)
            })

    return respuesta

