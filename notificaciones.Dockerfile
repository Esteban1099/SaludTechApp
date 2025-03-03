FROM python:3.12.2

COPY notificaciones-requirements.txt ./
RUN pip install --no-cache-dir -r notificaciones-requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD [ "python", "./src/notificaciones/main.py" ]