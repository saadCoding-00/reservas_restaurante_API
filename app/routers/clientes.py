from fastapi import APIRouter
from app.models.cliente import ClienteCreate, ClienteResponse
from app.services.cliente_service import crear_cliente, obtener_todos_clientes, obtener_cliente_por_id, actualizar_cliente, eliminar_cliente
from app.exceptions.custom_exceptions import ClienteNoEncontradoError

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# Endpoint Get /clientes/
@router.post("/", response_model=ClienteResponse)
def crear(cliente: ClienteCreate):
    return crear_cliente(cliente)

# Endpoint Get /clientes/{id}
@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int):
    cliente = obtener_cliente_por_id(cliente_id)
    if not cliente:
        raise ClienteNoEncontradoError("No existe un cliente con ese id")
    return cliente

# Endpoint Post /clientes/
@router.get("/", response_model=list[ClienteResponse])
def obtener_clientes():
    return obtener_todos_clientes()

# Endpoint Put /clientes/{id}
@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar(cliente_id: int, datos_actualizados: ClienteCreate):
    cliente = actualizar_cliente(cliente_id, datos_actualizados)
    if not cliente:
        raise ClienteNoEncontradoError("No existe un cliente con ese id")
    return cliente

# Endpoint Delete /clientes/{id}
@router.delete("/{cliente_id}", response_model=ClienteResponse)
def eliminar(cliente_id: int):
    cliente = eliminar_cliente(cliente_id)
    if not cliente:
        raise ClienteNoEncontradoError("No existe un cliente con ese id")
    return cliente