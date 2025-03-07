from pulsar.schema import *

from src.ingesta_automatizada.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)


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


class ComandoAgregarImagenMedicaPayload(ComandoIntegracion):
    id = String()
    modalidad = String()
    url = String()
    flag = Integer()
    fecha_creacion = String()
    regiones_anatomicas = Array(RegionAnatomicaRecord())
    diagnostico = DiagnosticoRecord()


class ComandoAgregarImagenMedica(ComandoIntegracion):
    data = ComandoAgregarImagenMedicaPayload()


class ComandoEliminarImagenMedicaPayload(ComandoIntegracion):
    id = String()


class ComandoEliminarImagenMedica(ComandoIntegracion):
    data = ComandoEliminarImagenMedicaPayload()
