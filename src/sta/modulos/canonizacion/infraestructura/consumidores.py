import logging
import traceback
import _pulsar
import pulsar
from pulsar.schema import *
import uuid
import datetime

from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import EventoImagenMedicaAgregada
from src.canonizacion.modulos.canonizacion.infraestructura.despachadores import Despachador

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-imagen-medica', 
                                    consumer_type=_pulsar.ConsumerType.Shared,
                                    subscription_name='canonizacion-sub-eventos',
                                    schema=AvroSchema(EventoImagenMedicaAgregada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento de imagen recibido: {mensaje.value().data}')
            
            # Mock del proceso de canonización
            print('Iniciando proceso de canonización...')
            despachador = Despachador()
            
            # Simulamos el proceso de canonización
            imagen_canonizada = {
                'id': str(uuid.uuid4()),
                'id_imagen_original': mensaje.value().data.id,
                'formato_canonizado': 'DICOM_CANONICO_V1',
                'fecha_canonizacion': datetime.datetime.now().isoformat(),
                'metadatos': 'Metadata estandarizada según protocolo XYZ'
            }
            
            # Publicamos el evento de canonización completada
            despachador.publicar_evento_canonizacion(imagen_canonizada)
            print('Proceso de canonización completado')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiéndose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close() 