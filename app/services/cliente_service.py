"""Servicios de clientes."""

from app.database import ejecutar_consulta, obtener_uno, obtener_todos
from app.models.cliente import ClienteCreate
from app.exceptions.custom_exceptions import ClienteYaExisteError


def crear_cliente(cliente: ClienteCreate):
    """Crea un cliente si el email no existe."""
    # 1. Comprobar si ya existe email
    consulta = "SELECT * FROM clientes WHERE email = ?"
    existente = obtener_uno(consulta, (cliente.email,))

    if existente:
        raise ClienteYaExisteError("Ya existe un cliente con ese email")

    # 2. Insertar en base de datos
    insert = """
    INSERT INTO clientes (nombre, email, telefono, notas)
    VALUES (?, ?, ?, ?)
    """
    ejecutar_consulta(insert, (
        cliente.nombre,
        cliente.email,
        cliente.telefono,
        cliente.notas
    ))

    # 3. Devolver cliente creado
    return obtener_uno("SELECT * FROM clientes WHERE email = ?", (cliente.email,))

def obtener_todos_clientes():
    """Obtiene la lista completa de clientes."""
    consulta = "SELECT * FROM clientes"
    return obtener_todos(consulta)


def obtener_cliente_por_id(cliente_id: int):
    """Obtiene un cliente por su id."""
    # 1. Comprobar si existe id
    consulta = "SELECT * FROM clientes WHERE id = ?"
    cliente = obtener_uno(consulta, (cliente_id,))
    if not cliente:
        return None
    return cliente

def actualizar_cliente(cliente_id: int, datos_actualizados: ClienteCreate):
    """Actualiza los datos de un cliente."""
    # 1. Comprobar si existe id
    consulta = "SELECT * FROM clientes WHERE id = ?"
    cliente = obtener_uno(consulta, (cliente_id,))
    if not cliente:
        return None

    # 2. Actualizar cliente
    update = """
    UPDATE clientes
    SET nombre = ?, email = ?, telefono = ?, notas = ?
    WHERE id = ?
    """
    ejecutar_consulta(update, (
        datos_actualizados.nombre,
        datos_actualizados.email,
        datos_actualizados.telefono,
        datos_actualizados.notas,
        cliente_id
    ))

    # 3. Devolver cliente actualizado
    return obtener_uno("SELECT * FROM clientes WHERE id = ?", (cliente_id,))

def eliminar_cliente(cliente_id: int):
    """Elimina un cliente si no tiene reservas activas."""
    # 1. Comprobar si existe id
    consulta = "SELECT * FROM clientes WHERE id = ?"
    cliente = obtener_uno(consulta, (cliente_id,))
    if not cliente:
        return None
    # 2. Comprobar si tiene reservas activas
    consulta_reservas = """
    SELECT * FROM reservas
    WHERE cliente_id = ? AND estado IN ('pendiente', 'confirmada')
    """
    reservas_activas = ejecutar_consulta(consulta_reservas, (cliente_id,))
    if reservas_activas:
        return "No se puede eliminar el cliente porque tiene reservas activas"
    # 3. Eliminar cliente
    delete = "DELETE FROM clientes WHERE id = ?"
    ejecutar_consulta(delete, (cliente_id,))
    return "Cliente eliminado correctamente"

def obtener_cliente_por_nombre_o_email_o_telefono(busqueda: str):
    """Busca clientes por nombre, email o teléfono."""
    consulta = """
    SELECT * FROM clientes
    WHERE nombre LIKE ? OR email LIKE ? OR telefono LIKE ?
    """
    parametro_busqueda = f"%{busqueda}%"
    return ejecutar_consulta(consulta, (parametro_busqueda, parametro_busqueda, parametro_busqueda))
