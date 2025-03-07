import time
from datetime import datetime

import requests


def monitor():
    healthcheck_canonizacion = "http://pqrs-1:5000/healthcheck"
    url_pqrs_2 = "http://pqrs-2:5000/healthcheck"
    url_clientes = "http://clientes:5000/healthcheck"
    while (True):
        response1 = requests.get(healthcheck_canonizacion)
        if response1.status_code != 200:
            mensaje = {"instance": "pqrs-1", "status": "Servicio no disponible",
                       "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}

        response2 = requests.get(url_pqrs_2)
        if response2.status_code != 200:
            mensaje = {"instance": "pqrs-2", "status": "Servicio no disponible",
                       "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}

        response3 = requests.get(url_clientes)
        if response3.status_code != 200:
            mensaje = {"instance": "clientes", "status": "Servicio no disponible",
                       "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}

        time.sleep(3)


if __name__ == '__main__':
    monitor()
