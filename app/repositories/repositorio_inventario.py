import sqlite3
from app.repositories.config_bd import obtener_conexion
from app.modelos import Inventario

def obtener_todo_inventario():
    conn = obtener_conexion()
    rows = conn.execute("""
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
        JOIN Producto   p ON p.id_producto   = i.id_producto
        JOIN Almacen w ON w.id_almacen = i.id_almacen
        ORDER BY p.nombre, w.nombre
    """).fetchall()
    conn.close()
    return [Inventario(**dict(r)) for r in rows]

def obtener_inventario_por_producto(id_producto):
    conn = obtener_conexion()
    rows = conn.execute("""
        SELECT i.*, w.nombre AS nombre_almacen, w.pais, w.ciudad
        FROM Inventario i
        JOIN Almacen w ON w.id_almacen = i.id_almacen
        WHERE i.id_producto = ?
    """, (id_producto,)).fetchall()
    conn.close()
    return [Inventario(**dict(r)) for r in rows]

def obtener_inventario_por_almacen(id_almacen):
    conn = obtener_conexion()
    rows = conn.execute("""
        SELECT i.*, p.nombre AS nombre_producto, p.precio, p.costo
        FROM Inventario i
        JOIN Producto p ON p.id_producto = i.id_producto
        WHERE i.id_almacen = ?
    """, (id_almacen,)).fetchall()
    conn.close()
    return [Inventario(**dict(r)) for r in rows]

def crear_inventario(inventario: Inventario):
    conn = obtener_conexion()
    try:
        conn.execute(
            "INSERT INTO Inventario(id_producto, id_almacen, cantidad) VALUES(?,?,?)",
            (inventario.id_producto, inventario.id_almacen, inventario.cantidad)
        )
        conn.commit()
        return True, "Inventario creado."
    except sqlite3.IntegrityError:
        return False, "Ya existe ese producto en ese almacén."
    finally:
        conn.close()

def actualizar_stock_inventario(id_producto, id_almacen, cantidad):
    conn = obtener_conexion()
    conn.execute(
        "UPDATE Inventario SET cantidad=? WHERE id_producto=? AND id_almacen=?",
        (cantidad, id_producto, id_almacen)
    )
    conn.commit()
    conn.close()
    return True, "Cantidad actualizada."

def eliminar_inventario(id_producto, id_almacen):
    conn = obtener_conexion()
    conn.execute(
        "DELETE FROM Inventario WHERE id_producto=? AND id_almacen=?",
        (id_producto, id_almacen)
    )
    conn.commit()
    conn.close()
    return True, "Registro eliminado."
