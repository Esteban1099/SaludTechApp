import threading
from src.canonizacion.modulos.canonizacion.infraestructura.consumidores import suscribirse_a_eventos

if __name__ == "__main__":
    # Iniciar el consumidor de eventos
    suscribirse_a_eventos() 