# config_bd.py
# Este archivo se encarga de conectar con la base de datos SQLite.

import sqlite3
import os

# Ruta al archivo de la base de datos
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inventario.db")


def obtener_conexion():
    """Abre y devuelve una conexion a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # permite acceder a las columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_bd():
    """Crea las tablas de la base de datos si aun no existen."""
    conn = obtener_conexion()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS Producto (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre       TEXT    NOT NULL,
            descripcion  TEXT,
            precio       REAL    NOT NULL DEFAULT 0,
            costo        REAL    NOT NULL DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Almacen (
            id_almacen  INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre       TEXT    NOT NULL,
            pais         TEXT    NOT NULL,
            ciudad       TEXT    NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Inventario (
            id_producto  INTEGER NOT NULL REFERENCES Producto(id_producto),
            id_almacen   INTEGER NOT NULL REFERENCES Almacen(id_almacen),
            cantidad     INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (id_producto, id_almacen)
        )
    """)

    conn.commit()
    conn.close()
    print("[OK] Base de datos inicializada.")
