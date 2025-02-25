from uuid import UUID
from src.sta.config.db import db
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenCanonizada
from src.canonizacion.modulos.canonizacion.dominio.repositorios import RepositorioImagenesCanonizadas
from src.canonizacion.modulos.canonizacion.infraestructura.mapeadores import MapeadorImagenCanonizadaDTOEntity

class RepositorioImagenesCanonizadasPostgres(RepositorioImagenesCanonizadas):
    def __init__(self):
        self._mapeador = MapeadorImagenCanonizadaDTOEntity()

    def obtener_por_id(self, id: UUID) -> ImagenCanonizada:
        # TODO: Implementar cuando sea necesario
        raise NotImplementedError

    def obtener_todos(self) -> list[ImagenCanonizada]:
        # TODO: Implementar cuando sea necesario
        raise NotImplementedError

    def agregar(self, imagen: ImagenCanonizada):
        imagen_dto = self._mapeador.entidad_a_dto(imagen)
        db.session.add(imagen_dto)
        db.session.commit() 