from app.repositories import repositorio_inventario, repositorio_producto, repositorio_almacen
from app.modelos import Inventario


def obtener_todo_inventario():
    """Devuelve todo el inventario."""
    return repositorio_inventario.obtener_todo_inventario()


def obtener_inventario_por_producto(id_producto):
    """Devuelve el inventario filtrado por producto."""
    return repositorio_inventario.obtener_inventario_por_producto(id_producto)


def obtener_inventario_por_almacen(id_almacen):
    """Devuelve el inventario filtrado por almacen."""
    return repositorio_inventario.obtener_inventario_por_almacen(id_almacen)


def crear_inventario(id_producto, id_almacen, cantidad):
    """
    Valida los datos y crea un nuevo registro de inventario.
    Devuelve (True, mensaje) si fue exitoso, o (False, mensaje) si hubo un error.
    """
    # Verificamos que el producto exista
    if not repositorio_producto.obtener_producto(id_producto):
        return False, "El producto no existe."

    # Verificamos que el almacen exista
    if not repositorio_almacen.obtener_almacen(id_almacen):
        return False, "El almacen no existe."

    # Validamos que la cantidad sea un numero no negativo
    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return False, "La cantidad debe ser un numero entero."

    if cantidad < 0:
        return False, "El stock no puede ser negativo."

    inventario = Inventario(
        id_producto=id_producto,
        id_almacen=id_almacen,
        cantidad=cantidad
    )
    return repositorio_inventario.crear_inventario(inventario)


def actualizar_stock_inventario(id_producto, id_almacen, cantidad):
    """
    Valida la cantidad y actualiza el stock de un registro de inventario.
    Devuelve (True, mensaje) si fue exitoso, o (False, mensaje) si hubo un error.
    """
    # Validamos que la cantidad sea un numero no negativo
    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return False, "La cantidad debe ser un numero entero."

    if cantidad < 0:
        return False, "El stock no puede ser negativo."

    return repositorio_inventario.actualizar_stock_inventario(id_producto, id_almacen, cantidad)


def eliminar_inventario(id_producto, id_almacen):
    """Elimina un registro de inventario."""
    return repositorio_inventario.eliminar_inventario(id_producto, id_almacen)
