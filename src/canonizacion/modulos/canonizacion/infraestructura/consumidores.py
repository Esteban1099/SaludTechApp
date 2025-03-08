import logging
import sys
from datetime import datetime
import traceback

import pulsar
from pulsar.schema import *

from src.canonizacion.modulos.canonizacion.aplicacion.comandos.eliminar_imagen_medica import EliminarImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.comandos import ComandoCanonizarImagenMedica, ComandoEliminarImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.eventos import EventoImagenMedicaAgregada, EventoCompensacionImagenMedica
from src.canonizacion.modulos.canonizacion.aplicacion.comandos.canonizar_imagen_medica import CanonizarImagenMedicaHandler
from src.canonizacion.modulos.canonizacion.dominio.mapeadores import MapeadorComandoCanonizarImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.despachadores import Despachador
from src.canonizacion.seedwork.aplicacion.comandos import ejecutar_comando
from src.canonizacion.seedwork.infraestructura import utils


def suscribirse_a_eventos():
    cliente = None
    consumidor = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(
            'eventos-imagen-medica',
            consumer_type=pulsar.ConsumerType.Shared,
            subscription_name='canonizacion-sub-eventos',
            schema=AvroSchema(EventoImagenMedicaAgregada)
        )

        despachador = Despachador()

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}', file=sys.stdout)

            if hasattr(datos, 'flag') and datos.flag == 0:
                logging.info(f'Rechazando transacción por flag=0, iniciando compensación para imagen {datos.id}')
                comando = EliminarImagenMedica(id=datos.id)
                despachador.publicar_comando(comando, topico='comandos-imagen-medica-canonizar-compensacion')
            else:
                logging.info(f'Aceptando transacción para imagen {datos.id}')
                comando = ComandoCanonizarImagenMedica(
                    id=datos.id,
                    url=datos.url,
                    fecha_creacion=datos.fecha_creacion,
                    flag=datos.flag
                    # Considera agregar regiones_anatomicas y diagnostico si están disponibles
                )
                despachador.publicar_comando(comando, topico='comandos-imagen-medica-canonizar')

            consumidor.acknowledge(mensaje)
            logging.info(f'Comando publicado exitosamente para imagen {datos.id}')

    except Exception as e:
        logging.error(f'ERROR grave en la suscripción al tópico de eventos: {e}')
        traceback.print_exc()
    finally:
        if consumidor:
            consumidor.close()
        if cliente:
            cliente.close()


def suscribirse_a_eventos_compensacion():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-compensacion-imagen-medica', consumer_type=pulsar.ConsumerType.Shared,
                                   subscription_name='canonizacion-sub-eventos-compensacion',
                                   schema=AvroSchema(EventoCompensacionImagenMedica))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            logging.info(f'Evento de compensación recibido: {datos}')

            id_imagen = datos.id
            logging.info(f'Iniciando compensación para imagen con ID: {id_imagen}')

            comando = EliminarImagenMedica(id=id_imagen)
            despachador = Despachador()
            despachador.publicar_comando(comando, topico='comandos-imagen-medica-canonizar-compensacion')

            logging.info(f'Compensación completada para imagen con ID: {id_imagen}')

            consumidor.acknowledge(mensaje)
    except Exception as e:
        logging.error(f'Error al procesar mensaje 2: {e}')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-imagen-medica-canonizar', consumer_type=pulsar.ConsumerType.Shared,
                                       subscription_name='canonizar-sub-comandos-imagen-medica-canonizar',
                                       schema=AvroSchema(ComandoCanonizarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}', file=sys.stdout)
            mapeador = MapeadorComandoCanonizarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(mensaje.value())
            ejecutar_comando(comando)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_compensacion():
    cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
    consumidor = cliente.subscribe('comandos-imagen-medica-canonizar-compensacion', consumer_type=pulsar.ConsumerType.Shared,
                                   subscription_name='canonizar-sub-comandos-imagen-medica-compensacion',
                                   schema=AvroSchema(ComandoEliminarImagenMedica))

    while True:
        try:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            logging.info(f'Evento de compensación recibido: {datos}')

            id_imagen = datos.id
            logging.info(f'Iniciando compensación para imagen con ID: {id_imagen}')

            comando = EliminarImagenMedica(id=id_imagen)
            ejecutar_comando(comando)

            logging.info(f'Compensación completada para imagen con ID: {id_imagen}')

            consumidor.acknowledge(mensaje)
        except Exception as e:
            logging.error(f'Error suscribiéndose al tópico de compensación: {e}')
            traceback.print_exc()
            if cliente:
                cliente.close()
