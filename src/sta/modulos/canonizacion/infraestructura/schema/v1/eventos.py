from pulsar.schema import *
from src.sta.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ImagenCanonizadaPayload(Record):
    id = String()
    id_imagen_original = String()
    formato_canonizado = String()
    fecha_canonizacion = String()
    metadatos = String()  # En un caso real, esto podría ser un objeto más complejo

class EventoImagenCanonizada(EventoIntegracion):
    data = ImagenCanonizadaPayload() 