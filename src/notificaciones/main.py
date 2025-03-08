import os
import sys
import time
import uuid

import _pulsar
import pulsar
from pulsar.schema import *


def time_millis():
    return int(time.time() * 1000)


class EventoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()


class ImagenMedicaAgregadaPayload(Record):
    id = String()
    modalidad = String()
    fecha_creacion = String()
    estado = String()


class EventoImagenMedicaAgregada(EventoIntegracion):
    data = ImagenMedicaAgregadaPayload()


BROKER_HOST = os.getenv('BROKER_HOST', default="localhost")

client = pulsar.Client(f'pulsar://{BROKER_HOST}:6650')
consumer = client.subscribe('eventos-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                            subscription_name='notificaciones-sub-eventos-imagen-medica',
                            schema=AvroSchema(EventoImagenMedicaAgregada))

while True:
    msg = consumer.receive()
    print('=========================================')
    print("Mensaje Recibido: '%s'" % msg.value().data, file=sys.stdout)
    print('=========================================')

    print('==== Envía correo a usuario ====', file=sys.stdout)

    consumer.acknowledge(msg)

client.close()
