import sqlite3
import csv
import os

DB_PATH = "valencia_luz_persistente.db" # Mantenemos el mismo archivo de base de datos del proyecto

def inicializar_base_de_datos():
    print("🛰️ Iniciando modelado relacional de NODENA Bienestar...")
    
    # Si la base de datos ya existe, la borramos para garantizar mesa limpia
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Base de datos residual eliminada con éxito.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. CREACIÓN DE LA TABLA DE SERVICIOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id TEXT PRIMARY KEY,
            nombre TEXT,
            tipo TEXT,
            duracion_min INTEGER,
            precio REAL
        )
    """)

    # 2. CREACIÓN DE LA TABLA DE DISPONIBILIDAD
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disponibilidad (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recurso_id TEXT,
            recurso_nombre TEXT,
            dia_semana TEXT,
            hora_inicio TEXT,
            hora_fin TEXT,
            plazas_fijas INTEGER
        )
    """)

    # 3. CREACIÓN DE LA TABLA DE CITAS / RESERVAS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id TEXT PRIMARY KEY,
            fecha TEXT,
            hora_inicio TEXT,
            hora_fin TEXT,
            servicio_id TEXT,
            recurso_id TEXT,
            cliente_nombre TEXT,
            cliente_contacto TEXT,
            canal TEXT,
            estado TEXT,
            precio REAL,
            FOREIGN KEY (servicio_id) REFERENCES servicios(id)
        )
    """)
    conn.commit()

    # 4. INGESTIÓN AUTOMATIZADA DE SERVICIOS
    with open("Servicios.csv", mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            cursor.execute("""
                INSERT INTO servicios (id, nombre, tipo, duracion_min, precio)
                VALUES (?, ?, ?, ?, ?)
            """, (fila["ID"], fila["Nombre"], fila["Tipo"], int(fila["Duracion_min"]), float(fila["Precio"])))

    # 5. INGESTIÓN AUTOMATIZADA DE DISPONIBILIDAD
    with open("Disponibilidad.csv", mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            cursor.execute("""
                INSERT INTO disponibilidad (recurso_id, recurso_nombre, dia_semana, hora_inicio, hora_fin, plazas_fijas)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fila["RecursoID"], fila["RecursoNombre"], fila["DiaSemana"], fila["HoraInicio"], fila["HoraFin"], int(fila["PlazasFijas"])))

    # 6. INGESTIÓN AUTOMATIZADA DE CITAS
    with open("Citas_ejemplo.csv", mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            cursor.execute("""
                INSERT INTO citas (id, fecha, hora_inicio, hora_fin, servicio_id, recurso_id, cliente_nombre, cliente_contacto, canal, estado, precio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (fila["ID"], fila["Fecha"], fila["HoraInicio"], fila["HoraFin"], fila["ServicioID"], fila["RecursoID"], fila["ClienteNombre"], fila["ClienteContacto"], fila["Canal"], fila["Estado"], float(fila["Precio"])))

    conn.commit()
    conn.close()
    print("🔥 Inyección relacional masiva de NODENA Bienestar completada al 100% en Alemania.")

if __name__ == "__main__":
    inicializar_base_de_datos()
