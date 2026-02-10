"""Rutas de estadísticas."""

from fastapi import APIRouter
from app.services.estadisticas_service import (
	obtener_ocupacion_diaria,
	obtener_ocupacion_semanal,
	obtener_clientes_frecuentes,
	obtener_mesas_populares,
	obtener_resumen_general,
)


router = APIRouter(prefix="/estadisticas", tags=["Estadisticas"])

# Endpoint para obtener la ocupación diaria
@router.get("/ocupacion/diaria")
def ocupacion_diaria(fecha: str):
	"""Devuelve la ocupación diaria para una fecha."""
	return obtener_ocupacion_diaria(fecha)


# Endpoint para obtener la ocupación semanal
@router.get("/ocupacion/semanal")
def ocupacion_semanal(fecha_inicio: str):
	"""Devuelve la ocupación de una semana."""
	return obtener_ocupacion_semanal(fecha_inicio)


# Endpoint para obtener los clientes más frecuentes
@router.get("/clientes-frecuentes")
def clientes_frecuentes():
	"""Devuelve el top de clientes con más reservas."""
	return obtener_clientes_frecuentes()


# Endpoint para obtener las mesas más populares
@router.get("/mesas-populares")
def mesas_populares():
	"""Devuelve las mesas más reservadas."""
	return obtener_mesas_populares()


# Endpoint para obtener un resumen general de estadísticas
@router.get("/resumen")
def resumen_general():
	"""Devuelve un resumen general de reservas."""
	return obtener_resumen_general()
