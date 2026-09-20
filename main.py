from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI(
    title="Nodena Bienestar API CORE",
    description="Backend asíncrono e inmutable conectado a la base de datos relacional SQLite3"
)

DB_PATH = "valencia_luz_persistente.db"

# ESTRUCTURA DE VALIDACIÓN DE DATOS (PYDANTIC) PARA NUEVAS RESERVAS
class RequestReserva(BaseModel):
    nombre: str
    telefono: str
    fecha: str  # Formato YYYY-MM-DD
    servicio_id: str

# 1. ENDPOINT GET: Recuperar el catálogo maestro de servicios desde la base de datos
@app.get("/api/v1/servicios")
def obtener_servicios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nombre, tipo, duracion_min, precio FROM servicios")
        filas = cursor.fetchall()
        
        # Mapeamos la tupla SQL a una estructura JSON limpia y legible
        servicios = []
        for f in filas:
            servicios.append({
                "id": f[0],
                "nombre": f[1],
                "tipo": f[2],
                "duracion_min": f[3],
                "precio": f[4]
            })
        return servicios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo en la base de datos: {str(e)}")
    finally:
        conn.close()

# 2. ENDPOINT POST: Capturar y registrar una nueva reserva en la tabla de citas
@app.post("/api/v1/reservar")
def crear_reserva(data: RequestReserva):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Generar un ID de cita secuencial básico para la prueba técnica
        cursor.execute("SELECT COUNT(*) FROM citas")
        conteo = cursor.fetchone()[0]
        nueva_cita_id = f"C{str(conteo + 1).zfill(3)}"
        
        # Consultar detalles básicos del servicio para la inyección (Precio y Recurso base)
        cursor.execute("SELECT precio, id FROM servicios WHERE id = ?", (data.servicio_id,))
        servicio = cursor.fetchone()
        if not servicio:
            raise HTTPException(status_code=44, detail="El ID del servicio proporcionado no existe.")
        
        precio_servicio = servicio[0]
        
        # Asignar recurso por defecto según el tipo de servicio (Física de tus CSV)
        recurso_id = "SALA_CLASES" if data.servicio_id in ["S01", "S02", "S03"] else "CAMILLA_1"
        
        # Inserción limpia en la tabla de citas relacionales
        cursor.execute("""
            INSERT INTO citas (id, fecha, hora_inicio, hora_fin, servicio_id, recurso_id, cliente_nombre, cliente_contacto, canal, estado, precio)
            VALUES (?, ?, '10:00', '11:00', ?, ?, ?, ?, 'web', 'Confirmada', ?)
        """, (nueva_cita_id, data.fecha, data.servicio_id, recurso_id, data.nombre, data.telefono, precio_servicio))
        
        conn.commit()
        return {"status": "success", "message": "Reserva asentada con éxito", "cita_id": nueva_cita_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Fallo en el asentamiento: {str(e)}")
    finally:
        conn.close()

# 3. INTERFAZ FRONTEND: Servir el HTML estático de la app de forma transparente
@app.get("/")
def servir_frontend():
    return FileResponse(os.path.join("static", "index.html"))

# Montar los archivos estáticos adicionales si fuesen necesarios (CSS, JS secundarios)
app.mount("/static", StaticFiles(directory="static"), name="static")

