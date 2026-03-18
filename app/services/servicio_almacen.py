from app.repositories import repositorio_almacen
from app.modelos import Almacen

def _campo_vacio(valor):
    return not valor or not str(valor).strip()

def obtener_todos_almacenes():
    return repositorio_almacen.obtener_todos_almacenes()

def obtener_almacen(id_almacen):
    return repositorio_almacen.obtener_almacen(id_almacen)

def crear_almacen(nombre, pais, ciudad):
    if _campo_vacio(nombre):
        return False, "El nombre del almacén no puede estar vacío."
    if _campo_vacio(pais):
        return False, "El país no puede estar vacío."
    if _campo_vacio(ciudad):
        return False, "La ciudad no puede estar vacía."

    almacen = Almacen(
        id_almacen=None,
        nombre=nombre.strip(),
        pais=pais.strip(),
        ciudad=ciudad.strip()
    )
    return repositorio_almacen.crear_almacen(almacen)


def actualizar_almacen(id_almacen, nombre, pais, ciudad):
    if not repositorio_almacen.obtener_almacen(id_almacen):
        return False, "El almacén no existe."

    if _campo_vacio(nombre):
        return False, "El nombre del almacén no puede estar vacío."
    if _campo_vacio(pais):
        return False, "El país no puede estar vacío."
    if _campo_vacio(ciudad):
        return False, "La ciudad no puede estar vacía."

    almacen = Almacen(
        id_almacen=id_almacen,
        nombre=nombre.strip(),
        pais=pais.strip(),
        ciudad=ciudad.strip()
    )
    return repositorio_almacen.actualizar_almacen(almacen)

def eliminar_almacen(id_almacen):
    if not repositorio_almacen.obtener_almacen(id_almacen):
        return False, "El almacén no existe."
    return repositorio_almacen.eliminar_almacen(id_almacen)
