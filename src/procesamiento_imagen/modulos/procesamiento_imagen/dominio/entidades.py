from __future__ import annotations

from dataclasses import dataclass, field

import src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.objetos_valor as objetos_valor
from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.eventos import ImagenMedicaProcesada, \
    ImagenMedicaEliminada, AtributoProcesada, DemografiaProcesada, DiagnosticoProcesada, RegionAnatomicaProcesada
from src.procesamiento_imagen.seedwork.dominio.entidades import AgregacionRaiz, Entidad


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
    url: str = None
    diagnostico: Diagnostico = None
    modalidad: objetos_valor.Modalidad = None
    flag: int = None
    regiones_anatomicas: list[RegionAnatomica] = field(default_factory=list[RegionAnatomica])
    estado = objetos_valor.EstadoImagenMedica.EN_PROCESAMIENTO

    def procesar_imagen_medica(self, imagen_medica: ImagenMedica):
        self.imagen = imagen_medica.url
        self.diagnostico = imagen_medica.diagnostico
        self.modalidad = imagen_medica.modalidad
        self.flag = imagen_medica.flag
        self.fecha_creacion = imagen_medica.fecha_creacion
        self.regiones_anatomicas = imagen_medica.regiones_anatomicas
        self.estado=objetos_valor.EstadoImagenMedica.PROCESADA
        self.agregar_evento(ImagenMedicaProcesada(
            id=self.id,
            modalidad=self.modalidad.value,
            url=self.url,
            flag=self.flag,
            fecha_creacion=self.fecha_creacion,
            regiones_anatomicas=[
                RegionAnatomicaProcesada(
                    id=region_anatomica.id,
                    categoria=region_anatomica.categoria.value,
                    especificacion=region_anatomica.especificacion
                ) for region_anatomica in self.regiones_anatomicas
            ],
            diagnostico=DiagnosticoProcesada(
                id=self.diagnostico.id,
                nombre=self.diagnostico.nombre,
                demografia=DemografiaProcesada(
                    id=self.diagnostico.demografia.id,
                    edad=self.diagnostico.demografia.edad,
                    grupo_edad=self.diagnostico.demografia.grupo_edad.value,
                    sexo=self.diagnostico.demografia.sexo.value,
                    etnicidad=self.diagnostico.demografia.etnicidad.value,
                ),
                atributos=[
                    AtributoProcesada(
                        id=atributo.id,
                        nombre=atributo.nombre,
                        descripcion=atributo.descripcion,
                    ) for atributo in self.diagnostico.atributos
                ]
            ),
            estado=self.estado.value
        ))

    def eliminar_imagen_medica(self, id):
        self.id = id
        self._id = id
        self.agregar_evento(ImagenMedicaEliminada(
            id=self.id,
            estado=objetos_valor.EstadoImagenMedica.ELIMINADA.value
        ))
