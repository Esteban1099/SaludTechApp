from uuid import UUID

from src.canonizacion.config.db import db
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica
from src.canonizacion.modulos.canonizacion.dominio.fabricas import FabricaCanonizacion
from src.canonizacion.modulos.canonizacion.dominio.repositorios import RepositorioImagenesMedicas
from src.canonizacion.modulos.canonizacion.infraestructura.mapeadores import MapeadorImagenMedicaDTOEntity


class RepositorioImagenesMedicasMySQL(RepositorioImagenesMedicas):
    def __init__(self):
        self._fabrica_ingesta_automatizada: FabricaCanonizacion = FabricaCanonizacion()

    def obtener_por_id(self, id: UUID) -> ImagenMedica:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[ImagenMedica]:
        # TODO
        raise NotImplementedError

    def agregar(self, imagen_medica: ImagenMedica):
        imagen_medica_dto = self._fabrica_ingesta_automatizada.crear_objeto(imagen_medica,
                                                                            MapeadorImagenMedicaDTOEntity())
        db.session.add(imagen_medica_dto)
        db.session.commit()
