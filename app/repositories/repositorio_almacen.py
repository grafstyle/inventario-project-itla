# repositorio_almacen.py
# Se comunica directamente con la base de datos para operaciones de Almacen (CRUD).

from app.repositories.config_bd import obtener_conexion
from app.modelos import Almacen


def obtener_todos_almacenes():
    """Devuelve una lista con todos los almacenes guardados en la base de datos."""
    conn = obtener_conexion()
    filas = conn.execute("SELECT * FROM Almacen ORDER BY nombre").fetchall()
    conn.close()

    # Convertimos cada fila de la base de datos en un objeto Almacen
    lista = []
    for fila in filas:
        almacen = Almacen(
            id_almacen=fila["id_almacen"],
            nombre=fila["nombre"],
            pais=fila["pais"],
            ciudad=fila["ciudad"]
        )
        lista.append(almacen)
    return lista


def obtener_almacen(id_almacen):
    """Busca un almacen por su ID. Devuelve el almacen o None si no existe."""
    conn = obtener_conexion()
    fila = conn.execute(
        "SELECT * FROM Almacen WHERE id_almacen=?", (id_almacen,)
    ).fetchone()
    conn.close()

    if fila is None:
        return None

    return Almacen(
        id_almacen=fila["id_almacen"],
        nombre=fila["nombre"],
        pais=fila["pais"],
        ciudad=fila["ciudad"]
    )


def crear_almacen(almacen):
    """Inserta un nuevo almacen en la base de datos."""
    conn = obtener_conexion()
    cursor = conn.execute(
        "INSERT INTO Almacen(nombre, pais, ciudad) VALUES(?,?,?)",
        (almacen.nombre, almacen.pais, almacen.ciudad)
    )
    conn.commit()
    conn.close()
    return True, "Almacen creado.", cursor.lastrowid


def actualizar_almacen(almacen):
    """Actualiza los datos de un almacen existente."""
    conn = obtener_conexion()
    conn.execute(
        "UPDATE Almacen SET nombre=?, pais=?, ciudad=? WHERE id_almacen=?",
        (almacen.nombre, almacen.pais, almacen.ciudad, almacen.id_almacen)
    )
    conn.commit()
    conn.close()
    return True, "Almacen actualizado."


def eliminar_almacen(id_almacen):
    """Elimina un almacen si no tiene productos asignados."""
    conn = obtener_conexion()

    # Verificamos si el almacen tiene productos en inventario
    fila = conn.execute(
        "SELECT COUNT(*) FROM Inventario WHERE id_almacen=?", (id_almacen,)
    ).fetchone()
    cantidad_en_uso = fila[0]

    if cantidad_en_uso > 0:
        conn.close()
        return False, "El almacen tiene productos asignados."

    conn.execute("DELETE FROM Almacen WHERE id_almacen=?", (id_almacen,))
    conn.commit()
    conn.close()
    return True, "Almacen eliminado."
