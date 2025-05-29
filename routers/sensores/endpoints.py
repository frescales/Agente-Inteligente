from fastapi import APIRouter, Query
from datetime import date
from services.influx_connector import (
    consultar_promedio_diario,
    consultar_valor_diario,
    analizar_clima_vs_produccion,
    exportar_entidades_csv

)
from routers.sensores.schema import PromedioSensorResponse
from constants.humedad_sustrato import SENSORES_HUMEDAD_SUSTRATO

router = APIRouter(
    prefix="/sensor",
    tags=["Sensores"]
)

@router.get("/ph/hoy", response_model=PromedioSensorResponse)
def obtener_ph_hoy():
    """
    Retorna el valor promedio de pH registrado hoy.
    """
    return consultar_promedio_diario(sensor_id="fresas_ph", field="value")

@router.get("/ce/hoy", response_model=PromedioSensorResponse)
def obtener_ce_hoy():
    """
    Retorna el valor promedio de Conductividad Eléctrica (CE) registrado hoy.
    """
    return consultar_promedio_diario(sensor_id="fresas_electrical_conductivity", field="value")

### LUMINOSIDAD SOLAR ########

@router.get("/luminosidad/historico")
def luminosidad_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="luminosidad_inv1",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="lx"
    )



## EXPORTAR ENTIDADES DAÑADO##

@router.get("/entidades/exportar")
def exportar_entidades():
    return exportar_entidades_csv()

### CE HISTORICO ########

@router.get("/ce/historico")
def ce_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="fresas_electrical_conductivity",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="state"
    )

### HUMEDAD AMBIENTE ########

@router.get("/humedad_ambiente/historico")
def humedad_ambiente_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="ambiente_humedad_ambiente",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="%"
    )

### TEMPERATURA AMBIENTE ########
@router.get("/temperatura/historico")
def temperatura_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="ambiente_temperatura_ambiente",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="°C"
    )


### PREION AMBIENTE ########
@router.get("/presion/historico")
def presion_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="ambiente_presi_n_atmosf_rica",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="hPa"
    )



### HUMEDAD SUSTRATOS########
@router.get("/humedad_sustrato/historico")
def humedad_sustrato_historico(
    inv: int = Query(...),
    zona: int = Query(...),
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...)
):
    sensor = SENSORES_HUMEDAD_SUSTRATO[f"inv{inv}"][f"zona{zona}"]
    entity_id = sensor["entity_id"]
    measurement = sensor["measurement"]

    return consultar_valor_diario(
        sensor_id=entity_id,
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement=measurement
    )

####PH HISTORICO#

@router.get("/ph/historico")
def ph_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="fresas_ph",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="state"
    )

    