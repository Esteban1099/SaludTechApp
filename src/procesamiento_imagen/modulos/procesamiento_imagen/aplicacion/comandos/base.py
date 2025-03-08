from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.fabricas import FabricaProcesamientoImagen
from src.procesamiento_imagen.modulos.procesamiento_imagen.infraestructura.fabricas import FabricaRepositorio
from src.procesamiento_imagen.seedwork.aplicacion.comandos import ComandoHandler


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

class EliminarImagenMedicaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_procesamiento_imagen: FabricaProcesamientoImagen = FabricaProcesamientoImagen()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_procesamiento_imagen(self):
        return self._fabrica_procesamiento_imagen
