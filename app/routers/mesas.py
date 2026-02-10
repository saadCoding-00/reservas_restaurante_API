"""Rutas de mesas."""

from fastapi import APIRouter
from app.models.mesa import MesaCreate, MesaResponse
from app.services.mesa_service import crear_mesa, obtener_todas_mesas, obtener_mesa_por_id, actualizar_mesa, eliminar_mesa, obtener_mesa_disponible
from app.exceptions.custom_exceptions import MesaNoExisteError

router = APIRouter(prefix="/mesas", tags=["Mesas"])

# Endpoint Get /mesas/
@router.post("/", response_model=MesaResponse)
def crear(mesa: MesaCreate):
    """Crea una mesa nueva."""
    return crear_mesa(mesa)

# Endpoint Get /mesas/{id}
@router.get("/{mesa_id}", response_model=MesaResponse)
def obtener_mesa(mesa_id: int):
    """Obtiene una mesa por su id."""
    mesa = obtener_mesa_por_id(mesa_id)
    if not mesa:
        raise MesaNoExisteError("No existe una mesa con ese id")
    return mesa

# Endpoint Post /mesas/
@router.get("/", response_model=list[MesaResponse])
def obtener_mesas():
    """Lista todas las mesas."""
    return obtener_todas_mesas()    

# Endpoint Put /mesas/{id}
@router.put("/{mesa_id}", response_model=MesaResponse)
def actualizar(mesa_id: int, datos_actualizados: MesaCreate):
    """Actualiza los datos de una mesa."""
    mesa = actualizar_mesa(mesa_id, datos_actualizados)
    if not mesa:
        raise MesaNoExisteError("No existe una mesa con ese id")
    return mesa 

# Endpoint Delete /mesas/{id}
@router.delete("/{mesa_id}", response_model=MesaResponse)
def eliminar(mesa_id: int):
    """Elimina una mesa por su id."""
    mesa = eliminar_mesa(mesa_id)
    if not mesa:
        raise MesaNoExisteError("No existe una mesa con ese id")
    return mesa

# Endpoint Get /mesas/disponibles/
@router.get("/disponibles/", response_model=list[MesaResponse])
def obtener_mesas_disponibles(fecha_inicio: str, fecha_fin: str, capacidad: int):
    """Devuelve mesas disponibles según filtros."""
    return obtener_mesa_disponible(fecha_inicio, fecha_fin, capacidad)

