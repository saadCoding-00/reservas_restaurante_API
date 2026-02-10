"""Rutas de reservas."""

from fastapi import APIRouter
from app.models.reserva import ReservaCreate, ReservaResponse, ReservaUpdate
from app.services.reserva_service import obtener_reservas, obtener_reserva_por_id, crear_reserva, actualizar_reserva, cancelar_reserva, confirmar_llegada_cliente_patch, marcar_reserva_como_completada_patch
from app.exceptions.custom_exceptions import (
    ReservaSolapadaError,
    CapacidadExcedidaError,
    MesaNoExisteError,
    ClienteNoEncontradoError,
    CancelacionNoPermitidaError,
)

router = APIRouter(prefix="/reservas", tags=["Reservas"])


# Endpoint Get /reservas/
@router.get("/", response_model=list[ReservaResponse])
def listar_reservas(fecha: str = None, cliente_id: int = None, mesa_id: int = None, estado: str = None):
    """Lista reservas con filtros opcionales."""
    return obtener_reservas(fecha, cliente_id, mesa_id, estado)

# Endpoint Get /reservas/{id}
@router.get("/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(reserva_id: int):
    """Obtiene una reserva por su id."""
    reserva = obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise ReservaSolapadaError("No existe una reserva con ese id")
    return reserva

# Endpoint Post /reservas/
@router.post("/", response_model=ReservaResponse)
def crear(reserva: ReservaCreate):
    """Crea una reserva nueva."""
    try:
        return crear_reserva(reserva)
    except (ReservaSolapadaError, CapacidadExcedidaError, MesaNoExisteError, ClienteNoEncontradoError) as e:
        raise e
    
# Endpoint Put /reservas/{id}
@router.put("/{reserva_id}", response_model=ReservaResponse)
def actualizar(reserva_id: int, datos_actualizados: ReservaUpdate):
    """Actualiza una reserva existente."""
    try:
        return actualizar_reserva(reserva_id, datos_actualizados)
    except (ReservaSolapadaError, CapacidadExcedidaError, MesaNoExisteError, ClienteNoEncontradoError) as e:
        raise e

# Endpoint DELETE /reservas/{id}
@router.delete("/{reserva_id}", response_model=ReservaResponse)
def cancelar(reserva_id: int):
    """Cancela una reserva por su id."""
    try:
        return cancelar_reserva(reserva_id)
    except CancelacionNoPermitidaError as e:
        raise e

# Endpoint PATCH /reservas/{id}/confirmar
@router.patch("/{reserva_id}/confirmar", response_model=ReservaResponse)
def confirmar_llegada(reserva_id: int):
    """Confirma la llegada del cliente."""
    try:
        return confirmar_llegada_cliente_patch(reserva_id)
    except ReservaSolapadaError as e:
        raise e
    
# Endpoint PATCH /reservas/{id}/completar
@router.patch("/{reserva_id}/completar", response_model=ReservaResponse)
def completar_reserva(reserva_id: int):
    """Marca la reserva como completada."""
    try:
        return marcar_reserva_como_completada_patch(reserva_id)
    except ReservaSolapadaError as e:
        raise e

