import database as db

# ════════════════════════════════════════════
#  LOGIC.PY
#  Capa intermedia entre la interfaz
#  y la base de datos (database.py).
#  Su trabajo: validar datos y aplicar
#  las reglas del negocio antes de guardar.
#
#  Flujo:
#  flask → logic.py → database.py → SQLite
# ════════════════════════════════════════════


# ════════════════════════════════════════════
#  HELPERS — funciones de validación general
# ════════════════════════════════════════════

def _campo_vacio(valor):
    """Retorna True si el valor está vacío o solo tiene espacios."""
    return not valor or not str(valor).strip()


def _es_numero_positivo(valor):
    """Retorna True si el valor es un número mayor a cero."""
    try:
        return float(valor) > 0
    except (ValueError, TypeError):
        return False


def _es_numero_no_negativo(valor):
    """Retorna True si el valor es un número mayor o igual a cero."""
    try:
        return float(valor) >= 0
    except (ValueError, TypeError):
        return False


# ════════════════════════════════════════════
#  PRODUCT — lógica y validaciones
# ════════════════════════════════════════════

def logic_get_all_products():
    """Obtiene todos los productos de la base de datos."""
    return db.get_all_products()


def logic_get_product(idProduct):
    """Obtiene un producto por su ID."""
    return db.get_product(idProduct)


def logic_create_product(name, description, price, cost):
    """
    Valida y crea un nuevo producto.
    Reglas:
      - Nombre no puede estar vacío
      - Precio debe ser mayor a cero
      - Costo debe ser mayor a cero
      - Precio no puede ser menor que el costo
    """
    # Validar nombre
    if _campo_vacio(name):
        return False, "El nombre del producto no puede estar vacío."

    # Validar precio
    if not _es_numero_positivo(price):
        return False, "El precio debe ser un número mayor a cero."

    # Validar costo
    if not _es_numero_positivo(cost):
        return False, "El costo debe ser un número mayor a cero."

    # Validar que el precio no sea menor que el costo
    if float(price) < float(cost):
        return False, "El precio no puede ser menor que el costo."

    # Todo válido — guardar en la base de datos
    ok, msg, idProduct = db.create_product(
        name.strip(),
        description.strip() if description else "",
        float(price),
        float(cost)
    )
    return ok, msg


def logic_update_product(idProduct, name, description, price, cost):
    """
    Valida y actualiza un producto existente.
    Aplica las mismas reglas que logic_create_product.
    """
    # Verificar que el producto existe
    if not db.get_product(idProduct):
        return False, "El producto no existe."

    # Validar nombre
    if _campo_vacio(name):
        return False, "El nombre del producto no puede estar vacío."

    # Validar precio
    if not _es_numero_positivo(price):
        return False, "El precio debe ser un número mayor a cero."

    # Validar costo
    if not _es_numero_positivo(cost):
        return False, "El costo debe ser un número mayor a cero."

    # Validar que el precio no sea menor que el costo
    if float(price) < float(cost):
        return False, "El precio no puede ser menor que el costo."

    # Todo válido — actualizar en la base de datos
    return db.update_product(
        idProduct,
        name.strip(),
        description.strip() if description else "",
        float(price),
        float(cost)
    )


def logic_delete_product(idProduct):
    """
    Elimina un producto.
    La base de datos ya protege contra eliminar
    productos que estén en Inventory.
    """
    # Verificar que el producto existe
    if not db.get_product(idProduct):
        return False, "El producto no existe."

    return db.delete_product(idProduct)


# ════════════════════════════════════════════
#  WAREHOUSE — lógica y validaciones
# ════════════════════════════════════════════

def logic_get_all_warehouses():
    """Obtiene todos los almacenes de la base de datos."""
    return db.get_all_warehouses()


def logic_get_warehouse(idWarehouse):
    """Obtiene un almacén por su ID."""
    return db.get_warehouse(idWarehouse)


def logic_create_warehouse(name, country, city):
    """
    Valida y crea un nuevo almacén.
    Reglas:
      - Nombre no puede estar vacío
      - País no puede estar vacío
      - Ciudad no puede estar vacía
    """
    # Validar nombre
    if _campo_vacio(name):
        return False, "El nombre del almacén no puede estar vacío."

    # Validar país
    if _campo_vacio(country):
        return False, "El país no puede estar vacío."

    # Validar ciudad
    if _campo_vacio(city):
        return False, "La ciudad no puede estar vacía."

    # Todo válido — guardar en la base de datos
    ok, msg, idWarehouse = db.create_warehouse(
        name.strip(),
        country.strip(),
        city.strip()
    )
    return ok, msg


