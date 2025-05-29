from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(title="Agente FRESCALES")

from routers.produccion import endpoints as produccion
from routers.insumos import router as insumos_router
from routers.enfermedades import router as enfermedades_router
from routers.sensores import endpoints as sensores_router  
from routers.precios import router as precios_router 

# Incluir routers
app.include_router(insumos_router, prefix="/insumos", tags=["Insumos"])
app.include_router(produccion.router, prefix="/produccion", tags=["Producción"])
app.include_router(enfermedades_router, prefix="/enfermedades", tags=["Enfermedades"])
app.include_router(precios_router, prefix="/precios", tags=["Precios"])

# Ruta raíz
@app.get("/")
def root():
    return {"message": "Agente FRESCALES activo 🧠🍓"}
