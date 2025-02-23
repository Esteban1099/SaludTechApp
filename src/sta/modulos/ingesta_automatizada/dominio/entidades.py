from __future__ import annotations

from dataclasses import dataclass, field

import src.sta.modulos.ingesta_automatizada.dominio.objetos_valor as objetos_valor
from src.sta.modulos.ingesta_automatizada.dominio.eventos import ImagenMedicaAgregada, ImagenMedicaPagada
from src.sta.seedwork.dominio.entidades import AgregacionRaiz, Entidad


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
    estado = objetos_valor.EstadoImagenMedica.CREADA

    def agregar_imagen_medica(self, imagen_medica: ImagenMedica):
        self.diagnostico = imagen_medica.diagnostico
        self.modalidad = imagen_medica.modalidad
        self.fecha_creacion = imagen_medica.fecha_creacion
        self.regiones_anatomicas = imagen_medica.regiones_anatomicas
        self.agregar_evento(ImagenMedicaAgregada(
            id_imagen_medica=self.id,
            estado=self.estado,
            fecha_creacion=self.fecha_creacion
        ))

    def pagar_imagen_medica(self):
        self.estado = objetos_valor.EstadoImagenMedica.PAGADA
        self.agregar_evento(ImagenMedicaPagada(
            id_imagen_medica=self.id,
            fecha_actualizacion=self.fecha_actualizacion
        ))
