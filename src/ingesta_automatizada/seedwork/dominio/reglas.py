from abc import ABC, abstractmethod


class ReglaNegocio(ABC):
    __mensaje: str = "Regla de negocio invalida"

    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def mensaje_error(self) -> str:
        return self.__mensaje

    @abstractmethod
    def es_valido(self) -> bool:
        ...

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__mensaje}"


class IdEntidadEsInmutable(ReglaNegocio):
    entidad: object

    def __init__(self, entidad, mensaje='El identificador de la entidad debe ser inmutable'):
        super().__init__(mensaje)
        self.entidad = entidad

    def es_valido(self) -> bool:
        try:
            if self.entidad._id:
                return True
        except AttributeError:
            return True
