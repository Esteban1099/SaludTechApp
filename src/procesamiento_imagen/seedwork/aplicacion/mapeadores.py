from abc import ABC, abstractmethod

from src.procesamiento_imagen.seedwork.aplicacion.dto import DTO


class Mapeador(ABC):
    @abstractmethod
    def externo_a_dto(self, externo: any) -> DTO:
        ...

    @abstractmethod
    def dto_a_externo(self, dto: DTO) -> any:
        ...
