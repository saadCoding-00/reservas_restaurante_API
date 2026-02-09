from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# -----------------------
# Modelo base (común)
# Aqui van los campos comun
# -----------------------
class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=3) # ... significa obligatorio
    email: EmailStr # EmailStr significa debe ser un email valido y pydantic lo valida
    telefono: str = Field(..., min_length=9, max_length=9)
    notas: Optional[str] = None


# -----------------------
# Para crear cliente (POST)
# solo los campos que necesitamos para crear cliente 
# y si lo ponen la base de datos entonces no hay que ponerlos
# -----------------------
class ClienteCreate(ClienteBase):
    pass #Aquí no añado nada nuevo, pero la clase debe existir.


# -----------------------
# Para actualizar cliente (PUT)
# Aqui el usuario puede mandar solo lo que quiere cambiar
# Por eso todos los campos son opcionales
# -----------------------
class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3) # None significa que es opcional 
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, min_length=9, max_length=9)
    notas: Optional[str] = None


# -----------------------
# Para respuestas (GET)
# Eso lo que devuelve la base de datos
# Aqui se aparecen id y fecha porque se generan auto en la base de datos
# -----------------------
class ClienteResponse(ClienteBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True
