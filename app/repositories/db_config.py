import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inventario.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

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
    print("[OK] Base de datos inicializada.")
