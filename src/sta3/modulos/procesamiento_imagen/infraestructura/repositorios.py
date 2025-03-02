from uuid import UUID

from src.sta3.config.db import db
from src.sta3.modulos.procesamiento_imagen.dominio.entidades import ImagenMedica
from src.sta3.modulos.procesamiento_imagen.dominio.fabricas import FabricaProcesamientoImagen
from src.sta3.modulos.procesamiento_imagen.dominio.repositorios import RepositorioImagenesMedicas
from src.sta3.modulos.procesamiento_imagen.infraestructura.mapeadores import MapeadorImagenMedicaDTOEntity


class RepositorioImagenesMedicasMySQL(RepositorioImagenesMedicas):
    def __init__(self):
        self._fabrica_procesamiento_imagen: FabricaProcesamientoImagen = FabricaProcesamientoImagen()

    def obtener_por_id(self, id: UUID) -> ImagenMedica:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[ImagenMedica]:
        # TODO
        raise NotImplementedError

    def agregar(self, imagen_medica: ImagenMedica):
        imagen_medica_dto = self._fabrica_procesamiento_imagen.crear_objeto(imagen_medica,
                                                                            MapeadorImagenMedicaDTOEntity())
        db.session.add(imagen_medica_dto)
        db.session.commit()
