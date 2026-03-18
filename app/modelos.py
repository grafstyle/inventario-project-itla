# modelos.py
# Define las clases que representan los datos de la aplicacion.
# Cada clase es como una "plantilla" para guardar informacion.

class Producto:
    def __init__(self, id_producto, nombre, descripcion, precio, costo):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.costo = costo


class Almacen:
    def __init__(self, id_almacen, nombre, pais, ciudad):
        self.id_almacen = id_almacen
        self.nombre = nombre
        self.pais = pais
        self.ciudad = ciudad


class Inventario:
    def __init__(self, id_producto, id_almacen, cantidad,
                 nombre_producto=None, nombre_almacen=None,
                 precio=None, costo=None, pais=None, ciudad=None):
        self.id_producto = id_producto
        self.id_almacen = id_almacen
        self.cantidad = cantidad
        self.nombre_producto = nombre_producto
        self.nombre_almacen = nombre_almacen
        self.precio = precio
        self.costo = costo
        self.pais = pais
        self.ciudad = ciudad
