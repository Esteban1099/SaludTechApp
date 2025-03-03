from dataclasses import dataclass

from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica
from src.canonizacion.seedwork.dominio.entidades import Entidad
from src.canonizacion.seedwork.dominio.fabricas import Fabrica
from src.canonizacion.seedwork.dominio.mapeadores import Mapeador


@dataclass
class _FabricaImagenMedica(Fabrica):
    def crear_objeto(self, objeto: any, mapeador: Mapeador = None) -> any:
        if isinstance(objeto, Entidad):
            return mapeador.entidad_a_dto(objeto)
        else:
            imagen_medica: ImagenMedica = mapeador.dto_a_entidad(objeto)
            return imagen_medica


@dataclass
class FabricaCanonizacion(Fabrica):
    def crear_objeto(self, objeto: any, mapeador: Mapeador = None) -> any:
        if mapeador.obtener_tipo() == ImagenMedica.__class__:
            fabrica_imagen_medica = _FabricaImagenMedica()
            return fabrica_imagen_medica.crear_objeto(objeto, mapeador)
