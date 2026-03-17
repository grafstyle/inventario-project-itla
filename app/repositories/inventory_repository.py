import sqlite3
from app.repositories.db_config import get_conn
from app.models import Inventory

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
    return [Inventory(**dict(r)) for r in rows]

def get_inventory_by_product(idProduct):
    conn = get_conn()
    rows = conn.execute("""
        SELECT i.*, w.Name AS WarehouseName, w.Country, w.City
        FROM Inventory i
        JOIN Warehouse w ON w.idWarehouse = i.idWarehouse
        WHERE i.idProduct = ?
    """, (idProduct,)).fetchall()
    conn.close()
    return [Inventory(**dict(r)) for r in rows]

def get_inventory_by_warehouse(idWarehouse):
    conn = get_conn()
    rows = conn.execute("""
        SELECT i.*, p.Name AS ProductName, p.Price, p.Cost
        FROM Inventory i
        JOIN Product p ON p.idProduct = i.idProduct
        WHERE i.idWarehouse = ?
    """, (idWarehouse,)).fetchall()
    conn.close()
    return [Inventory(**dict(r)) for r in rows]


def create_inventory(inventory: Inventory):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO Inventory(idProduct, idWarehouse, Stock) VALUES(?,?,?)",
            (inventory.idProduct, inventory.idWarehouse, inventory.Stock)
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
