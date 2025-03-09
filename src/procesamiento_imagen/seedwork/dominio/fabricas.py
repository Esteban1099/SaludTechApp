from abc import ABC, abstractmethod

from src.procesamiento_imagen.seedwork.aplicacion.mapeadores import Mapeador


class Fabrica(ABC):
    @abstractmethod
    def crear_objeto(self, objeto: any, mapeador: Mapeador = None) -> any:
        ...
