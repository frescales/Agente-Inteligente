from fastapi import APIRouter
from influx_connector import get_ph_promedio_diario

router = APIRouter()

@router.get("/test")
def test_influx():
    return {"status": "Conexión con Influx funcionando 🟢"}

@router.get("/ph/hoy")
def obtener_ph_hoy():
    promedio = get_ph_promedio_diario()
    if promedio is None:
        return {"ph_promedio": None, "mensaje": "No se encontraron datos de pH"}
    return {"ph_promedio": promedio, "unidad": "pH"}
