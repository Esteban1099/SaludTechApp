from uuid import UUID

from src.ingesta_automatizada.config.db import db
from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.entidades import ImagenMedica
from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.fabricas import FabricaIngestaAutomatizada
from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.repositorios import RepositorioImagenesMedicas
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.dto import ImagenMedicaDTO
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.mapeadores import \
    MapeadorImagenMedicaDTOEntity
from src.ingesta_automatizada.seedwork.dominio.excepciones import ExcepcionDominio


class RepositorioImagenesMedicasMySQL(RepositorioImagenesMedicas):
    def eliminar(self, imagen_medica: ImagenMedica):
        imagen_medica_dto = db.session.query(ImagenMedicaDTO).filter_by(id=str(imagen_medica.id)).first()
        db.session.delete(imagen_medica_dto)
        db.session.commit()

    def __init__(self):
        self._fabrica_ingesta_automatizada: FabricaIngestaAutomatizada = FabricaIngestaAutomatizada()

    def obtener_por_id(self, id: UUID) -> ImagenMedica:
        imagen_medica_dto = db.session.query(ImagenMedicaDTO).filter_by(id=id).first()
        if imagen_medica_dto:
            return self._fabrica_ingesta_automatizada.crear_objeto(imagen_medica_dto, MapeadorImagenMedicaDTOEntity())
        else:
            raise ExcepcionDominio(f"No se encontró una imagen médica con id {id}")

    def obtener_todos(self) -> list[ImagenMedica]:
        # TODO
        raise NotImplementedError

    def agregar(self, imagen_medica: ImagenMedica):
        imagen_medica_dto = self._fabrica_ingesta_automatizada.crear_objeto(imagen_medica,
                                                                            MapeadorImagenMedicaDTOEntity())
        db.session.add(imagen_medica_dto)
        db.session.commit()
