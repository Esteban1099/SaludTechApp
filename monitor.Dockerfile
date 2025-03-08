FROM python:3.8

COPY monitor-requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r monitor-requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "./src/monitor/main.py"]