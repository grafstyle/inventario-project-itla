import sqlite3

DB_PATH = "inventario.db"


# ════════════════════════════════════════════
#  CONEXIÓN
# ════════════════════════════════════════════

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ════════════════════════════════════════════
#  CREAR TABLAS
# ════════════════════════════════════════════

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            idProduct   INTEGER PRIMARY KEY AUTOINCREMENT,
            Name        TEXT    NOT NULL,
            Description TEXT,
            Price       REAL    NOT NULL DEFAULT 0,
            Cost        REAL    NOT NULL DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Warehouse (
            idWarehouse INTEGER PRIMARY KEY AUTOINCREMENT,
            Name        TEXT    NOT NULL,
            Country     TEXT    NOT NULL,
            City        TEXT    NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Inventory (
            idProduct   INTEGER NOT NULL REFERENCES Product(idProduct),
            idWarehouse INTEGER NOT NULL REFERENCES Warehouse(idWarehouse),
            Stock       INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (idProduct, idWarehouse)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada.")


# ════════════════════════════════════════════
#  PRODUCT — CRUD
# ════════════════════════════════════════════
# CRUD = Create, Read, Update, Delete
def get_all_products():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM Product ORDER BY Name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_product(idProduct):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM Product WHERE idProduct=?", (idProduct,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def create_product(name, description, price, cost):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO Product(Name, Description, Price, Cost) VALUES(?,?,?,?)",
        (name, description, price, cost)
    )
    conn.commit()
    conn.close()
    return True, "Producto creado.", cur.lastrowid


def update_product(idProduct, name, description, price, cost):
    conn = get_conn()
    conn.execute(
        "UPDATE Product SET Name=?, Description=?, Price=?, Cost=? WHERE idProduct=?",
        (name, description, price, cost, idProduct)
    )
    conn.commit()
    conn.close()
    return True, "Producto actualizado."


def delete_product(idProduct):
    conn = get_conn()
    en_uso = conn.execute(
        "SELECT COUNT(*) FROM Inventory WHERE idProduct=?", (idProduct,)
    ).fetchone()[0]
    if en_uso > 0:
        conn.close()
        return False, "El producto está asignado a uno o más almacenes."
    conn.execute("DELETE FROM Product WHERE idProduct=?", (idProduct,))
    conn.commit()
    conn.close()
    return True, "Producto eliminado."


# ════════════════════════════════════════════
#  WAREHOUSE — CRUD
# ════════════════════════════════════════════

def get_all_warehouses():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM Warehouse ORDER BY Name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_warehouse(idWarehouse):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM Warehouse WHERE idWarehouse=?", (idWarehouse,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def create_warehouse(name, country, city):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO Warehouse(Name, Country, City) VALUES(?,?,?)",
        (name, country, city)
    )
    conn.commit()
    conn.close()
    return True, "Almacén creado.", cur.lastrowid


def update_warehouse(idWarehouse, name, country, city):
    conn = get_conn()
    conn.execute(
        "UPDATE Warehouse SET Name=?, Country=?, City=? WHERE idWarehouse=?",
        (name, country, city, idWarehouse)
    )
    conn.commit()
    conn.close()
    return True, "Almacén actualizado."


def delete_warehouse(idWarehouse):
    conn = get_conn()
    en_uso = conn.execute(
        "SELECT COUNT(*) FROM Inventory WHERE idWarehouse=?", (idWarehouse,)
    ).fetchone()[0]
    if en_uso > 0:
        conn.close()
        return False, "El almacén tiene productos asignados."
    conn.execute("DELETE FROM Warehouse WHERE idWarehouse=?", (idWarehouse,))
    conn.commit()
    conn.close()
    return True, "Almacén eliminado."


# ════════════════════════════════════════════
#  INVENTORY — CRUD
# ════════════════════════════════════════════

def get_all_inventory():
    conn = get_conn()
    rows = conn.execute("""
        SELECT
            i.idProduct,
            i.idWarehouse,
            i.Stock,
            p.Name    AS ProductName,
            p.Price,
            p.Cost,
            w.Name    AS WarehouseName,
            w.Country,
            w.City
        FROM Inventory i
        JOIN Product   p ON p.idProduct   = i.idProduct
        JOIN Warehouse w ON w.idWarehouse = i.idWarehouse
        ORDER BY p.Name, w.Name
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_inventory_by_product(idProduct):
    conn = get_conn()
    rows = conn.execute("""
        SELECT i.*, w.Name AS WarehouseName, w.Country, w.City
        FROM Inventory i
        JOIN Warehouse w ON w.idWarehouse = i.idWarehouse
        WHERE i.idProduct = ?
    """, (idProduct,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_inventory_by_warehouse(idWarehouse):
    conn = get_conn()
    rows = conn.execute("""
        SELECT i.*, p.Name AS ProductName, p.Price, p.Cost
        FROM Inventory i
        JOIN Product p ON p.idProduct = i.idProduct
        WHERE i.idWarehouse = ?
    """, (idWarehouse,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_inventory(idProduct, idWarehouse, stock):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO Inventory(idProduct, idWarehouse, Stock) VALUES(?,?,?)",
            (idProduct, idWarehouse, stock)
        )
        conn.commit()
        return True, "Inventario creado."
    except sqlite3.IntegrityError:
        return False, "Ya existe ese producto en ese almacén."
    finally:
        conn.close()


def update_inventory_stock(idProduct, idWarehouse, stock):
    conn = get_conn()
    conn.execute(
        "UPDATE Inventory SET Stock=? WHERE idProduct=? AND idWarehouse=?",
        (stock, idProduct, idWarehouse)
    )
    conn.commit()
    conn.close()
    return True, "Stock actualizado."


def delete_inventory(idProduct, idWarehouse):
    conn = get_conn()
    conn.execute(
        "DELETE FROM Inventory WHERE idProduct=? AND idWarehouse=?",
        (idProduct, idWarehouse)
    )
    conn.commit()
    conn.close()
    return True, "Registro eliminado."

"""
# ════════════════════════════════════════════
#  PRUEBA RÁPIDA
# ════════════════════════════════════════════

if __name__ == "__main__":
    import os

    init_db()

    create_product("Laptop HP", "Core i5 16GB RAM", 35000, 28000)
    create_product("Mouse Logitech", "Inalámbrico", 1200, 800)

    create_warehouse("Almacén Central", "República Dominicana", "Santiago")
    create_warehouse("Sucursal Norte",  "República Dominicana", "Puerto Plata")

    create_inventory(1, 1, 20)
    create_inventory(1, 2, 10)
    create_inventory(2, 1, 50)

    print("\n📦 Inventario completo:")
    for row in get_all_inventory():
        print(f"  {row['ProductName']} | {row['WarehouseName']} | Stock: {row['Stock']}")

    print("\n🏭 Productos en Almacén Central:")
    for row in get_inventory_by_warehouse(1):
        print(f"  {row['ProductName']} — Stock: {row['Stock']}")

    update_inventory_stock(1, 1, 25)
    print(f"\n✏️  Stock actualizado: {get_inventory_by_product(1)[0]['Stock']} unidades")

    ok, msg = delete_product(1)
    print(f"\n🛡  Protección al eliminar: {msg}")

    ok, msg = delete_warehouse(1)
    print(f"🛡  Protección al eliminar almacén: {msg}")

#    os.remove("inventario.db")
    print("\n✅ Todas las pruebas pasaron.")
"""    
