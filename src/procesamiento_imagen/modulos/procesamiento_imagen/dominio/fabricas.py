from dataclasses import dataclass

from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.entidades import ImagenMedica
from src.procesamiento_imagen.seedwork.dominio.entidades import Entidad
from src.procesamiento_imagen.seedwork.dominio.fabricas import Fabrica
from src.procesamiento_imagen.seedwork.dominio.mapeadores import Mapeador


@dataclass
class _FabricaProcesamientoImagen(Fabrica):
    def crear_objeto(self, objeto: any, mapeador: Mapeador = None) -> any:
        if isinstance(objeto, Entidad):
            return mapeador.entidad_a_dto(objeto)
        else:
            imagen_medica: ImagenMedica = mapeador.dto_a_entidad(objeto)
            return imagen_medica


@dataclass
class FabricaProcesamientoImagen(Fabrica):
    def crear_objeto(self, objeto: any, mapeador: Mapeador = None) -> any:
        if mapeador.obtener_tipo() == ImagenMedica.__class__:
            fabrica_imagen_medica = _FabricaProcesamientoImagen()
            return fabrica_imagen_medica.crear_objeto(objeto, mapeador)
