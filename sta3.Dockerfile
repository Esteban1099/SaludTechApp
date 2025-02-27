FROM python:3.12.2

EXPOSE 5003

COPY sta3-requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r sta3-requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/sta/api", "run", "--host=0.0.0.0"]