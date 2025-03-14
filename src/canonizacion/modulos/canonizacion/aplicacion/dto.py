from dataclasses import field, dataclass

from src.canonizacion.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class DemografiaDTO(DTO):
    id: str = field(default_factory=str)
    edad: int = field(default_factory=int)
    grupo_edad: str = field(default_factory=str)
    sexo: str = field(default_factory=str)
    etnicidad: str = field(default_factory=str)


@dataclass(frozen=True)
class RegionAnatomicaDTO(DTO):
    id: str = field(default_factory=str)
    categoria: str = field(default_factory=str)
    especificacion: str = field(default_factory=str)


@dataclass(frozen=True)
class AtributoDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)


@dataclass(frozen=True)
class DiagnosticoDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    demografia: DemografiaDTO = field(default_factory=DemografiaDTO)
    atributos: list[AtributoDTO] = field(default_factory=list[AtributoDTO])


@dataclass(frozen=True)
class ImagenMedicaDTO(DTO):
    id: str = field(default_factory=str)
    modalidad: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    regiones_anatomicas: list[RegionAnatomicaDTO] = field(default_factory=list[RegionAnatomicaDTO])
    diagnostico: DiagnosticoDTO = field(default_factory=DiagnosticoDTO)
