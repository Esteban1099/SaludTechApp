import uuid
from dataclasses import dataclass
from datetime import datetime

from src.procesamiento_imagen.seedwork.dominio.eventos import EventoDominio


@dataclass
class DemografiaProcesada():
    id: uuid.UUID = None
    edad: int = None
    grupo_edad: str = None
    sexo: str = None
    etnicidad: str = None


@dataclass
class AtributoProcesada():
    id: uuid.UUID = None
    nombre: str = None
    descripcion: str = None


@dataclass
class DiagnosticoProcesada():
    id: uuid.UUID = None
    nombre: str = None
    descripcion: str = None
    demografia: DemografiaProcesada = None
    atributos: [AtributoProcesada] = None


@dataclass
class RegionAnatomicaProcesada():
    id: uuid.UUID = None
    categoria: str = None
    especificacion: str = None


@dataclass
class ImagenMedicaProcesada(EventoDominio):
    id: uuid.UUID = None
    modalidad: str = None
    url: str = None
    flag: int = None
    fecha_creacion: datetime = None
    regiones_anatomicas: [RegionAnatomicaProcesada] = None
    diagnostico: DiagnosticoProcesada = None
    estado: str = None


@dataclass
class ImagenMedicaEliminada(EventoDominio):
    id: uuid.UUID = None
    estado: str = None