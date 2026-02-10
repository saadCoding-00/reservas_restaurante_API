"""Servicios de mesas."""

from app.database import ejecutar_consulta, obtener_uno, obtener_todos
from app.models.mesa import MesaCreate
from app.exceptions.custom_exceptions import MesaNoExisteError, MesaYaExisteError


def obtener_todas_mesas():
    """Obtiene la lista completa de mesas."""
    consulta = "SELECT * FROM mesas"
    return obtener_todos(consulta)

def obtener_mesa_por_id(mesa_id: int):
    """Obtiene una mesa por su id."""
        # 1. Comprobar si existe id
    consulta = "SELECT * FROM mesas WHERE id = ?"
    mesa = obtener_uno(consulta, (mesa_id,))
    if not mesa:
        raise MesaNoExisteError("No existe una mesa con este id")
    return mesa

def crear_mesa(mesa: MesaCreate):
    """Crea una mesa si el número no existe."""
    # 1. Comprobar si ya existe numero_mesa
    consulta = "SELECT * FROM mesas WHERE numero = ?"
    existente = obtener_uno(consulta, (mesa.numero,))

    if existente:
        raise MesaYaExisteError("Ya existe una mesa con este numero de mesa")

    # 2. Insertar en base de datos
    insert = """
    INSERT INTO mesas (numero, capacidad, ubicacion, activa)
    VALUES (?, ?, ?, ?)
    """
    ejecutar_consulta(insert, (
        mesa.numero,
        mesa.capacidad,
        mesa.ubicacion,
        mesa.activa
    ))

    # 3. Devolver mesa creada
    return obtener_uno("SELECT * FROM mesas WHERE numero = ?", (mesa.numero,))

def actualizar_mesa(mesa_id: int, datos_actualizados: MesaCreate):
    """Actualiza los datos de una mesa."""
    # 1. Comprobar si existe id
    consulta = "SELECT * FROM mesas WHERE id = ?"
    mesa = obtener_uno(consulta, (mesa_id,))
    if not mesa:
        raise MesaNoExisteError("No existe una mesa con este id")

    # 2. Actualizar mesa
    update = """
    UPDATE mesas
    SET numero = ?, capacidad = ?, ubicacion = ?, activa = ?
    WHERE id = ?
    """
    ejecutar_consulta(update, (
        datos_actualizados.numero,
        datos_actualizados.capacidad,
        datos_actualizados.ubicacion,
        datos_actualizados.activa,
        mesa_id
    ))

    # 3. Devolver mesa actualizada
    return obtener_uno("SELECT * FROM mesas WHERE id = ?", (mesa_id,))


def eliminar_mesa(mesa_id: int):
    """Elimina una mesa si no tiene reservas futuras."""
    
    #1. comprobar si existe id
    consulta = "SELECT * FROM mesas WHERE id = ?"
    mesa = obtener_uno(consulta,(mesa_id))
    if not mesa:
        raise MesaNoExisteError("No existe ninguna mesa con este id")
    
    #2. comprobar si no tiene reservas futuras
    consulta_reservas = """
    SELECT * FROM reservas
    WHERE cliente_id = ? AND estado IN ('pendiente', 'confirmada')
    """

    reservas_activas = ejecutar_consulta(consulta_reservas, (mesa_id,))
    if reservas_activas:
        return "No se puede eliminar la mesa porque tiene reservas futuras"
    # 3. Eliminar mesa
    delete = "DELETE FROM mesas WHERE id = ?"
    ejecutar_consulta(delete, (mesa_id,))
    return "Mesa eliminada correctamente"

def obtener_mesa_disponible(numero: int, fecha_hora: str):
    """Busca una mesa disponible por número y fecha."""
    consulta = """
    SELECT * FROM mesas
    WHERE numero = ? AND id NOT IN (
        SELECT mesa_id FROM reservas
        WHERE fecha_hora = ? AND estado IN ('pendiente', 'confirmada')
    )
    """
    return obtener_uno(consulta, (numero, fecha_hora))
