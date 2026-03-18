from app.repositories.config_bd import obtener_conexion
from app.modelos import Producto

def obtener_todos_productos():
    conn = obtener_conexion()
    rows = conn.execute("SELECT * FROM Producto ORDER BY nombre").fetchall()
    conn.close()
    return [Producto(**dict(r)) for r in rows]

def obtener_producto(id_producto):
    conn = obtener_conexion()
    row = conn.execute(
        "SELECT * FROM Producto WHERE id_producto=?", (id_producto,)
    ).fetchone()
    conn.close()
    return Producto(**dict(row)) if row else None

def crear_producto(producto: Producto):
    conn = obtener_conexion()
    cur = conn.execute(
        "INSERT INTO Producto(nombre, descripcion, precio, costo) VALUES(?,?,?,?)",
        (producto.nombre, producto.descripcion, producto.precio, producto.costo)
    )
    conn.commit()
    conn.close()
    return True, "Producto creado.", cur.lastrowid

def actualizar_producto(producto: Producto):
    conn = obtener_conexion()
    conn.execute(
        "UPDATE Producto SET nombre=?, descripcion=?, precio=?, costo=? WHERE id_producto=?",
        (producto.nombre, producto.descripcion, producto.precio, producto.costo, producto.id_producto)
    )
    conn.commit()
    conn.close()
    return True, "Producto actualizado."

def eliminar_producto(id_producto):
    conn = obtener_conexion()
    en_uso = conn.execute(
        "SELECT COUNT(*) FROM Inventario WHERE id_producto=?", (id_producto,)
    ).fetchone()[0]
    if en_uso > 0:
        conn.close()
        return False, "El producto está asignado a uno o más almacenes."
    conn.execute("DELETE FROM Producto WHERE id_producto=?", (id_producto,))
    conn.commit()
    conn.close()
    return True, "Producto eliminado."
