from uuid import UUID

from src.sta.config.db import db
from src.sta.modulos.ingesta_automatizada.infraestructura.mapeadores import MapeadorImagenMedicaDTOEntity
from src.sta.modulos.ingesta_automatizada.dominio.entidades import ImagenMedica
from src.sta.modulos.ingesta_automatizada.dominio.fabricas import FabricaIngestaAutomatizada
from src.sta.modulos.ingesta_automatizada.dominio.repositorios import RepositorioImagenesMedicas


class RepositorioImagenesMedicasMySQL(RepositorioImagenesMedicas):
    def __init__(self):
        self._fabrica_ingesta_automatizada: FabricaIngestaAutomatizada = FabricaIngestaAutomatizada()

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
