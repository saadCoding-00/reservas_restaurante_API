"""Modelos de reserva."""

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime, timedelta


# -----------------------
# Modelo base (común)
# -----------------------
class ReservaBase(BaseModel):
	"""Campos comunes de una reserva."""
	cliente_id: int = Field(..., ge=1)
	mesa_id: int = Field(..., ge=1)
	fecha_inicio: datetime
	numero_comensales: int = Field(..., ge=1)
	estado: Literal["pendiente", "confirmada", "completada", "cancelada"] = "pendiente"
	notas: Optional[str] = None


# -----------------------
# Para crear reserva (POST)
# -----------------------
class ReservaCreate(ReservaBase):
	"""Modelo para crear una reserva."""
	@validator("fecha_inicio")
	def fecha_inicio_futura(cls, value: datetime) -> datetime:
		if value <= datetime.now(value.tzinfo):
			raise ValueError("La fecha de inicio debe ser futura")
		return value


# -----------------------
# Para actualizar reserva (PUT)
# -----------------------
class ReservaUpdate(BaseModel):
	"""Modelo para actualizar una reserva."""
	cliente_id: Optional[int] = Field(None, ge=1)
	mesa_id: Optional[int] = Field(None, ge=1)
	fecha_inicio: Optional[datetime] = None
	numero_comensales: Optional[int] = Field(None, ge=1)
	estado: Optional[Literal["pendiente", "confirmada", "completada", "cancelada"]] = None
	notas: Optional[str] = None

	@validator("fecha_inicio")
	def fecha_inicio_futura(cls, value: Optional[datetime]) -> Optional[datetime]:
		if value is not None and value <= datetime.now(value.tzinfo):
			raise ValueError("La fecha de inicio debe ser futura")
		return value


# -----------------------
# Para respuestas (GET)
# -----------------------
class ReservaResponse(ReservaBase):
	"""Modelo de respuesta para reserva."""
	id: int
	fecha_fin: datetime
	fecha_creacion: datetime

	class Config:
		from_attributes = True
