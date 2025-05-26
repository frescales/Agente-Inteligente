from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class RegistroEnfermedad(BaseModel):
    id: str
    fecha: date
    ubicacion_id: str
    cultivo: str
    enfermedad: str
    severidad: Optional[str] = ""
    observaciones: Optional[str] = ""

class RegistroEnfermedadResponse(BaseModel):
    registros: List[RegistroEnfermedad]

class ClimaEnfermedadPatron(BaseModel):
    fecha: date
    ubicacion_id: str
    temperatura: float
    humedad: float
    enfermedad: Optional[str]

class ClimaEnfermedadResponse(BaseModel):
    patrones: List[ClimaEnfermedadPatron]

class ComparacionSensor(BaseModel):
    sensor: str
    promedio_con_enfermedad: Optional[float]
    promedio_sin_enfermedad: Optional[float]

class EnfermedadClimaComparacionResponse(BaseModel):
    comparaciones: List[ComparacionSensor]