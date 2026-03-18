from app.repositories.config_bd import obtener_conexion
from app.modelos import Almacen

def obtener_todos_almacenes():
    conn = obtener_conexion()
    rows = conn.execute("SELECT * FROM Almacen ORDER BY nombre").fetchall()
    conn.close()
    return [Almacen(**dict(r)) for r in rows]

def obtener_almacen(id_almacen):
    conn = obtener_conexion()
    row = conn.execute(
        "SELECT * FROM Almacen WHERE id_almacen=?", (id_almacen,)
    ).fetchone()
    conn.close()
    return Almacen(**dict(row)) if row else None

def crear_almacen(almacen: Almacen):
    conn = obtener_conexion()
    cur = conn.execute(
        "INSERT INTO Almacen(nombre, pais, ciudad) VALUES(?,?,?)",
        (almacen.nombre, almacen.pais, almacen.ciudad)
    )
    conn.commit()
    conn.close()
    return True, "Almacén creado.", cur.lastrowid

def actualizar_almacen(almacen: Almacen):
    conn = obtener_conexion()
    conn.execute(
        "UPDATE Almacen SET nombre=?, pais=?, ciudad=? WHERE id_almacen=?",
        (almacen.nombre, almacen.pais, almacen.ciudad, almacen.id_almacen)
    )
    conn.commit()
    conn.close()
    return True, "Almacén actualizado."

def eliminar_almacen(id_almacen):
    conn = obtener_conexion()
    en_uso = conn.execute(
        "SELECT COUNT(*) FROM Inventario WHERE id_almacen=?", (id_almacen,)
    ).fetchone()[0]
    if en_uso > 0:
        conn.close()
        return False, "El almacén tiene productos asignados."
    conn.execute("DELETE FROM Almacen WHERE id_almacen=?", (id_almacen,))
    conn.commit()
    conn.close()
    return True, "Almacén eliminado."
