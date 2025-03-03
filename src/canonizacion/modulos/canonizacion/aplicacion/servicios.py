from src.canonizacion.modulos.canonizacion.aplicacion.dto import ImagenMedicaDTO
from src.canonizacion.modulos.canonizacion.aplicacion.mapeadores import MapeadorImagenMedicaDTOEntity
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica
from src.canonizacion.modulos.canonizacion.dominio.fabricas import FabricaCanonizacion
from src.canonizacion.modulos.canonizacion.dominio.repositorios import RepositorioImagenesMedicas
from src.canonizacion.modulos.canonizacion.infraestructura.fabricas import FabricaRepositorio
from src.canonizacion.seedwork.aplicacion.servicio import Servicio


class ServicioImagenMedica(Servicio):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_ingesta_automatizada: FabricaCanonizacion = FabricaCanonizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_ingesta_automatizada(self):
        return self._fabrica_ingesta_automatizada

    def crear_imagen_medica(self, imagen_medica_dto: ImagenMedicaDTO) -> ImagenMedicaDTO:
        imagen_medica: ImagenMedica = self.fabrica_ingesta_automatizada.crear_objeto(imagen_medica_dto,
                                                                                     MapeadorImagenMedicaDTOEntity())
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesMedicas.__class__)
        repositorio.agregar(imagen_medica)
        result = self.fabrica_ingesta_automatizada.crear_objeto(imagen_medica, MapeadorImagenMedicaDTOEntity())
        return result
