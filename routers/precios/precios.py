from fastapi import APIRouter, HTTPException
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

router = APIRouter()

@router.get("/precios_insumo")
def get_precio(insumo_id: str, fecha: str):
    # 1. Traer todos los precios de ese insumo, cuya fecha_inicio sea válida
    result = supabase.table("precios_insumos").select("*")\
        .eq("insumo_id", insumo_id)\
        .lte("fecha_inicio", fecha)\
        .order("fecha_inicio", desc=True)\
        .execute()

    # 2. Filtrar por Python para permitir fecha_fin nula o posterior a la fecha dada
    precios_validos = [
        r for r in result.data
        if r["fecha_fin"] is None or r["fecha_fin"] >= fecha
    ]

    if not precios_validos:
        raise HTTPException(status_code=404, detail="Precio no encontrado")

    return precios_validos[0]
