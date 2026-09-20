FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias base del sistema
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos e instalar / usaremos pandas/numpy para procesar analítica de los CSV)
RUN pip install --no-cache-dir fastapi uvicorn pydantic

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
