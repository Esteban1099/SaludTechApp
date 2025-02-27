from dataclasses import dataclass

from src.sta3.modulos.procesamiento_imagen.dominio.repositorios import RepositorioImagenesMedicas
from src.sta3.modulos.procesamiento_imagen.infraestructura.repositorios import RepositorioImagenesMedicasMySQL
from src.sta3.seedwork.aplicacion.mapeadores import Mapeador
from src.sta3.seedwork.dominio.excepciones import ExcepcionFabrica
from src.sta3.seedwork.dominio.fabricas import Fabrica
from src.sta3.seedwork.dominio.repositorios import Repositorio


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, objeto: type, mapeador: Mapeador = None) -> Repositorio:
        if objeto == RepositorioImagenesMedicas.__class__:
            return RepositorioImagenesMedicasMySQL()
        else:
            raise ExcepcionFabrica()
