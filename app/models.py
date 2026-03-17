from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    idProduct: Optional[int]
    Name: str
    Description: str
    Price: float
    Cost: float

@dataclass
class Warehouse:
    idWarehouse: Optional[int]
    Name: str
    Country: str
    City: str

@dataclass
class Inventory:
    idProduct: int
    idWarehouse: int
    Stock: int
    ProductName: Optional[str] = None
    WarehouseName: Optional[str] = None
    Price: Optional[float] = None
    Cost: Optional[float] = None
    Country: Optional[str] = None
    City: Optional[str] = None
