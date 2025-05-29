# routers/produccion/schema.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class FiltroProduccion(BaseModel):
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    ubicacion_id: Optional[str]
    producto_id: Optional[str]

class ResultadoProduccion(BaseModel):
    total_kg: float
    unidad: str
