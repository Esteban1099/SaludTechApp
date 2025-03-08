from pulsar.schema import *

from src.procesamiento_imagen.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DemografiaRecord(Record):
    id = String()
    edad = Integer()
    grupo_edad = String()
    sexo = String()
    etnicidad = String()


class AtributoRecord(Record):
    id = String()
    nombre = String()
    descripcion = String()


class DiagnosticoRecord(Record):
    id = String()
    nombre = String()
    descripcion = String()
    demografia = DemografiaRecord()
    atributos = Array(AtributoRecord())


class RegionAnatomicaRecord(Record):
    id = String()
    categoria = String()
    especificacion = String()

class ImagenMedicaProcesadaPayload(Record):
    id = String()
    modalidad = String()
    url = String()
    flag = Integer()
    fecha_creacion = String()
    regiones_anatomicas = Array(RegionAnatomicaRecord())
    diagnostico = DiagnosticoRecord()
    estado = String()


class EventoImagenMedicaProcesada(EventoIntegracion):
    data = ImagenMedicaProcesadaPayload()

class ImagenMedicaEliminadaPayload(Record):
    id = String()
    estado = String()


class EventoImagenMedicaEliminada(EventoIntegracion):
    data = ImagenMedicaEliminadaPayload()