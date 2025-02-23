import pulsar
from pulsar.schema import *

import datetime

from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.comandos import ComandoAgregarImagenMedicaPayload, \
    ComandoAgregarImagenMedica
from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import EventoImagenMedicaAgregada
from src.sta.seedwork.infraestructura import utils

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_comando(self, comando, topico):
        payload = ComandoAgregarImagenMedicaPayload(
            id=str(comando.id),
            modalidad=comando.modalidad,
            fecha_creacion=comando.fecha_creacion
        )
        comando_integracion = ComandoAgregarImagenMedica(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoAgregarImagenMedica))
