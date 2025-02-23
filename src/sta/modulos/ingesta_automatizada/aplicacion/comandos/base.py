from src.sta.modulos.ingesta_automatizada.dominio.fabricas import FabricaIngestaAutomatizada
from src.sta.modulos.ingesta_automatizada.infraestructura.fabricas import FabricaRepositorio
from src.sta.seedwork.aplicacion.comandos import ComandoHandler


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
