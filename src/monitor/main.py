import os
import sys
import time
import requests

INGESTA_AUTOMATIZADA_HOST = os.getenv('INGESTA_AUTOMATIZADA_HOST', "localhost")
CANONIZACION_HOST = os.getenv('CANONIZACION_HOST', "localhost")
STA3_HOST = os.getenv('STA3_HOST', "localhost")


def check_service(name, url):
    try:
        requests.get(url, timeout=5)
        print(f"Servicio {name} up!", file=sys.stdout)
    except requests.exceptions.RequestException:
        print(f"Servicio {name} down!", file=sys.stdout)


def monitor():
    healthcheck_urls = {
        "ingesta automatizada": f'http://{INGESTA_AUTOMATIZADA_HOST}:5000/health',
        "canonización": f'http://{CANONIZACION_HOST}:5002/health',
        "sta3": f'http://{STA3_HOST}:5000/health'
    }

    try:
        while True:
            for name, url in healthcheck_urls.items():
                check_service(name, url)
            time.sleep(3)
    except KeyboardInterrupt:
        print("Monitoreo detenido.")


if __name__ == '__main__':
    monitor()
