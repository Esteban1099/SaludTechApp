import logging
import traceback

import _pulsar
import pulsar
from pulsar.schema import *

from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.comandos import ComandoAgregarImagenMedica
from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import EventoImagenMedicaAgregada
from src.sta.seedwork.infraestructura import utils

from src.sta.seedwork.aplicacion.comandos import ejecutar_comando


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-eventos',
                                       schema=AvroSchema(EventoImagenMedicaAgregada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-comandos-imagen-medica',
                                       schema=AvroSchema(ComandoAgregarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
