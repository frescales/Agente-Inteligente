from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(title="Agente FRESCALES")

# Importar routers
from routers import produccion, insumos, enfermedades, reportes, precios, sensor

# Incluir routers
app.include_router(produccion.router, prefix="/produccion", tags=["Producción"])
app.include_router(insumos.router, prefix="/insumos", tags=["Insumos"])
app.include_router(enfermedades.router, prefix="/enfermedades", tags=["Enfermedades"])
app.include_router(reportes.router, prefix="/reportes", tags=["Reportes"])
app.include_router(precios.router, prefix="/precios", tags=["Precios"])
app.include_router(sensor.router, prefix="/sensor", tags=["Sensores"])

# Ruta raíz
@app.get("/")
def root():
    return {"message": "Agente FRESCALES activo 🧠🍓"}
