"""Servicios de reservas."""

from app.database import ejecutar_consulta, obtener_uno, obtener_todos
from app.models.reserva import ReservaCreate, ReservaUpdate
from app.exceptions.custom_exceptions import (
    ReservaSolapadaError,
    CapacidadExcedidaError,
    MesaNoExisteError,
    ClienteNoEncontradoError,
)
from datetime import datetime, timedelta
from typing import Optional

# Funciones para manejar reservas: crear, actualizar, cancelar, confirmar llegada, marcar como completada, obtener reservas por filtros o por id
def obtener_reservas(fecha: Optional[str] = None, cliente_id: Optional[int] = None, mesa_id: Optional[int] = None, estado: Optional[str] = None):
    """Lista reservas con filtros opcionales."""
    consulta = "SELECT * FROM reservas WHERE 1=1"
    parametros = []

    if fecha:
        consulta += " AND DATE(fecha_inicio) = DATE(?)"
        parametros.append(fecha)
    if cliente_id:
        consulta += " AND cliente_id = ?"
        parametros.append(cliente_id)
    if mesa_id:
        consulta += " AND mesa_id = ?"
        parametros.append(mesa_id)
    if estado:
        consulta += " AND estado = ?"
        parametros.append(estado)

    return obtener_todos(consulta, tuple(parametros))

# Función para obtener una reserva por su id
def obtener_reserva_por_id(reserva_id: int):
    """Obtiene una reserva por su id."""
    consulta = "SELECT * FROM reservas WHERE id = ?"
    return obtener_uno(consulta, (reserva_id,))

# Función para crear una nueva reserva, con validaciones de cliente, mesa, capacidad y solapamiento de horarios
def _asegurar_datetime(valor):
    """Convierte una fecha en datetime si viene como texto."""
    if isinstance(valor, str):
        return datetime.fromisoformat(valor)
    return valor

# Función para validar que el cliente existe
def _validar_cliente(cliente_id: int):
    """Valida que el cliente exista."""
    consulta_cliente = "SELECT * FROM clientes WHERE id = ?"
    cliente = obtener_uno(consulta_cliente, (cliente_id,))
    if not cliente:
        raise ClienteNoEncontradoError("No existe un cliente con ese id")

# Función para validar que la mesa existe y está activa
def _validar_mesa_activa(mesa_id: int):
    """Valida que la mesa exista y esté activa."""
    consulta_mesa = "SELECT * FROM mesas WHERE id = ?"
    mesa = obtener_uno(consulta_mesa, (mesa_id,))
    if not mesa:
        raise MesaNoExisteError("No existe una mesa con esa información")
    mesa_activa = mesa[4]
    if not mesa_activa:
        raise MesaNoExisteError("La mesa no está activa")
    return mesa

# Función para validar que no hay reservas solapadas para la misma mesa en el mismo horario
def _validar_reserva_solapada(mesa_id: int, fecha_inicio: datetime, fecha_fin: datetime, reserva_id: Optional[int] = None):
    """Valida que no haya solapamiento de reservas."""
    consulta_reservas = """
    SELECT * FROM reservas
    WHERE mesa_id = ?
      AND estado IN ('pendiente', 'confirmada')
      AND fecha_inicio < ?
      AND fecha_fin > ?
    """
    parametros = [mesa_id, fecha_fin, fecha_inicio]
    if reserva_id is not None:
        consulta_reservas += " AND id != ?"
        parametros.append(reserva_id)
    reservas_existentes = obtener_todos(consulta_reservas, tuple(parametros))
    if reservas_existentes:
        raise ReservaSolapadaError("Ya existe una reserva para esa mesa en ese horario")

