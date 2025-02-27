from __future__ import annotations

from dataclasses import dataclass, field

import src.canonizacion.modulos.canonizacion.dominio.objetos_valor as objetos_valor
from src.canonizacion.modulos.canonizacion.dominio.eventos import ImagenMedicaAgregada, ImagenMedicaCanonizada
from src.canonizacion.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class RegionAnatomica(Entidad):
    categoria: objetos_valor.CategoriaAnatomica = None
    especificacion: str = field(default_factory=str)


@dataclass
class Atributo(Entidad):
    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)


@dataclass
class Demografia(Entidad):
    edad: int = field(default_factory=int)
    grupo_edad: objetos_valor.GrupoEdad = None
    sexo: objetos_valor.Sexo = None
    etnicidad: objetos_valor.Etnia = None


@dataclass
class Diagnostico(Entidad):
    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    demografia: Demografia = None
    atributos: list[Atributo] = field(default_factory=list[Atributo])


@dataclass
class ImagenMedica(AgregacionRaiz):
    diagnostico: Diagnostico = None
    modalidad: objetos_valor.Modalidad = None
    regiones_anatomicas: list[RegionAnatomica] = field(default_factory=list[RegionAnatomica])
    estado = objetos_valor.EstadoImagenMedica.EN_INGESTA

    def agregar_imagen_medica(self, imagen_medica: ImagenMedica):
        self.diagnostico = imagen_medica.diagnostico
        self.modalidad = imagen_medica.modalidad
        self.fecha_creacion = imagen_medica.fecha_creacion
        self.regiones_anatomicas = imagen_medica.regiones_anatomicas
        self.estado=objetos_valor.EstadoImagenMedica.CREADA
        self.agregar_evento(ImagenMedicaAgregada(
            id=self.id,
            modalidad=self.modalidad.value,
            fecha_creacion=self.fecha_creacion,
            estado=self.estado.value
        ))
        
    def canonizar_imagen_medica(self):
        # Aquí iría la lógica real de canonización, pero para este ejemplo solo cambiamos el estado
        self.estado = objetos_valor.EstadoImagenMedica.CANONIZADA
        self.agregar_evento(ImagenMedicaCanonizada(
            id=self.id,
            modalidad=self.modalidad.value,
            fecha_creacion=self.fecha_creacion,
            estado=self.estado.value
        ))
