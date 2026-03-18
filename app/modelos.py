from dataclasses import dataclass
from typing import Optional

@dataclass
class Producto:
    id_producto: Optional[int]
    nombre: str
    descripcion: str
    precio: float
    costo: float

@dataclass
class Almacen:
    id_almacen: Optional[int]
    nombre: str
    pais: str
    ciudad: str

@dataclass
class Inventario:
    id_producto: int
    id_almacen: int
    cantidad: int
    nombre_producto: Optional[str] = None
    nombre_almacen: Optional[str] = None
    precio: Optional[float] = None
    costo: Optional[float] = None
    pais: Optional[str] = None
    ciudad: Optional[str] = None
