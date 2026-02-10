from pydantic import BaseModel, Field
from typing import Optional, Literal


class MesaBase(BaseModel):
    numero: int = Field(..., ge=1, le=99) # ge significa mayor o igual que, le significa menor o igual que
    capacidad: Literal[2, 4, 6, 8]
    ubicacion: str = Field(..., pattern="^(interior|terraza|privado)$") # regex significa que debe ser una de esas tres opciones
    activa: bool = True # Por defecto la mesa está activa
    
class MesaCreate(MesaBase):
    pass

class MesaUpdate(BaseModel):
    numero: Optional[int] = Field(None, ge=1, le=99) 
    capacidad: Optional[Literal[2, 4, 6, 8]] = None
    ubicacion: Optional[str] = Field(None, pattern="^(interior|terraza|privado)$") 
    activa: Optional[bool] = None

class MesaResponse(MesaBase):
    id: int
    
    class Config:
        from_attributes = True