import uuid
from dataclasses import dataclass
from datetime import datetime

from src.sta.seedwork.dominio.eventos import EventoDominio

@dataclass
class ImagenMedicaAgregada(EventoDominio):
    id_imagen_medica: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None

@dataclass
class ImagenMedicaPagada(EventoDominio):
    id_imagen_medica: uuid.UUID = None
    fecha_actualizacion: datetime = None
