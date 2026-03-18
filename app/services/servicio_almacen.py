from app.repositories import repositorio_almacen
from app.modelos import Almacen


def obtener_todos_almacenes():
    """Devuelve la lista de todos los almacenes."""
    return repositorio_almacen.obtener_todos_almacenes()


def obtener_almacen(id_almacen):
    """Devuelve un almacen por su ID."""
    return repositorio_almacen.obtener_almacen(id_almacen)


def crear_almacen(nombre, pais, ciudad):
    """
    Valida los datos y crea un nuevo almacen.
    Devuelve (True, mensaje, id) si fue exitoso, o (False, mensaje, None) si hubo un error.
    """
    # Validacion 1: el nombre no puede estar vacio
    if not nombre or nombre.strip() == "":
        return False, "El nombre del almacen no puede estar vacio.", None

    # Validacion 2: el pais no puede estar vacio
    if not pais or pais.strip() == "":
        return False, "El pais no puede estar vacio.", None

    # Validacion 3: la ciudad no puede estar vacia
    if not ciudad or ciudad.strip() == "":
        return False, "La ciudad no puede estar vacia.", None

    almacen = Almacen(
        id_almacen=None,
        nombre=nombre.strip(),
        pais=pais.strip(),
        ciudad=ciudad.strip()
    )
    return repositorio_almacen.crear_almacen(almacen)


def actualizar_almacen(id_almacen, nombre, pais, ciudad):
    """
    Valida los datos y actualiza el almacen indicado.
    Devuelve (True, mensaje) si fue exitoso, o (False, mensaje) si hubo un error.
    """
    # Verificamos que el almacen exista
    if not repositorio_almacen.obtener_almacen(id_almacen):
        return False, "El almacen no existe."

    # Validacion 1: el nombre no puede estar vacio
    if not nombre or nombre.strip() == "":
        return False, "El nombre del almacen no puede estar vacio."

    # Validacion 2: el pais no puede estar vacio
    if not pais or pais.strip() == "":
        return False, "El pais no puede estar vacio."

    # Validacion 3: la ciudad no puede estar vacia
    if not ciudad or ciudad.strip() == "":
        return False, "La ciudad no puede estar vacia."

    almacen = Almacen(
        id_almacen=id_almacen,
        nombre=nombre.strip(),
        pais=pais.strip(),
        ciudad=ciudad.strip()
    )
    return repositorio_almacen.actualizar_almacen(almacen)


def eliminar_almacen(id_almacen):
    """Elimina el almacen indicado si existe."""
    if not repositorio_almacen.obtener_almacen(id_almacen):
        return False, "El almacen no existe."
    return repositorio_almacen.eliminar_almacen(id_almacen)
