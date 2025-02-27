from pulsar.schema import *

from src.canonizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class ImagenMedicaAgregadaPayload(Record):
    id = String()
    modalidad = String()
    fecha_creacion = String()
    estado = String()


class EventoImagenMedicaAgregada(EventoIntegracion):
    data = ImagenMedicaAgregadaPayload()


class ImagenMedicaCanonizadaPayload(Record):
    id = String()
    modalidad = String()
    fecha_creacion = String()
    estado = String()


class EventoImagenMedicaCanonizada(EventoIntegracion):
    data = ImagenMedicaCanonizadaPayload()
