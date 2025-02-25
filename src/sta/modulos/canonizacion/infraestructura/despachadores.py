import pulsar
from pulsar.schema import *
import datetime

from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.eventos import EventoImagenCanonizada, ImagenCanonizadaPayload
from src.sta.seedwork.infraestructura import utils

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento_canonizacion(self, evento_dict):
        payload = ImagenCanonizadaPayload(
            id=evento_dict['id'],
            id_imagen_original=evento_dict['id_imagen_original'],
            formato_canonizado=evento_dict['formato_canonizado'],
            fecha_canonizacion=evento_dict['fecha_canonizacion'],
            metadatos=evento_dict['metadatos']
        )
        evento = EventoImagenCanonizada(data=payload)
        self._publicar_mensaje(evento, 'eventos-imagen-canonizada', AvroSchema(EventoImagenCanonizada)) 