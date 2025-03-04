import json
import logging
from typing import Dict, Any

import pulsar
from pulsar.schema import *

from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.comandos import ComandoCanonizarImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.eventos import EventoImagenMedicaAgregada
from src.canonizacion.modulos.canonizacion.aplicacion.comandos.canonizar_imagen_medica import CanonizarImagenMedica, CanonizarImagenMedicaHandler
from src.canonizacion.modulos.canonizacion.dominio.mapeadores import MapeadorComandoCanonizarImagenMedica
from src.canonizacion.seedwork.infraestructura import utils

logger = logging.getLogger(__name__)

def suscribirse_a_eventos():
    cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
    consumidor = cliente.subscribe('eventos-imagen-medica', consumer_type=pulsar.ConsumerType.Shared,
                                 subscription_name='canonizacion-sub-eventos',
                                 schema=AvroSchema(EventoImagenMedicaAgregada))

    while True:
        try:
            mensaje = consumidor.receive()
            datos = mensaje.value()
            logger.info(f'Evento recibido: {datos}')

            mapeador = MapeadorComandoCanonizarImagenMedica()
            comando = mapeador.evento_a_comando(datos.data)
            
            handler = CanonizarImagenMedicaHandler()
            handler.handle(comando)

            consumidor.acknowledge(mensaje)
        except Exception as e:
            logger.error(f'Error al procesar mensaje: {e}')
            consumidor.negative_acknowledge(mensaje)

def suscribirse_a_comandos():
    cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
    consumidor = cliente.subscribe('comandos-imagen-medica', consumer_type=pulsar.ConsumerType.Shared,
                                 subscription_name='canonizacion-sub-comandos',
                                 schema=AvroSchema(ComandoCanonizarImagenMedica))

    while True:
        try:
            mensaje = consumidor.receive()
            datos = mensaje.value()
            logger.info(f'Comando recibido: {datos}')

            mapeador = MapeadorComandoCanonizarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(datos)
            
            handler = CanonizarImagenMedicaHandler()
            handler.handle(comando)

            consumidor.acknowledge(mensaje)
        except Exception as e:
            logger.error(f'Error al procesar mensaje: {e}')
            consumidor.negative_acknowledge(mensaje)
