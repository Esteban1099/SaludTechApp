from src.procesamiento_imagen.modulos.procesamiento_imagen.aplicacion.dto import ImagenMedicaDTO
from src.procesamiento_imagen.modulos.procesamiento_imagen.aplicacion.mapeadores import MapeadorImagenMedicaDTOEntity
from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.entidades import ImagenMedica
from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.fabricas import FabricaProcesamientoImagen
from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.repositorios import RepositorioImagenesMedicas
from src.procesamiento_imagen.modulos.procesamiento_imagen.infraestructura.fabricas import FabricaRepositorio
from src.procesamiento_imagen.seedwork.aplicacion.servicio import Servicio


class ServicioImagenMedica(Servicio):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_procesamiento_imagen: FabricaProcesamientoImagen = FabricaProcesamientoImagen()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_procesamiento_imagen(self):
        return self._fabrica_procesamiento_imagen

    def procesar_imagen_medica(self, imagen_medica_dto: ImagenMedicaDTO) -> ImagenMedicaDTO:
        imagen_medica: ImagenMedica = self._fabrica_procesamiento_imagen.crear_objeto(imagen_medica_dto,
                                                                                     MapeadorImagenMedicaDTOEntity())
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesMedicas.__class__)
        repositorio.agregar(imagen_medica)
        result = self._fabrica_procesamiento_imagen.crear_objeto(imagen_medica, MapeadorImagenMedicaDTOEntity())
        return result
