import sqlite3
from app.repositories.config_bd import obtener_conexion
from app.modelos import Inventario


def obtener_todo_inventario():
    """Devuelve todo el inventario con datos del producto y del almacen."""
    conn = obtener_conexion()
    filas = conn.execute("""
        SELECT
            i.id_producto,
            i.id_almacen,
            i.cantidad,
            p.nombre    AS nombre_producto,
            p.precio,
            p.costo,
            w.nombre    AS nombre_almacen,
            w.pais,
            w.ciudad
        FROM Inventario i
        JOIN Producto   p ON p.id_producto = i.id_producto
        JOIN Almacen    w ON w.id_almacen  = i.id_almacen
        ORDER BY p.nombre, w.nombre
    """).fetchall()
    conn.close()

    # Convertimos cada fila en un objeto Inventario
    lista = []
    for fila in filas:
        item = Inventario(
            id_producto=fila["id_producto"],
            id_almacen=fila["id_almacen"],
            cantidad=fila["cantidad"],
            nombre_producto=fila["nombre_producto"],
            nombre_almacen=fila["nombre_almacen"],
            precio=fila["precio"],
            costo=fila["costo"],
            pais=fila["pais"],
            ciudad=fila["ciudad"]
        )
        lista.append(item)
    return lista


def obtener_inventario_por_producto(id_producto):
    """Devuelve todos los registros de inventario de un producto especifico."""
    conn = obtener_conexion()
    filas = conn.execute("""
        SELECT i.*, w.nombre AS nombre_almacen, w.pais, w.ciudad
        FROM Inventario i
        JOIN Almacen w ON w.id_almacen = i.id_almacen
        WHERE i.id_producto = ?
    """, (id_producto,)).fetchall()
    conn.close()

    lista = []
    for fila in filas:
        item = Inventario(
            id_producto=fila["id_producto"],
            id_almacen=fila["id_almacen"],
            cantidad=fila["cantidad"],
            nombre_almacen=fila["nombre_almacen"],
            pais=fila["pais"],
            ciudad=fila["ciudad"]
        )
        lista.append(item)
    return lista


def obtener_inventario_por_almacen(id_almacen):
    """Devuelve todos los registros de inventario de un almacen especifico."""
    conn = obtener_conexion()
    filas = conn.execute("""
        SELECT i.*, p.nombre AS nombre_producto, p.precio, p.costo
        FROM Inventario i
        JOIN Producto p ON p.id_producto = i.id_producto
        WHERE i.id_almacen = ?
    """, (id_almacen,)).fetchall()
    conn.close()

    lista = []
    for fila in filas:
        item = Inventario(
            id_producto=fila["id_producto"],
            id_almacen=fila["id_almacen"],
            cantidad=fila["cantidad"],
            nombre_producto=fila["nombre_producto"],
            precio=fila["precio"],
            costo=fila["costo"]
        )
        lista.append(item)
    return lista


def crear_inventario(inventario):
    """Inserta un nuevo registro en el inventario."""
    conn = obtener_conexion()
    try:
        conn.execute(
            "INSERT INTO Inventario(id_producto, id_almacen, cantidad) VALUES(?,?,?)",
            (inventario.id_producto, inventario.id_almacen, inventario.cantidad)
        )
        conn.commit()
        return True, "Inventario creado."
    except sqlite3.IntegrityError:
        # Este error ocurre cuando el producto ya existe en ese almacen
        return False, "Ya existe ese producto en ese almacen."
    finally:
        conn.close()


def actualizar_stock_inventario(id_producto, id_almacen, cantidad):
    """Actualiza la cantidad de un producto en un almacen."""
    conn = obtener_conexion()
    conn.execute(
        "UPDATE Inventario SET cantidad=? WHERE id_producto=? AND id_almacen=?",
        (cantidad, id_producto, id_almacen)
    )
    conn.commit()
    conn.close()
    return True, "Cantidad actualizada."


def eliminar_inventario(id_producto, id_almacen):
    """Elimina un registro de inventario."""
    conn = obtener_conexion()
    conn.execute(
        "DELETE FROM Inventario WHERE id_producto=? AND id_almacen=?",
        (id_producto, id_almacen)
    )
    conn.commit()
    conn.close()
    return True, "Registro eliminado."
