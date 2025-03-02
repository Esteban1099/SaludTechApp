FROM python:3.12.2

EXPOSE 5000

COPY bff-requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r bff-requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/bff/api", "run", "--host=0.0.0.0"]