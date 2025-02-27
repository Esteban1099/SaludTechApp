import uuid
from dataclasses import dataclass
from datetime import datetime

from src.canonizacion.seedwork.dominio.eventos import EventoDominio


@dataclass
class ImagenMedicaAgregada(EventoDominio):
    id: uuid.UUID = None
    modalidad: str = None
    fecha_creacion: datetime = None
    estado: str = None


@dataclass
class ImagenMedicaCanonizada(EventoDominio):
    id: uuid.UUID = None
    modalidad: str = None
    fecha_creacion: datetime = None
    estado: str = None
