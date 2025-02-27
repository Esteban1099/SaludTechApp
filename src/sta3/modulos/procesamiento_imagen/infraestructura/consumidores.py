import logging
import traceback

import _pulsar
import pulsar
from pulsar.schema import *

from src.sta3.modulos.procesamiento_imagen.dominio.mapeadores import MapeadorComandoProcesarImagenMedica
from src.sta3.modulos.procesamiento_imagen.infraestructura.schema.v1.comandos import ComandoProcesarImagenMedica
from src.sta3.modulos.procesamiento_imagen.infraestructura.schema.v1.eventos import EventoImagenMedicaProcesada
from src.sta3.seedwork.aplicacion.comandos import ejecutar_comando
from src.sta3.seedwork.infraestructura import utils


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-imagen-medica-procesada', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-eventos-imagen-medica-procesada',
                                       schema=AvroSchema(EventoImagenMedicaProcesada))

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
        consumidor = cliente.subscribe('comandos-imagen-medica-procesar', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sta-sub-comandos-imagen-medica-procesar',
                                       schema=AvroSchema(ComandoProcesarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')
            mapeador = MapeadorComandoProcesarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(mensaje.value())
            ejecutar_comando(comando)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