# Función para crear una nueva reserva, con validaciones de cliente, mesa, capacidad y solapamiento de horarios
def crear_reserva(reserva: ReservaCreate):
    """Crea una reserva con validaciones básicas."""
    _validar_cliente(reserva.cliente_id)
    mesa = _validar_mesa_activa(reserva.mesa_id)

    capacidad_mesa = mesa[2]
    if reserva.numero_comensales > capacidad_mesa:
        raise CapacidadExcedidaError("El número de comensales excede la capacidad de la mesa")

    fecha_inicio = _asegurar_datetime(reserva.fecha_inicio)
    if fecha_inicio <= datetime.now(fecha_inicio.tzinfo):
        raise ValueError("La fecha de inicio debe ser futura")

    fecha_fin = fecha_inicio + timedelta(hours=2)
    _validar_reserva_solapada(reserva.mesa_id, fecha_inicio, fecha_fin)

    fecha_creacion = datetime.now(fecha_inicio.tzinfo)

    insert = """
    INSERT INTO reservas (cliente_id, mesa_id, fecha_inicio, fecha_fin, numero_comensales, estado, notas, fecha_creacion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    ejecutar_consulta(insert, (
        reserva.cliente_id,
        reserva.mesa_id,
        fecha_inicio,
        fecha_fin,
        reserva.numero_comensales,
        reserva.estado,
        reserva.notas,
        fecha_creacion
    ))

    return obtener_uno(
        "SELECT * FROM reservas WHERE cliente_id = ? AND mesa_id = ? AND fecha_inicio = ?",
        (reserva.cliente_id, reserva.mesa_id, fecha_inicio)
    )

# Función para actualizar una reserva existente, con validaciones de cliente, mesa, capacidad y solapamiento de horarios    
def actualizar_reserva(reserva_id: int, datos_actualizados: ReservaUpdate):
    """Actualiza una reserva con validaciones básicas."""
    reserva_actual = obtener_reserva_por_id(reserva_id)
    if not reserva_actual:
        return None

    cliente_id = datos_actualizados.cliente_id if datos_actualizados.cliente_id is not None else reserva_actual[1]
    mesa_id = datos_actualizados.mesa_id if datos_actualizados.mesa_id is not None else reserva_actual[2]
    fecha_inicio = datos_actualizados.fecha_inicio if datos_actualizados.fecha_inicio is not None else reserva_actual[3]
    numero_comensales = datos_actualizados.numero_comensales if datos_actualizados.numero_comensales is not None else reserva_actual[5]
    estado = datos_actualizados.estado if datos_actualizados.estado is not None else reserva_actual[6]
    notas = datos_actualizados.notas if datos_actualizados.notas is not None else reserva_actual[7]

    _validar_cliente(cliente_id)
    mesa = _validar_mesa_activa(mesa_id)

    fecha_inicio = _asegurar_datetime(fecha_inicio)
    if fecha_inicio <= datetime.now(fecha_inicio.tzinfo):
        raise ValueError("La fecha de inicio debe ser futura")

    capacidad_mesa = mesa[2]
    if numero_comensales > capacidad_mesa:
        raise CapacidadExcedidaError("El número de comensales excede la capacidad de la mesa")

    fecha_fin = fecha_inicio + timedelta(hours=2)
    _validar_reserva_solapada(mesa_id, fecha_inicio, fecha_fin, reserva_id=reserva_id)

    update = """
    UPDATE reservas
    SET cliente_id = ?, mesa_id = ?, fecha_inicio = ?, fecha_fin = ?, numero_comensales = ?, estado = ?, notas = ?
    WHERE id = ?
    """
    ejecutar_consulta(update, (
        cliente_id,
        mesa_id,
        fecha_inicio,
        fecha_fin,
        numero_comensales,
        estado,
        notas,
        reserva_id
    ))

    return obtener_reserva_por_id(reserva_id)

# Función para cancelar una reserva (cambia el estado a 'cancelada')
def cancelar_reserva(reserva_id: int):
    """Cancela una reserva cambiando su estado."""
    update = """
    UPDATE reservas
    SET estado = 'cancelada'
    WHERE id = ?
    """
    ejecutar_consulta(update, (reserva_id,))
    return obtener_reserva_por_id(reserva_id)

# Función para confirmar la llegada del cliente (cambia el estado a 'confirmada')
def confirmar_llegada_cliente_patch(reserva_id: int):
    """Confirma la llegada del cliente."""
    update = """
    UPDATE reservas
    SET estado = 'confirmada'
    WHERE id = ?
    """
    ejecutar_consulta(update, (reserva_id,))
    return obtener_reserva_por_id(reserva_id)

# Función para marcar una reserva como completada (cambia el estado a 'completada')
def marcar_reserva_como_completada_patch(reserva_id: int):
    """Marca la reserva como completada."""
    update = """
    UPDATE reservas
    SET estado = 'completada'
    WHERE id = ?
    """
    ejecutar_consulta(update, (reserva_id,))
    return obtener_reserva_por_id(reserva_id)

 