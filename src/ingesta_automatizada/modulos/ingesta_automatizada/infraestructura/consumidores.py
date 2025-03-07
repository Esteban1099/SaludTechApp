import logging
import sys
import traceback

import _pulsar
import pulsar
from pulsar.schema import *

from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.mapeadores import MapeadorComandoAgregarImagenMedica, \
    MapeadorComandoEliminarImagenMedica
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.schema.v1.comandos import \
    ComandoAgregarImagenMedica, \
    ComandoEliminarImagenMedica
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import \
    EventoImagenMedicaAgregada, \
    EventoImagenMedicaEliminada
from src.ingesta_automatizada.seedwork.aplicacion.comandos import ejecutar_comando
from src.ingesta_automatizada.seedwork.dominio.excepciones import ExcepcionDominio
from src.ingesta_automatizada.seedwork.infraestructura import utils


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='ingesta_automatizada-sub-eventos-imagen-medica',
                                       schema=AvroSchema(EventoImagenMedicaAgregada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}', sys.stdout)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_eventos_compensacion():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-compensacion-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='ingesta_automatizada-sub-eventos-compensacion-imagen-medica',
                                       schema=AvroSchema(EventoImagenMedicaEliminada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}', sys.stdout)
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
                                       subscription_name='ingesta_automatizada-sub-comandos-imagen-medica',
                                       schema=AvroSchema(ComandoAgregarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}', file=sys.stdout)
            mapeador = MapeadorComandoAgregarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(mensaje.value())
            ejecutar_comando(comando)
            consumidor.acknowledge(mensaje)
            print(f'Se ejecutó el comando exitosamente: {comando}', sys.stdout)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos_compensacion():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-compensacion-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='ingesta_automatizada-sub-comandos-compensancion-imagen-medica',
                                       schema=AvroSchema(ComandoEliminarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando de compensaciónn recibido: {mensaje.value().data}', file=sys.stdout)
            mapeador = MapeadorComandoEliminarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(mensaje.value())
            try:
                ejecutar_comando(comando)
                print(f'Se ejecutó el comando de compensación exitosamente: {comando}', sys.stdout)
            except ExcepcionDominio as e:
                print(e, sys.stdout)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
