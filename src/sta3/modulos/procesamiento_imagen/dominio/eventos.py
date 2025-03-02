import uuid
from dataclasses import dataclass
from datetime import datetime

from src.sta3.seedwork.dominio.eventos import EventoDominio

@dataclass
class ImagenMedicaProcesada(EventoDominio):
    id: uuid.UUID = None
    url: str = None
    modalidad: str = None
    fecha_creacion: datetime = None
    estado: str = None