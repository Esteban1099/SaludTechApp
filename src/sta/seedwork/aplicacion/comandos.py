from abc import ABC, abstractmethod
from functools import singledispatch


class Comando:
    ...


class ComandoHandler(ABC):
    @abstractmethod
    def handle(selfself, comando: Comando):
        raise NotImplementedError()


@singledispatch
def ejecutar_comando(comando):
    raise NotImplementedError(f'No existe implementación para el comando de tipo {type(comando).__name__}')
