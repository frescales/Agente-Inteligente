# routers/sensores/schema.py

from pydantic import BaseModel

class PromedioSensorResponse(BaseModel):
    sensor_id: str
    fecha: str
    promedio: float | None
