from app.repositories import repositorio_producto
from app.modelos import Producto

def _campo_vacio(valor):
    return not valor or not str(valor).strip()

def _es_numero_positivo(valor):
    try:
        return float(valor) > 0
    except (ValueError, TypeError):
        return False

def obtener_todos_productos():
    return repositorio_producto.obtener_todos_productos()

def obtener_producto(id_producto):
    return repositorio_producto.obtener_producto(id_producto)

def crear_producto(nombre, descripcion, precio, costo):
    if _campo_vacio(nombre):
        return False, "El nombre del producto no puede estar vacío."
    if not _es_numero_positivo(precio):
        return False, "El precio debe ser un número mayor a cero."
    if not _es_numero_positivo(costo):
        return False, "El costo debe ser un número mayor a cero."
    if float(precio) < float(costo):
        return False, "El precio no puede ser menor que el costo."

    producto = Producto(
        id_producto=None,
        nombre=nombre.strip(),
        descripcion=descripcion.strip() if descripcion else "",
        precio=float(precio),
        costo=float(costo)
    )
    return repositorio_producto.crear_producto(producto)

def actualizar_producto(id_producto, nombre, descripcion, precio, costo):
    if not repositorio_producto.obtener_producto(id_producto):
        return False, "El producto no existe."

    if _campo_vacio(nombre):
        return False, "El nombre del producto no puede estar vacío."
    if not _es_numero_positivo(precio):
        return False, "El precio debe ser un número mayor a cero."
    if not _es_numero_positivo(costo):
        return False, "El costo debe ser un número mayor a cero."
    if float(precio) < float(costo):
        return False, "El precio no puede ser menor que el costo."

    producto = Producto(
        id_producto=id_producto,
        nombre=nombre.strip(),
        descripcion=descripcion.strip() if descripcion else "",
        precio=float(precio),
        costo=float(costo)
    )
    return repositorio_producto.actualizar_producto(producto)

def eliminar_producto(id_producto):
    if not repositorio_producto.obtener_producto(id_producto):
        return False, "El producto no existe."
    return repositorio_producto.eliminar_producto(id_producto)
