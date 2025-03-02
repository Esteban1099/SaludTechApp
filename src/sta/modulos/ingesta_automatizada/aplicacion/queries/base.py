from src.sta.modulos.ingesta_automatizada.dominio.fabricas import FabricaIngestaAutomatizada
from src.sta.modulos.ingesta_automatizada.infraestructura.fabricas import FabricaRepositorio
from src.sta.seedwork.aplicacion.queries import QueryHandler


class ImagenMedicaQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingesta_automatizada: FabricaIngestaAutomatizada = FabricaIngestaAutomatizada()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_ingesta_automatizada(self):
        return self._fabrica_ingesta_automatizada
