import sqlite3

# esta funcion es para obtener un solo resultado de la base de datos, por ejemplo, un cliente por su email
def obtener_uno(consulta, parametros=()):
    """
    Ejecuta una consulta SQL y devuelve una sola fila.
    Si no hay resultados, devuelve None.
    """
    conexion = sqlite3.connect("data/restaurante.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    cursor.execute(consulta, parametros)
    resultado = cursor.fetchone()

    conexion.close()
    if resultado is None:
        return None
    return dict(resultado)

# esta funcion es para obtener muchos resultados de la base de datos, por ejemplo, todas las reservas de un cliente
def obtener_todos(consulta, parametros=()):
    """
    Ejecuta una consulta SQL y devuelve muchas filas.
    Si no hay resultados, devuelve None.
    """
    conexion = sqlite3.connect("data/restaurante.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    cursor.execute(consulta, parametros)
    resultado = cursor.fetchall()

    conexion.close()
    return [dict(fila) for fila in resultado]

# esta funcion es para ejecutar una consulta SQL que no devuelve resultados, por ejemplo, para insertar un nuevo cliente o actualizar una reserva
def ejecutar_consulta(consulta, parametros=()):
    """
    Ejecuta una consulta SQL que no devuelve resultados (INSERT, UPDATE, DELETE). 
    """
    conexion = sqlite3.connect("data/restaurante.db")
    cursor = conexion.cursor()

    cursor.execute(consulta, parametros)
    conexion.commit()  # Guardar cambios en la base de datos
    conexion.close()
