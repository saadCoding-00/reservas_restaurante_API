"""Servicios de estadísticas."""

from datetime import datetime, timedelta
from app.database import obtener_todos, obtener_uno

# Funcion para calcular la ocupación diaria, semanal, clientes frecuentes, mesas populares y resumen general de reservas
def obtener_ocupacion_diaria(fecha: str):
    """Calcula la ocupación de un día."""
    consulta = """
    SELECT
        COUNT(*) as total_reservas,
        COALESCE(SUM(num_comensales), 0) as total_comensales
    FROM reservas
    WHERE DATE(fecha_hora_inicio) = DATE(?)
      AND estado IN ('pendiente', 'confirmada', 'completada')
    """
    resultado = obtener_uno(consulta, (fecha,))
    return {
        "fecha": fecha,
        "total_reservas": resultado["total_reservas"] if resultado else 0,
        "total_comensales": resultado["total_comensales"] if resultado else 0,
    }

# Función para calcular la ocupación semanal
def obtener_ocupacion_semanal(fecha_inicio: str):
    """Calcula la ocupación de una semana completa."""
    inicio = datetime.fromisoformat(fecha_inicio).date()
    fin = inicio + timedelta(days=6)

    consulta = """
    SELECT DATE(fecha_hora_inicio) as fecha, COUNT(*) as total_reservas
    FROM reservas
    WHERE DATE(fecha_hora_inicio) BETWEEN DATE(?) AND DATE(?)
      AND estado IN ('pendiente', 'confirmada', 'completada')
    GROUP BY DATE(fecha_hora_inicio)
    ORDER BY DATE(fecha_hora_inicio)
    """
    filas = obtener_todos(consulta, (inicio.isoformat(), fin.isoformat()))
    return {
        "fecha_inicio": inicio.isoformat(),
        "fecha_fin": fin.isoformat(),
        "ocupacion": [
            {"fecha": fila["fecha"], "total_reservas": fila["total_reservas"]}
            for fila in (filas or [])
        ],
    }

# Función para obtener los clientes más frecuentes
def obtener_clientes_frecuentes():
    """Devuelve el top 10 de clientes con más reservas."""
    consulta = """
    SELECT cliente_id, COUNT(*) as total_reservas
    FROM reservas
    GROUP BY cliente_id
    ORDER BY total_reservas DESC
    LIMIT 10
    """
    filas = obtener_todos(consulta)
    return [
        {"cliente_id": fila["cliente_id"], "total_reservas": fila["total_reservas"]}
        for fila in (filas or [])
    ]

# Función para obtener las mesas más populares
def obtener_mesas_populares():
    """Devuelve las mesas más reservadas."""
    consulta = """
    SELECT mesa_id, COUNT(*) as total_reservas
    FROM reservas
    GROUP BY mesa_id
    ORDER BY total_reservas DESC
    """
    filas = obtener_todos(consulta)
    return [
        {"mesa_id": fila["mesa_id"], "total_reservas": fila["total_reservas"]}
        for fila in (filas or [])
    ]

# Función para obtener un resumen general de reservas
def obtener_resumen_general():
    """Devuelve un resumen general de reservas."""
    consulta = """
    SELECT
        COUNT(*) as total_reservas,
        SUM(CASE WHEN estado = 'cancelada' THEN 1 ELSE 0 END) as total_canceladas,
        SUM(CASE WHEN estado = 'completada' THEN 1 ELSE 0 END) as total_completadas,
        SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END) as total_pendientes,
        SUM(CASE WHEN estado = 'confirmada' THEN 1 ELSE 0 END) as total_confirmadas
    FROM reservas
    """
    fila = obtener_uno(consulta)
    if not fila:
        return {
            "total_reservas": 0,
            "total_canceladas": 0,
            "total_completadas": 0,
            "total_pendientes": 0,
            "total_confirmadas": 0,
        }
    return {
        "total_reservas": fila["total_reservas"],
        "total_canceladas": fila["total_canceladas"],
        "total_completadas": fila["total_completadas"],
        "total_pendientes": fila["total_pendientes"],
        "total_confirmadas": fila["total_confirmadas"],
    }
