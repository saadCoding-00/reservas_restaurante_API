from fastapi import APIRouter
from app.services.estadisticas_service import (
	obtener_ocupacion_diaria,
	obtener_ocupacion_semanal,
	obtener_clientes_frecuentes,
	obtener_mesas_populares,
	obtener_resumen_general,
)


router = APIRouter(prefix="/estadisticas", tags=["Estadisticas"])


@router.get("/ocupacion/diaria")
def ocupacion_diaria(fecha: str):
	return obtener_ocupacion_diaria(fecha)


@router.get("/ocupacion/semanal")
def ocupacion_semanal(fecha_inicio: str):
	return obtener_ocupacion_semanal(fecha_inicio)


@router.get("/clientes-frecuentes")
def clientes_frecuentes():
	return obtener_clientes_frecuentes()


@router.get("/mesas-populares")
def mesas_populares():
	return obtener_mesas_populares()


@router.get("/resumen")
def resumen_general():
	return obtener_resumen_general()
