FROM python:3.12.2

EXPOSE 5000

COPY procesamiento_imagen-requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r procesamiento_imagen-requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD [ "flask", "--app", "./src/procesamiento_imagen/api", "run", "--host=0.0.0.0"]