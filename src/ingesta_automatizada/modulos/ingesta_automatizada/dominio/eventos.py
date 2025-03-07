import uuid
from dataclasses import dataclass
from datetime import datetime

from src.ingesta_automatizada.seedwork.dominio.eventos import EventoDominio


@dataclass
class DemografiaAgregada():
    id: uuid.UUID = None
    edad: int = None
    grupo_edad: str = None
    sexo: str = None
    etnicidad: str = None


@dataclass
class AtributoAgregada():
    id: uuid.UUID = None
    nombre: str = None
    descripcion: str = None


@dataclass
class DiagnosticoAgregada():
    id: uuid.UUID = None
    nombre: str = None
    descripcion: str = None
    demografia: DemografiaAgregada = None
    atributos: [AtributoAgregada] = None


@dataclass
class RegionAnatomicaAgregada():
    id: uuid.UUID = None
    categoria: str = None
    especificacion: str = None


@dataclass
class ImagenMedicaAgregada(EventoDominio):
    id: uuid.UUID = None
    modalidad: str = None
    url: str = None
    flag: int = None
    fecha_creacion: datetime = None
    regiones_anatomicas: [RegionAnatomicaAgregada] = None
    diagnostico: DiagnosticoAgregada = None
    estado: str = None


@dataclass
class ImagenMedicaEliminada(EventoDominio):
    id: uuid.UUID = None
    estado: str = None
