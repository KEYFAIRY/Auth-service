# Imagen base
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para mysqlclient y compilar
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY firebase_account.json ./credentials/firebase_account.json

# Variables de entorno para FastAPI
ENV PYTHONUNBUFFERED=1

# Puerto por defecto de FastAPI
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
