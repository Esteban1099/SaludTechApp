from dataclasses import dataclass

from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.mapeadores import MapeadorImagenMedicaDTOEntity
from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.queries.base import ImagenMedicaQueryBaseHandler
from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.repositorios import RepositorioImagenesMedicas
from src.ingesta_automatizada.seedwork.aplicacion.queries import Query, QueryResultado
from src.ingesta_automatizada.seedwork.aplicacion.queries import ejecutar_query as query


@dataclass
class ObtenerImagenMedica(Query):
    id: str


class ObtenerImagenMedicaHandler(ImagenMedicaQueryBaseHandler):
    def handle(self, query: ObtenerImagenMedica) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesMedicas.__class__)
        imagen_medica = self.fabrica_ingesta_automatizada.crear_objeto(repositorio.obtener_por_id(query.id),
                                                                       MapeadorImagenMedicaDTOEntity())
        return QueryResultado(resultado=imagen_medica)


@query.register(ObtenerImagenMedica)
def ejecutar_query_obtener_imagen_medica(query: ObtenerImagenMedica):
    handler = ObtenerImagenMedicaHandler()
    return handler.handle(query)
