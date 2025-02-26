from abc import ABC, abstractmethod
from uuid import UUID
from .entidades import ImagenCanonizada

class RepositorioImagenesCanonizadas(ABC):
    @abstractmethod
    def obtener_por_id(self, id: UUID) -> ImagenCanonizada:
        ...

    @abstractmethod
    def obtener_todos(self) -> list[ImagenCanonizada]:
        ...

    @abstractmethod
    def agregar(self, imagen: ImagenCanonizada):
        ... 