from abc import ABC, abstractmethod

from src.sta3.seedwork.aplicacion.comandos import Comando
from src.sta3.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion


class Mapeador(ABC):
    @abstractmethod
    def comando_a_comando_integracion(self, comando: Comando) -> ComandoIntegracion:
        ...

    @abstractmethod
    def comando_integracion_a_comando(self, comando_integracion: ComandoIntegracion) -> Comando:
        ...
