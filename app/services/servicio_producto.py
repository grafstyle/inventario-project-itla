# servicio_producto.py
# Esta capa valida los datos antes de guardarlos en la base de datos.
# Si los datos son correctos, llama al repositorio para hacer el trabajo real.

from app.repositories import repositorio_producto
from app.modelos import Producto


def obtener_todos_productos():
    """Devuelve la lista de todos los productos."""
    return repositorio_producto.obtener_todos_productos()


def obtener_producto(id_producto):
    """Devuelve un producto por su ID."""
    return repositorio_producto.obtener_producto(id_producto)


def crear_producto(nombre, descripcion, precio, costo):
    """
    Valida los datos y, si son correctos, crea un nuevo producto.
    Devuelve (True, mensaje, id) si fue exitoso, o (False, mensaje, None) si hubo un error.
    """
    # Validacion 1: el nombre no puede estar vacio
    if not nombre or nombre.strip() == "":
        return False, "El nombre del producto no puede estar vacio.", None

    # Validacion 2: el precio debe ser un numero valido
    try:
        precio = float(precio)
    except (ValueError, TypeError):
        return False, "El precio debe ser un numero valido.", None

    if precio <= 0:
        return False, "El precio debe ser mayor a cero.", None

    # Validacion 3: el costo debe ser un numero valido
    try:
        costo = float(costo)
    except (ValueError, TypeError):
        return False, "El costo debe ser un numero valido.", None

    if costo <= 0:
        return False, "El costo debe ser mayor a cero.", None

    # Validacion 4: el precio no puede ser menor que el costo
    if precio < costo:
        return False, "El precio no puede ser menor que el costo.", None

    # Creamos el objeto Producto con los datos validados
    producto = Producto(
        id_producto=None,
        nombre=nombre.strip(),
        descripcion=descripcion.strip() if descripcion else "",
        precio=precio,
        costo=costo
    )
    return repositorio_producto.crear_producto(producto)


def actualizar_producto(id_producto, nombre, descripcion, precio, costo):
    """
    Valida los datos y actualiza el producto indicado.
    Devuelve (True, mensaje) si fue exitoso, o (False, mensaje) si hubo un error.
    """
    # Verificamos que el producto exista
    if not repositorio_producto.obtener_producto(id_producto):
        return False, "El producto no existe."

    # Validacion 1: el nombre no puede estar vacio
    if not nombre or nombre.strip() == "":
        return False, "El nombre del producto no puede estar vacio."

    # Validacion 2: el precio debe ser un numero valido
    try:
        precio = float(precio)
    except (ValueError, TypeError):
        return False, "El precio debe ser un numero valido."

    if precio <= 0:
        return False, "El precio debe ser mayor a cero."

    # Validacion 3: el costo debe ser un numero valido
    try:
        costo = float(costo)
    except (ValueError, TypeError):
        return False, "El costo debe ser un numero valido."

    if costo <= 0:
        return False, "El costo debe ser mayor a cero."

    # Validacion 4: el precio no puede ser menor que el costo
    if precio < costo:
        return False, "El precio no puede ser menor que el costo."

    producto = Producto(
        id_producto=id_producto,
        nombre=nombre.strip(),
        descripcion=descripcion.strip() if descripcion else "",
        precio=precio,
        costo=costo
    )
    return repositorio_producto.actualizar_producto(producto)


def eliminar_producto(id_producto):
    """Elimina el producto indicado si existe."""
    if not repositorio_producto.obtener_producto(id_producto):
        return False, "El producto no existe."
    return repositorio_producto.eliminar_producto(id_producto)
