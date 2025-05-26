from fastapi import APIRouter
from services.supabase_service import supabase

router = APIRouter()

@router.get("/resumen-semanal")
def resumen():
    produccion = supabase.table("produccion").select("*").limit(10).execute()
    enfermedades = supabase.table("enfermedades_detectadas").select("*").limit(10).execute()
    return {
        "produccion": produccion.data,
        "enfermedades": enfermedades.data
    }
