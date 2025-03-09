from abc import ABC, abstractmethod

from src.procesamiento_imagen.seedwork.dominio.entidades import Entidad


class Mapeador(ABC):
    @abstractmethod
    def obtener_tipo(self) -> type:
        ...

    @abstractmethod
    def entidad_a_dto(self, entidad: Entidad) -> any:
        ...

    @abstractmethod
    def dto_a_entidad(self, dto: any) -> Entidad:
        ...
