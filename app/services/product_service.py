from app.repositories import product_repository
from app.models import Product

def _campo_vacio(valor):
    return not valor or not str(valor).strip()

def _es_numero_positivo(valor):
    try:
        return float(valor) > 0
    except (ValueError, TypeError):
        return False

def get_all_products():
    return product_repository.get_all_products()

def get_product(idProduct):
    return product_repository.get_product(idProduct)

def create_product(name, description, price, cost):
    if _campo_vacio(name):
        return False, "El nombre del producto no puede estar vacío."
    if not _es_numero_positivo(price):
        return False, "El precio debe ser un número mayor a cero."
    if not _es_numero_positivo(cost):
        return False, "El costo debe ser un número mayor a cero."
    if float(price) < float(cost):
        return False, "El precio no puede ser menor que el costo."

    product = Product(
        idProduct=None,
        Name=name.strip(),
        Description=description.strip() if description else "",
        Price=float(price),
        Cost=float(cost)
    )
    return product_repository.create_product(product)

def update_product(idProduct, name, description, price, cost):
    if not product_repository.get_product(idProduct):
        return False, "El producto no existe."

    if _campo_vacio(name):
        return False, "El nombre del producto no puede estar vacío."
    if not _es_numero_positivo(price):
        return False, "El precio debe ser un número mayor a cero."
    if not _es_numero_positivo(cost):
        return False, "El costo debe ser un número mayor a cero."
    if float(price) < float(cost):
        return False, "El precio no puede ser menor que el costo."

    product = Product(
        idProduct=idProduct,
        Name=name.strip(),
        Description=description.strip() if description else "",
        Price=float(price),
        Cost=float(cost)
    )
    return product_repository.update_product(product)

def delete_product(idProduct):
    if not product_repository.get_product(idProduct):
        return False, "El producto no existe."
    return product_repository.delete_product(idProduct)
