FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY canonizacion-requirements.txt .
RUN pip install -r canonizacion-requirements.txt

# Copiar el código fuente
COPY src/ ./src/

CMD ["python", "-m", "src.canonizacion.main"] 