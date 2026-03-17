from app.repositories.db_config import get_conn
from app.models import Product

def get_all_products():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM Product ORDER BY Name").fetchall()
    conn.close()
    return [Product(**dict(r)) for r in rows]

def get_product(idProduct):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM Product WHERE idProduct=?", (idProduct,)
    ).fetchone()
    conn.close()
    return Product(**dict(row)) if row else None

def create_product(product: Product):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO Product(Name, Description, Price, Cost) VALUES(?,?,?,?)",
        (product.Name, product.Description, product.Price, product.Cost)
    )
    conn.commit()
    conn.close()
    return True, "Producto creado.", cur.lastrowid

def update_product(product: Product):
    conn = get_conn()
    conn.execute(
        "UPDATE Product SET Name=?, Description=?, Price=?, Cost=? WHERE idProduct=?",
        (product.Name, product.Description, product.Price, product.Cost, product.idProduct)
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
