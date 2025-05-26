from influxdb_client import InfluxDBClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Leer configuración desde .env
INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = "invernadero"

# Cliente principal de InfluxDB
client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
)

query_api = client.query_api()

def query_influx(query: str):
    try:
        return query_api.query_data_frame(org=INFLUX_ORG, query=query)
    except Exception as e:
        print(f"❌ Error consultando InfluxDB: {e}")
        return None
