from dataclasses import dataclass

from src.canonizacion.modulos.canonizacion.dominio.repositorios import RepositorioImagenesMedicas
from src.canonizacion.modulos.canonizacion.infraestructura.repositorios import RepositorioImagenesMedicasMySQL
from src.canonizacion.seedwork.aplicacion.mapeadores import Mapeador
from src.canonizacion.seedwork.dominio.excepciones import ExcepcionFabrica
from src.canonizacion.seedwork.dominio.fabricas import Fabrica
from src.canonizacion.seedwork.dominio.repositorios import Repositorio


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, objeto: type, mapeador: Mapeador = None) -> Repositorio:
        if objeto == RepositorioImagenesMedicas.__class__:
            return RepositorioImagenesMedicasMySQL()
        else:
            raise ExcepcionFabrica()