def logic_update_warehouse(idWarehouse, name, country, city):
    """
    Valida y actualiza un almacén existente.
    Aplica las mismas reglas que logic_create_warehouse.
    """
    # Verificar que el almacén existe
    if not db.get_warehouse(idWarehouse):
        return False, "El almacén no existe."

    # Validar nombre
    if _campo_vacio(name):
        return False, "El nombre del almacén no puede estar vacío."

    # Validar país
    if _campo_vacio(country):
        return False, "El país no puede estar vacío."

    # Validar ciudad
    if _campo_vacio(city):
        return False, "La ciudad no puede estar vacía."

    # Todo válido — actualizar en la base de datos
    return db.update_warehouse(
        idWarehouse,
        name.strip(),
        country.strip(),
        city.strip()
    )


def logic_delete_warehouse(idWarehouse):
    """
    Elimina un almacén.
    La base de datos ya protege contra eliminar
    almacenes que tengan productos asignados.
    """
    # Verificar que el almacén existe
    if not db.get_warehouse(idWarehouse):
        return False, "El almacén no existe."

    return db.delete_warehouse(idWarehouse)


# ════════════════════════════════════════════
#  INVENTORY — lógica y validaciones
# ════════════════════════════════════════════

def logic_get_all_inventory():
    """Obtiene todo el inventario con datos de producto y almacén."""
    return db.get_all_inventory()


def logic_get_inventory_by_product(idProduct):
    """Obtiene el inventario filtrado por producto."""
    return db.get_inventory_by_product(idProduct)


def logic_get_inventory_by_warehouse(idWarehouse):
    """Obtiene el inventario filtrado por almacén."""
    return db.get_inventory_by_warehouse(idWarehouse)


def logic_create_inventory(idProduct, idWarehouse, stock):
    """
    Valida y crea un registro de inventario.
    Reglas:
      - El producto debe existir
      - El almacén debe existir
      - El stock no puede ser negativo
    """
    # Verificar que el producto existe
    if not db.get_product(idProduct):
        return False, "El producto no existe."

    # Verificar que el almacén existe
    if not db.get_warehouse(idWarehouse):
        return False, "El almacén no existe."

    # Validar stock
    if not _es_numero_no_negativo(stock):
        return False, "El stock no puede ser negativo."

    # Todo válido — guardar en la base de datos
    return db.create_inventory(idProduct, idWarehouse, int(stock))


def logic_update_inventory_stock(idProduct, idWarehouse, stock):
    """
    Valida y actualiza el stock de un producto en un almacén.
    Reglas:
      - El stock no puede ser negativo
    """
    # Validar stock
    if not _es_numero_no_negativo(stock):
        return False, "El stock no puede ser negativo."

    # Todo válido — actualizar en la base de datos
    return db.update_inventory_stock(idProduct, idWarehouse, int(stock))


def logic_delete_inventory(idProduct, idWarehouse):
    """Elimina un registro de inventario."""
    return db.delete_inventory(idProduct, idWarehouse)

"""
# ════════════════════════════════════════════
#  PRUEBA RÁPIDA
# ════════════════════════════════════════════

if __name__ == "__main__":
    import os

    # Inicializar base de datos
    db.init_db()

    print("── Pruebas Product ──────────────────────")

    # Nombre vacío
    ok, msg = logic_create_product("", "", 100, 50)
    print(f"Nombre vacío: {msg}")

    # Precio menor que costo
    ok, msg = logic_create_product("Laptop", "Desc", 100, 500)
    print(f"Precio < Costo: {msg}")

    # Precio negativo
    ok, msg = logic_create_product("Laptop", "Desc", -100, 50)
    print(f"Precio negativo: {msg}")

    # Producto válido
    ok, msg = logic_create_product("Laptop HP", "Core i5", 35000, 28000)
    print(f"Producto válido: {msg}")

    print("\n── Pruebas Warehouse ────────────────────")

    # Campo vacío
    ok, msg = logic_create_warehouse("", "RD", "Santiago")
    print(f"Nombre vacío: {msg}")

    # Almacén válido
    ok, msg = logic_create_warehouse("Almacén Central", "República Dominicana", "Santiago")
    print(f"Almacén válido: {msg}")

    print("\n── Pruebas Inventory ────────────────────")

    # Stock negativo
    ok, msg = logic_create_inventory(1, 1, -10)
    print(f"Stock negativo: {msg}")

    # Producto no existe
    ok, msg = logic_create_inventory(999, 1, 10)
    print(f"Producto no existe: {msg}")

    # Inventario válido
    ok, msg = logic_create_inventory(1, 1, 20)
    print(f"Inventario válido: {msg}")

    # Duplicado
    ok, msg = logic_create_inventory(1, 1, 20)
    print(f"Duplicado: {msg}")

    print("\n── Inventario completo ──────────────────")
    for row in logic_get_all_inventory():
        print(f"  {row['ProductName']} | {row['WarehouseName']} | Stock: {row['Stock']}")

#     os.remove("inventario.db")
#     print("\n✅ Todas las pruebas pasaron.")
"""