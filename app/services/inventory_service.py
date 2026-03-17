from app.repositories import inventory_repository, product_repository, warehouse_repository
from app.models import Inventory

def _es_numero_no_negativo(valor):
    try:
        return float(valor) >= 0
    except (ValueError, TypeError):
        return False

def get_all_inventory():
    return inventory_repository.get_all_inventory()

def get_inventory_by_product(idProduct):
    return inventory_repository.get_inventory_by_product(idProduct)

def get_inventory_by_warehouse(idWarehouse):
    return inventory_repository.get_inventory_by_warehouse(idWarehouse)

def create_inventory(idProduct, idWarehouse, stock):
    if not product_repository.get_product(idProduct):
        return False, "El producto no existe."

    if not warehouse_repository.get_warehouse(idWarehouse):
        return False, "El almacén no existe."

    if not _es_numero_no_negativo(stock):
        return False, "El stock no puede ser negativo."

    inventory = Inventory(
        idProduct=idProduct,
        idWarehouse=idWarehouse,
        Stock=int(stock)
    )
    return inventory_repository.create_inventory(inventory)

def update_inventory_stock(idProduct, idWarehouse, stock):
    if not _es_numero_no_negativo(stock):
        return False, "El stock no puede ser negativo."

    return inventory_repository.update_inventory_stock(idProduct, idWarehouse, int(stock))

def delete_inventory(idProduct, idWarehouse):
    return inventory_repository.delete_inventory(idProduct, idWarehouse)
