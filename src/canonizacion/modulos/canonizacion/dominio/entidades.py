from dataclasses import dataclass, field
from src.sta.seedwork.dominio.entidades import AgregacionRaiz
from datetime import datetime
from uuid import UUID

@dataclass
class Demografia:
    id: UUID
    edad: int
    grupo_edad: str
    sexo: str
    etnicidad: str

@dataclass
class Atributo:
    id: UUID
    nombre: str
    descripcion: str

@dataclass
class Diagnostico:
    id: UUID
    nombre: str
    descripcion: str
    demografia: Demografia
    atributos: list[Atributo]

@dataclass
class RegionAnatomica:
    id: UUID
    categoria: str
    especificacion: str

@dataclass
class ImagenCanonizada(AgregacionRaiz):
    id: UUID
    fecha_creacion: datetime
    modalidad: str
    diagnostico: Diagnostico
    regiones_anatomicas: list[RegionAnatomica]
    formato_canonizado: str = field(default="DICOM_CANONICO_V1")
    fecha_canonizacion: datetime = field(default_factory=datetime.now) 