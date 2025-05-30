import requests
from os import getenv

HA_URL = getenv("HA_URL")
HA_TOKEN = getenv("HA_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}


def listar_entidades():
    url = f"{HA_URL}/api/states"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def estado_entidad(entity_id: str):
    url = f"{HA_URL}/api/states/{entity_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def activar_switch(entity_id: str):
    url = f"{HA_URL}/api/services/switch/turn_on"
    data = {"entity_id": entity_id}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()


def desactivar_switch(entity_id: str):
    url = f"{HA_URL}/api/services/switch/turn_off"
    data = {"entity_id": entity_id}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()
