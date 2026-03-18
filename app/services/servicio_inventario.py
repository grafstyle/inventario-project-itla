from app.repositories import repositorio_inventario, repositorio_producto, repositorio_almacen
from app.modelos import Inventario

def _es_numero_no_negativo(valor):
    try:
        return float(valor) >= 0
    except (ValueError, TypeError):
        return False

def obtener_todo_inventario():
    return repositorio_inventario.obtener_todo_inventario()

def obtener_inventario_por_producto(id_producto):
    return repositorio_inventario.obtener_inventario_por_producto(id_producto)

def obtener_inventario_por_almacen(id_almacen):
    return repositorio_inventario.obtener_inventario_por_almacen(id_almacen)

def crear_inventario(id_producto, id_almacen, cantidad):
    if not repositorio_producto.obtener_producto(id_producto):
        return False, "El producto no existe."

    if not repositorio_almacen.obtener_almacen(id_almacen):
        return False, "El almacén no existe."

    if not _es_numero_no_negativo(cantidad):
        return False, "El stock no puede ser negativo."

    inventario = Inventario(
        id_producto=id_producto,
        id_almacen=id_almacen,
        cantidad=int(cantidad)
    )
    return repositorio_inventario.crear_inventario(inventario)

def actualizar_stock_inventario(id_producto, id_almacen, cantidad):
    if not _es_numero_no_negativo(cantidad):
        return False, "El stock no puede ser negativo."

    return repositorio_inventario.actualizar_stock_inventario(id_producto, id_almacen, int(cantidad))

def eliminar_inventario(id_producto, id_almacen):
    return repositorio_inventario.eliminar_inventario(id_producto, id_almacen)
