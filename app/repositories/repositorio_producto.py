# repositorio_producto.py
# Se comunica directamente con la base de datos para operaciones de Producto (CRUD).

from app.repositories.config_bd import obtener_conexion
from app.modelos import Producto


def obtener_todos_productos():
    """Devuelve una lista con todos los productos guardados en la base de datos."""
    conn = obtener_conexion()
    filas = conn.execute("SELECT * FROM Producto ORDER BY nombre").fetchall()
    conn.close()

    # Convertimos cada fila de la base de datos en un objeto Producto
    lista = []
    for fila in filas:
        producto = Producto(
            id_producto=fila["id_producto"],
            nombre=fila["nombre"],
            descripcion=fila["descripcion"],
            precio=fila["precio"],
            costo=fila["costo"]
        )
        lista.append(producto)
    return lista


def obtener_producto(id_producto):
    """Busca un producto por su ID. Devuelve el producto o None si no existe."""
    conn = obtener_conexion()
    fila = conn.execute(
        "SELECT * FROM Producto WHERE id_producto=?", (id_producto,)
    ).fetchone()
    conn.close()

    if fila is None:
        return None

    return Producto(
        id_producto=fila["id_producto"],
        nombre=fila["nombre"],
        descripcion=fila["descripcion"],
        precio=fila["precio"],
        costo=fila["costo"]
    )


def crear_producto(producto):
    """Inserta un nuevo producto en la base de datos."""
    conn = obtener_conexion()
    cursor = conn.execute(
        "INSERT INTO Producto(nombre, descripcion, precio, costo) VALUES(?,?,?,?)",
        (producto.nombre, producto.descripcion, producto.precio, producto.costo)
    )
    conn.commit()
    conn.close()
    return True, "Producto creado.", cursor.lastrowid


def actualizar_producto(producto):
    """Actualiza los datos de un producto existente."""
    conn = obtener_conexion()
    conn.execute(
        "UPDATE Producto SET nombre=?, descripcion=?, precio=?, costo=? WHERE id_producto=?",
        (producto.nombre, producto.descripcion, producto.precio, producto.costo, producto.id_producto)
    )
    conn.commit()
    conn.close()
    return True, "Producto actualizado."


def eliminar_producto(id_producto):
    """Elimina un producto si no esta asignado a ningun almacen."""
    conn = obtener_conexion()

    # Verificamos si el producto esta en algun inventario
    fila = conn.execute(
        "SELECT COUNT(*) FROM Inventario WHERE id_producto=?", (id_producto,)
    ).fetchone()
    cantidad_en_uso = fila[0]

    if cantidad_en_uso > 0:
        conn.close()
        return False, "El producto esta asignado a uno o mas almacenes."

    conn.execute("DELETE FROM Producto WHERE id_producto=?", (id_producto,))
    conn.commit()
    conn.close()
    return True, "Producto eliminado."
