# routers/insumos/schema.py
from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import date

class InsumoDetalle(BaseModel):
    insumo_id: str
    nombre: str
    cantidad: float
    unidad: str
    precio_unitario: float
    costo_total: float

class InsumosAplicadosResponse(BaseModel):
    id: str
    fecha: date
    ubicacion_id: str
    observaciones: Optional[str] = None
    insumos: List[InsumoDetalle]

class CostoMensual(BaseModel):
    mes: str
    total: float

class ComparacionItem(BaseModel):
    insumo_id: str
    nombre: str
    cantidad_a: float
    cantidad_b: float

class ComparacionInsumoResponse(BaseModel):
    comparaciones: List[ComparacionItem]

class EfectividadItem(BaseModel):
    insumo_id: str
    nombre: str
    costo_total: float
    produccion_total: float
    costo_por_kg: float

class EfectividadInsumoResponse(BaseModel):
    efectividad: List[EfectividadItem]
