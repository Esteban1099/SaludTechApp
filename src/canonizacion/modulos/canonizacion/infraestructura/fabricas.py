from dataclasses import dataclass

from src.sta.modulos.ingesta_automatizada.dominio.repositorios import RepositorioImagenesMedicas
from src.sta.modulos.ingesta_automatizada.infraestructura.repositorios import RepositorioImagenesMedicasMySQL
from src.sta.seedwork.aplicacion.mapeadores import Mapeador
from src.sta.seedwork.dominio.excepciones import ExcepcionFabrica
from src.sta.seedwork.dominio.fabricas import Fabrica
from src.sta.seedwork.dominio.repositorios import Repositorio


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, objeto: type, mapeador: Mapeador = None) -> Repositorio:
        if objeto == RepositorioImagenesMedicas.__class__:
            return RepositorioImagenesMedicasMySQL()
        else:
            raise ExcepcionFabrica()
