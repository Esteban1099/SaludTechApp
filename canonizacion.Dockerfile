FROM python:3.9-slim

WORKDIR /app
COPY canonizacion-requirements.txt .
RUN pip install -r canonizacion-requirements.txt

COPY src/ ./src/

CMD ["python", "-m", "src.canonizacion.main"] 