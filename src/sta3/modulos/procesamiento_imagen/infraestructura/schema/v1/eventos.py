from pulsar.schema import *

from src.sta3.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class ImagenMedicaProcesadaPayload(Record):
    id = String()
    url = String()
    modalidad = String()
    fecha_creacion = String()
    estado = String()


class EventoImagenMedicaProcesada(EventoIntegracion):
    data = ImagenMedicaProcesadaPayload()
