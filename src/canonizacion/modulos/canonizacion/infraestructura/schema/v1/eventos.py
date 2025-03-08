from dataclasses import dataclass, field
from pulsar.schema import *

from src.canonizacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class ImagenMedicaAgregadaPayload(Record):
    id = String()
    modalidad = String()
    fecha_creacion = String()
    estado = String()
    url = String()
    flag = Integer(default=1)  # Nuevo campo para decisiones, por defecto acepta


class EventoImagenMedicaAgregada(EventoIntegracion):
    type = String(default="ImagenMedicaAgregada")
    data = ImagenMedicaAgregadaPayload()


class ImagenMedicaCanonizadaPayload(Record):
    id = String()
    modalidad = String()
    fecha_creacion = String()
    estado = String()


class EventoImagenMedicaCanonizada(EventoIntegracion):
    data = ImagenMedicaCanonizadaPayload()


# Nuevo esquema para eventos de compensación
class CompensacionImagenMedicaPayload(Record):
    id = String()
    motivo = String()
    fecha_compensacion = String()


class EventoCompensacionImagenMedica(EventoIntegracion):
    data = CompensacionImagenMedicaPayload()
