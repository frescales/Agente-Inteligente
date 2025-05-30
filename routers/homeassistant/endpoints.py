from fastapi import APIRouter, Query
from services.home_assistant_connector import listar_entidades, estado_entidad, activar_switch, desactivar_switch

router = APIRouter(prefix="/homeassistant", tags=["Home Assistant"])


@router.get("/entidades")
def obtener_entidades():
    return listar_entidades()


@router.get("/estado")
def obtener_estado(entity_id: str = Query(...)):
    return estado_entidad(entity_id)


@router.post("/encender")
def encender_switch(entity_id: str = Query(...)):
    return activar_switch(entity_id)


@router.post("/apagar")
def apagar_switch(entity_id: str = Query(...)):
    return desactivar_switch(entity_id)
