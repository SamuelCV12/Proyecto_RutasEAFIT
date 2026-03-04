# Usamos una versión oficial y ligera de Python para ahorrar memoria
FROM python:3.10-slim

# Evita que Python escriba archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que la salida de Python se envíe directamente a la terminal (útil para logs)
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos las dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiamos el resto del código del proyecto al contenedor
COPY . /app/