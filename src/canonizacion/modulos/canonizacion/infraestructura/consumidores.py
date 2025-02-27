import logging
import traceback
import uuid
from datetime import datetime

import _pulsar
import pulsar
from pulsar.schema import *

from src.canonizacion.modulos.canonizacion.dominio.mapeadores import MapeadorComandoAgregarImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.comandos import ComandoAgregarImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.eventos import EventoImagenMedicaAgregada
from src.canonizacion.seedwork.aplicacion.comandos import ejecutar_comando
from src.canonizacion.seedwork.infraestructura import utils
from src.canonizacion.modulos.canonizacion.infraestructura.despachadores import Despachador
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica
from src.canonizacion.modulos.canonizacion.dominio.objetos_valor import Modalidad, EstadoImagenMedica


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='canonizacion-sub-eventos-imagen-medica',
                                       schema=AvroSchema(EventoImagenMedicaAgregada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido en canonización: {mensaje.value().data}')
            
            # Procesar el evento recibido
            datos = mensaje.value().data
            
            # Crear una imagen médica con los datos recibidos
            imagen_medica = ImagenMedica()
            imagen_medica.id = uuid.UUID(datos.id)
            imagen_medica.modalidad = Modalidad(datos.modalidad)
            imagen_medica.fecha_creacion = datetime.fromisoformat(datos.fecha_creacion)
            imagen_medica.estado = EstadoImagenMedica.CREADA
            
            # Canonizar la imagen médica
            imagen_medica.canonizar_imagen_medica()
            
            # Publicar el evento de canonización
            despachador = Despachador()
            despachador.publicar_evento(evento=imagen_medica.eventos[-1], topico='eventos-imagen-canonizada')
            
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
                                       subscription_name='canonizacion-sub-comandos-imagen-medica',
                                       schema=AvroSchema(ComandoAgregarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')
            mapeador = MapeadorComandoAgregarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(mensaje.value())
            ejecutar_comando(comando)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
