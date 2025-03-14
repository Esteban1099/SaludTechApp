FROM python:3.12.2

EXPOSE 5002

COPY canonizacion-requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r canonizacion-requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD [ "flask", "--app", "./src/canonizacion/api", "run", "--host=0.0.0.0", "--port=5002"]