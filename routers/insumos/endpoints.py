from fastapi import APIRouter, Query
from supabase import create_client
from services.supabase_connector import obtener_consumo_por_insumo
from os import getenv
from datetime import date
from dotenv import load_dotenv
from .schema import (
    InsumosAplicadosResponse,
    CostoMensual,
    ComparacionInsumoResponse,
    EfectividadInsumoResponse,
)

# routers/insumos/endpoints.py
from fastapi import APIRouter, Query
from typing import List
from datetime import datetime
from datetime import date
from services.supabase_connector import supabase
from .schema import (
    InsumosAplicadosResponse, CostoMensual, ComparacionInsumoResponse, EfectividadInsumoResponse
)

router = APIRouter()

@router.get("/aplicados", response_model=List[InsumosAplicadosResponse])
def get_insumos_aplicados(fecha_inicio: date, fecha_fin: date):
    aplicaciones = supabase.table("insumos_aplicados").select("*").gte("fecha", fecha_inicio).lte("fecha", fecha_fin).execute().data
    detalles = supabase.table("detalle_insumos_aplicados").select("*, insumos(nombre), unidades(nombre)").execute().data

    respuesta = []
    for app in aplicaciones:
        insumos_detalle = [
            {
                "insumo_id": d["insumo_id"],
                "nombre": d["insumos"]["nombre"],
                "cantidad": d["cantidad"],
                "unidad": d["unidades"]["nombre"],
                "precio_unitario": d["precio_unitario_usado"],
                "costo_total": d["cantidad"] * d["precio_unitario_usado"]
            }
            for d in detalles if d["aplicacion_id"] == app["id"]
        ]
        respuesta.append({
            "id": app["id"],
            "fecha": app["fecha"],
            "ubicacion_id": app["ubicacion_id"],
            "observaciones": app.get("observaciones", ""),
            "insumos": insumos_detalle
        })
    return respuesta

@router.get("/costos-mensuales", response_model=List[CostoMensual])
def get_costos_mensuales():
    detalles = supabase.table("detalle_insumos_aplicados").select("*, insumos_aplicados(fecha)").execute().data
    costos = {}
    for d in detalles:
        fecha = d["insumos_aplicados"]["fecha"]
        mes = fecha[:7]  # yyyy-mm
        total = d["cantidad"] * d["precio_unitario_usado"]
        costos[mes] = costos.get(mes, 0) + total

    return [{"mes": k, "total": round(v, 2)} for k, v in sorted(costos.items())]

@router.get("/comparar", response_model=ComparacionInsumoResponse)
def comparar_insumos(ubicacion_a: str, ubicacion_b: str, fecha_inicio: date, fecha_fin: date):
    detalles = supabase.table("detalle_insumos_aplicados").select("*, insumos(nombre), insumos_aplicados(ubicacion_id,fecha)").execute().data

    a, b = {}, {}
    for d in detalles:
        app = d["insumos_aplicados"]
        # 🔧 Convertimos la fecha string a objeto date
        fecha_aplicacion = datetime.strptime(app["fecha"], "%Y-%m-%d").date()

        if fecha_inicio <= fecha_aplicacion <= fecha_fin:
            total = d["cantidad"]
            key = d["insumo_id"]
            if app["ubicacion_id"] == ubicacion_a:
                a[key] = a.get(key, 0) + total
            elif app["ubicacion_id"] == ubicacion_b:
                b[key] = b.get(key, 0) + total

    insumo_nombres = {d["insumo_id"]: d["insumos"]["nombre"] for d in detalles}
    todos_ids = set(a) | set(b)
    resultado = [{
        "insumo_id": i,
        "nombre": insumo_nombres.get(i, ""),
        "cantidad_a": round(a.get(i, 0), 2),
        "cantidad_b": round(b.get(i, 0), 2)
    } for i in todos_ids]

    return {"comparaciones": resultado}

@router.get("/efectividad", response_model=EfectividadInsumoResponse)
def efectividad_insumos(ubicacion_id: str, fecha_inicio: date, fecha_fin: date):
    detalles = supabase.table("detalle_insumos_aplicados").select("*, insumos(nombre), insumos_aplicados(ubicacion_id,fecha)").execute().data
    produccion = supabase.table("produccion").select("*").eq("ubicacion_id", ubicacion_id).gte("fecha", fecha_inicio).lte("fecha", fecha_fin).execute().data

    produccion_total = sum(p["cantidad"] for p in produccion)
    acumulado = {}

    for d in detalles:
        app = d["insumos_aplicados"]
        # 🔧 Convertimos la fecha string a objeto date
        fecha_aplicacion = datetime.strptime(app["fecha"], "%Y-%m-%d").date()

        if app["ubicacion_id"] == ubicacion_id and fecha_inicio <= fecha_aplicacion <= fecha_fin:
            insumo_id = d["insumo_id"]
            nombre = d["insumos"]["nombre"]
            costo = d["cantidad"] * d["precio_unitario_usado"]
            if insumo_id not in acumulado:
                acumulado[insumo_id] = {"nombre": nombre, "costo": 0}
            acumulado[insumo_id]["costo"] += costo

    respuesta = [{
        "insumo_id": i,
        "nombre": v["nombre"],
        "costo_total": round(v["costo"], 2),
        "produccion_total": round(produccion_total, 2),
        "costo_por_kg": round(v["costo"] / produccion_total, 4) if produccion_total > 0 else 0
    } for i, v in acumulado.items()]

    return {"efectividad": respuesta}


########CONSUMO AGRUPADO POR INSUMO############

@router.get("/consumo/rango")
def consumo_insumos_rango(
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...)
):
    return obtener_consumo_por_insumo(fecha_inicio, fecha_fin)