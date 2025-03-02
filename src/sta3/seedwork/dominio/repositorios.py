from abc import ABC, abstractmethod
from uuid import UUID

from src.sta3.seedwork.dominio.entidades import Entidad


class Repositorio(ABC):
    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Entidad:
        ...

    @abstractmethod
    def obtener_todos(self) -> list[Entidad]:
        ...

    @abstractmethod
    def agregar(self, entidad: Entidad):
        ...
