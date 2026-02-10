"""Modelos de mesa."""

from pydantic import BaseModel, Field
from typing import Optional, Literal

# Modelos para Mesa
# El modelo base para crear o actualizar una mesa
class MesaBase(BaseModel):
    """Campos comunes de una mesa."""
    numero: int = Field(..., ge=1, le=99) # ge significa mayor o igual que, le significa menor o igual que
    capacidad: Literal[2, 4, 6, 8]
    ubicacion: str = Field(..., pattern="^(interior|terraza|privado)$") # regex significa que debe ser una de esas tres opciones
    activa: bool = True # Por defecto la mesa está activa

# Modelo para crear una mesa (hereda de MesaBase)    
class MesaCreate(MesaBase):
    """Modelo para crear una mesa."""
    pass

# Modelo para actualizar una mesa (todos los campos son opcionales)
class MesaUpdate(BaseModel):
    """Modelo para actualizar una mesa."""
    numero: Optional[int] = Field(None, ge=1, le=99) 
    capacidad: Optional[Literal[2, 4, 6, 8]] = None
    ubicacion: Optional[str] = Field(None, pattern="^(interior|terraza|privado)$") 
    activa: Optional[bool] = None

# Modelo para la respuesta de una mesa (incluye el id y hereda de MesaBase)
class MesaResponse(MesaBase):
    """Modelo de respuesta para mesa."""
    id: int
    
    class Config:
        from_attributes = True