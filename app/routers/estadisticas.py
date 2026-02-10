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
	return obtener_ocupacion_diaria(fecha)


# Endpoint para obtener la ocupación semanal
@router.get("/ocupacion/semanal")
def ocupacion_semanal(fecha_inicio: str):
	return obtener_ocupacion_semanal(fecha_inicio)


# Endpoint para obtener los clientes más frecuentes
@router.get("/clientes-frecuentes")
def clientes_frecuentes():
	return obtener_clientes_frecuentes()


# Endpoint para obtener las mesas más populares
@router.get("/mesas-populares")
def mesas_populares():
	return obtener_mesas_populares()


# Endpoint para obtener un resumen general de estadísticas
@router.get("/resumen")
def resumen_general():
	return obtener_resumen_general()
