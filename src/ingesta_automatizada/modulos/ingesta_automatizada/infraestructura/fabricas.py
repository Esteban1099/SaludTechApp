from dataclasses import dataclass

from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.repositorios import RepositorioImagenesMedicas
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.repositorios import \
    RepositorioImagenesMedicasMySQL
from src.ingesta_automatizada.seedwork.aplicacion.mapeadores import Mapeador
from src.ingesta_automatizada.seedwork.dominio.excepciones import ExcepcionFabrica
from src.ingesta_automatizada.seedwork.dominio.fabricas import Fabrica
from src.ingesta_automatizada.seedwork.dominio.repositorios import Repositorio


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, objeto: type, mapeador: Mapeador = None) -> Repositorio:
        if objeto == RepositorioImagenesMedicas.__class__:
            return RepositorioImagenesMedicasMySQL()
        else:
            raise ExcepcionFabrica()
