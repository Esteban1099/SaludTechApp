from pulsar.schema import *

from src.sta.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class ImagenMedicaAgregadaPayload(Record):
    id = String()
    modalidad = String()
    fecha_creacion = String()
    estado = String()


class EventoImagenMedicaAgregada(EventoIntegracion):
    data = ImagenMedicaAgregadaPayload()
