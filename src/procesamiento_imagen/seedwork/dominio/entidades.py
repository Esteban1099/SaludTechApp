import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.procesamiento_imagen.seedwork.dominio.eventos import EventoDominio
from src.procesamiento_imagen.seedwork.dominio.excepciones import IdDebeSerInmutableExcepcion
from src.procesamiento_imagen.seedwork.dominio.mixins import ValidarReglasMixin
from src.procesamiento_imagen.seedwork.dominio.reglas import IdEntidadEsInmutable


@dataclass
class Entidad:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    fecha_creacion: datetime = field(default=datetime.now())
    fecha_actualizacion: datetime = field(default=datetime.now())

    @classmethod
    def generar_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value) -> None:
        if not IdEntidadEsInmutable(self).es_valido():
            raise IdDebeSerInmutableExcepcion()
        self._id = self.generar_id()


@dataclass
class AgregacionRaiz(Entidad, ValidarReglasMixin):
    eventos: list[EventoDominio] = field(default_factory=list)

    def agregar_evento(self, evento: EventoDominio):
        self.eventos.append(evento)

    def limpiar_eventos(self):
        self.eventos = list()
