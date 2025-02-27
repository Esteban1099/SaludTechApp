from src.sta3.modulos.procesamiento_imagen.dominio.fabricas import FabricaProcesamientoImagen
from src.sta3.modulos.procesamiento_imagen.infraestructura.fabricas import FabricaRepositorio
from src.sta3.seedwork.aplicacion.comandos import ComandoHandler


class ProcesarImagenMedicaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_procesamiento_imagen: FabricaProcesamientoImagen = FabricaProcesamientoImagen()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_procesamiento_imagen(self):
        return self._fabrica_procesamiento_imagen
