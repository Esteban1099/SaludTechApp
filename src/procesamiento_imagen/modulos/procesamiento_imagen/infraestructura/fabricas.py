from dataclasses import dataclass

from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.repositorios import RepositorioImagenesMedicas
from src.procesamiento_imagen.modulos.procesamiento_imagen.infraestructura.repositorios import RepositorioImagenesMedicasMySQL
from src.procesamiento_imagen.seedwork.aplicacion.mapeadores import Mapeador
from src.procesamiento_imagen.seedwork.dominio.excepciones import ExcepcionFabrica
from src.procesamiento_imagen.seedwork.dominio.fabricas import Fabrica
from src.procesamiento_imagen.seedwork.dominio.repositorios import Repositorio


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, objeto: type, mapeador: Mapeador = None) -> Repositorio:
        if objeto == RepositorioImagenesMedicas.__class__:
            return RepositorioImagenesMedicasMySQL()
        else:
            raise ExcepcionFabrica()
