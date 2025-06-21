# Dockerfile para desarrollo
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para cachear la instalación
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Variables de entorno para desarrollo
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Puerto de la aplicación
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
