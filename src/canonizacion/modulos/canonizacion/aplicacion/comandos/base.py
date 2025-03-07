from src.canonizacion.modulos.canonizacion.dominio.fabricas import FabricaCanonizacion
from src.canonizacion.modulos.canonizacion.infraestructura.fabricas import FabricaRepositorio
from src.canonizacion.seedwork.aplicacion.comandos import ComandoHandler


class CanonizarImagenMedicaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingestion_automatizada: FabricaCanonizacion = FabricaCanonizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_ingestion_automatizada(self):
        return self._fabrica_ingestion_automatizada
