import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .excepciones import IdDebeSerInmutableExcepcion
from .reglas import IdEntidadEsInmutable


@dataclass
class EventoDominio():
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    fecha_evento: datetime = field(default=datetime.now())

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
