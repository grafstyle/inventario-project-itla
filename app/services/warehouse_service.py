from app.repositories import warehouse_repository
from app.models import Warehouse

def _campo_vacio(valor):
    return not valor or not str(valor).strip()

def get_all_warehouses():
    return warehouse_repository.get_all_warehouses()

def get_warehouse(idWarehouse):
    return warehouse_repository.get_warehouse(idWarehouse)

def create_warehouse(name, country, city):
    if _campo_vacio(name):
        return False, "El nombre del almacén no puede estar vacío."
    if _campo_vacio(country):
        return False, "El país no puede estar vacío."
    if _campo_vacio(city):
        return False, "La ciudad no puede estar vacía."

    warehouse = Warehouse(
        idWarehouse=None,
        Name=name.strip(),
        Country=country.strip(),
        City=city.strip()
    )
    return warehouse_repository.create_warehouse(warehouse)


def update_warehouse(idWarehouse, name, country, city):
    if not warehouse_repository.get_warehouse(idWarehouse):
        return False, "El almacén no existe."

    if _campo_vacio(name):
        return False, "El nombre del almacén no puede estar vacío."
    if _campo_vacio(country):
        return False, "El país no puede estar vacío."
    if _campo_vacio(city):
        return False, "La ciudad no puede estar vacía."

    warehouse = Warehouse(
        idWarehouse=idWarehouse,
        Name=name.strip(),
        Country=country.strip(),
        City=city.strip()
    )
    return warehouse_repository.update_warehouse(warehouse)

def delete_warehouse(idWarehouse):
    if not warehouse_repository.get_warehouse(idWarehouse):
        return False, "El almacén no existe."
    return warehouse_repository.delete_warehouse(idWarehouse)
