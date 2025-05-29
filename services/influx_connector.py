
# services/influx_connector.py

from influxdb_client_3 import InfluxDBClient3
from dotenv import load_dotenv
from datetime import datetime, timedelta, date

import os
from datetime import datetime, timedelta
import pandas as pd

# Cargar variables de entorno
load_dotenv()

INFLUX_URL    = os.getenv("INFLUX_URL")
INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN")
INFLUX_ORG    = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

print(f"✅ INFLUX_URL    = {INFLUX_URL}")
print(f"✅ INFLUX_ORG    = {INFLUX_ORG}")
print(f"✅ INFLUX_BUCKET = {INFLUX_BUCKET}")

client = InfluxDBClient3(
    host=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
    database=INFLUX_BUCKET,
    verify_ssl=False
)

def query_influx(sensor_id: str, fecha_inicio: str, fecha_fin: str, measurement: str = "state") -> pd.DataFrame:
    filtro_horas = ""
    if sensor_id == "luminosidad_inv1":
        filtro_horas = "AND EXTRACT(HOUR FROM time) BETWEEN 7 AND 18"

    sql = f"""
    SELECT
      DATE_TRUNC('day', time) AS _time,
      MEAN(value) AS _value
    FROM "{measurement}"
    WHERE
      entity_id = '{sensor_id}'
      AND time >= '{fecha_inicio}T00:00:00Z'
      AND time <= '{fecha_fin}T23:59:59Z'
      {filtro_horas}
    GROUP BY 1
    ORDER BY _time ASC
    """
    print(f"\n🔍 SQL DEBUG:\n{sql}")
    try:
        result = client.query(query=sql, language="sql")
        return result.to_pandas()
    except Exception as e:
        print(f"❌ Error SQL Influx para {sensor_id}: {e}")
        return pd.DataFrame()


def consultar_promedio_diario(sensor_id: str, field: str) -> dict:
    hoy = datetime.utcnow().date()
    df = query_influx(sensor_id, str(hoy), str(hoy))

    print(f"\n🧪 DEBUG [{sensor_id}] → DataFrame:\n", df.head())

    if not df.empty and "_value" in df.columns:
        valor = round(df["_value"].mean(), 2)
        return {"sensor_id": sensor_id, "fecha": str(hoy), "promedio": valor}

    return {"sensor_id": sensor_id, "fecha": str(hoy), "promedio": None}

def consultar_valor_diario(sensor_id: str, field: str, dias: int = None, fecha_inicio: date = None, fecha_fin: date = None, measurement: str = "state") -> list:
    if dias is not None:
        fecha_fin = datetime.utcnow().date()
        fecha_inicio = fecha_fin - timedelta(days=dias)
    elif not (fecha_inicio and fecha_fin):
        raise ValueError("Debes proporcionar 'dias' o 'fecha_inicio' y 'fecha_fin'")

    df = query_influx(sensor_id, str(fecha_inicio), str(fecha_fin), measurement=measurement)

    if df.empty:
        return []

    df["_time"] = pd.to_datetime(df["_time"]).dt.date
    diario = df.groupby("_time")["_value"].mean().round(2)
    return [{"fecha": str(f), "valor": v} for f, v in diario.items()]



def analizar_clima_vs_produccion():
    from constants.clima import SENSORES_CLIMA
    from services.supabase_connector import obtener_total_producido

    hoy = datetime.utcnow().date()
    hace7 = hoy - timedelta(days=7)

    resultados = {}
    for clave, info in SENSORES_CLIMA.items():
        df = query_influx(info["entity_id"], str(hace7), str(hoy))
        if df.empty:
            resultados[clave] = None
        else:
            df["time"] = pd.to_datetime(df["time"]).dt.date
            diario = df.groupby("time")["_value"].mean().round(2)
            resultados[clave] = [{"fecha": str(k), "valor": v} for k, v in diario.items()]

    produccion = obtener_total_producido(rango="comparar", fecha_inicio=hace7, fecha_fin=hoy)

    return {"clima": resultados, "produccion": produccion}

def exportar_entidades_csv():
    """
    Exporta un CSV con los entity_id y metadata de los últimos 30 días.
    """
    ini = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")
    fin = datetime.utcnow().strftime("%Y-%m-%dT23:59:59Z")

    sql = f"""
    SELECT
      entity_id,
      domain,
      _measurement,
      _field,
      COUNT(*) AS registros
    FROM state
    WHERE time >= '{ini}' AND time <= '{fin}'
    GROUP BY entity_id, domain, _measurement, _field
    ORDER BY registros DESC
    """
    try:
        result = client.query(query=sql, language="sql")
        df = result.to_pandas()
        ruta = os.path.join(os.getcwd(), "entidades_influx.csv")
        df.to_csv(ruta, index=False)
        return {"status": "ok", "total": len(df), "archivo": ruta}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}
