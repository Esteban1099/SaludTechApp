from abc import ABC, abstractmethod

from src.sta3.seedwork.aplicacion.mapeadores import Mapeador


class Fabrica(ABC):
    @abstractmethod
    def crear_objeto(self, objeto: any, mapeador: Mapeador = None) -> any:
        ...
