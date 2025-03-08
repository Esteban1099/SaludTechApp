from uuid import UUID

from src.canonizacion.config.db import db
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica
from src.canonizacion.modulos.canonizacion.dominio.fabricas import FabricaCanonizacion
from src.canonizacion.modulos.canonizacion.dominio.repositorios import RepositorioImagenesMedicas
from src.canonizacion.modulos.canonizacion.infraestructura.dto import ImagenMedicaDTO
from src.canonizacion.modulos.canonizacion.infraestructura.mapeadores import MapeadorImagenMedicaDTOEntity


class RepositorioImagenesMedicasMySQL(RepositorioImagenesMedicas):
    def __init__(self):
        self._fabrica_canonizacion: FabricaCanonizacion = FabricaCanonizacion()

    def obtener_por_id(self, id: UUID) -> ImagenMedica:
        imagen_medica_dto = db.session.query(ImagenMedicaDTO).filter_by(id=str(id)).one()
        return self._fabrica_canonizacion.crear_objeto(imagen_medica_dto, MapeadorImagenMedicaDTOEntity())

    def obtener_todos(self) -> list[ImagenMedica]:
        # TODO
        raise NotImplementedError

    def agregar(self, imagen_medica: ImagenMedica):
        imagen_medica_dto = self._fabrica_canonizacion.crear_objeto(imagen_medica,
                                                                    MapeadorImagenMedicaDTOEntity())
        db.session.add(imagen_medica_dto)
        
    def eliminar(self, id: UUID):
        imagen_medica_dto = db.session.query(ImagenMedicaDTO).filter_by(id=str(id)).first()
        if imagen_medica_dto:
            db.session.delete(imagen_medica_dto)
