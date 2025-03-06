from dataclasses import dataclass

from src.sta3.modulos.procesamiento_imagen.dominio.entidades import ImagenMedica
from src.sta3.seedwork.dominio.entidades import Entidad
from src.sta3.seedwork.dominio.fabricas import Fabrica
from src.sta3.seedwork.dominio.mapeadores import Mapeador


@dataclass
class _FabricaProcesamientoImagen(Fabrica):
    def crear_objeto(self, objeto: any, mapeador: Mapeador = None) -> any:
        if isinstance(objeto, Entidad):
            return mapeador.entidad_a_dto(objeto)
        else:
            imagen_medica: ImagenMedica = mapeador.dto_a_entidad(objeto)
            if hasattr(objeto, 'id') and objeto.id:
                imagen_medica._id = objeto.id
            return imagen_medica


@dataclass
class FabricaProcesamientoImagen(Fabrica):
    def crear_objeto(self, objeto: any, mapeador: Mapeador = None) -> any:
        if mapeador.obtener_tipo() == ImagenMedica.__class__:
            fabrica_imagen_medica = _FabricaProcesamientoImagen()
            return fabrica_imagen_medica.crear_objeto(objeto, mapeador)
