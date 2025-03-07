FROM python:3.12.2

EXPOSE 5000

COPY ingesta_automatizada-requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r ingesta_automatizada-requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD [ "flask", "--app", "./src/ingesta_automatizada/api", "run", "--host=0.0.0.0"]