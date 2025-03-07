from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.fabricas import FabricaIngestaAutomatizada
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.fabricas import FabricaRepositorio
from src.ingesta_automatizada.seedwork.aplicacion.comandos import ComandoHandler


class AgregarImagenMedicaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingestion_automatizada: FabricaIngestaAutomatizada = FabricaIngestaAutomatizada()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_ingestion_automatizada(self):
        return self._fabrica_ingestion_automatizada


class EliminarImagenMedicaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingestion_automatizada: FabricaIngestaAutomatizada = FabricaIngestaAutomatizada()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_ingestion_automatizada(self):
        return self._fabrica_ingestion_automatizada
