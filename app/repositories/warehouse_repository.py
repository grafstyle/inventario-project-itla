from app.repositories.db_config import get_conn
from app.models import Warehouse

def get_all_warehouses():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM Warehouse ORDER BY Name").fetchall()
    conn.close()
    return [Warehouse(**dict(r)) for r in rows]

def get_warehouse(idWarehouse):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM Warehouse WHERE idWarehouse=?", (idWarehouse,)
    ).fetchone()
    conn.close()
    return Warehouse(**dict(row)) if row else None

def create_warehouse(warehouse: Warehouse):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO Warehouse(Name, Country, City) VALUES(?,?,?)",
        (warehouse.Name, warehouse.Country, warehouse.City)
    )
    conn.commit()
    conn.close()
    return True, "Almacén creado.", cur.lastrowid

def update_warehouse(warehouse: Warehouse):
    conn = get_conn()
    conn.execute(
        "UPDATE Warehouse SET Name=?, Country=?, City=? WHERE idWarehouse=?",
        (warehouse.Name, warehouse.Country, warehouse.City, warehouse.idWarehouse)
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
