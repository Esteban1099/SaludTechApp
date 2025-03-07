from dataclasses import dataclass

from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.comandos.base import \
    EliminarImagenMedicaBaseHandler
from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.entidades import ImagenMedica
from src.ingesta_automatizada.seedwork.aplicacion.comandos import Comando, ejecutar_comando
from src.ingesta_automatizada.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.repositorios import \
    RepositorioImagenesMedicas


@dataclass
class EliminarImagenMedica(Comando):
    id: str


class EliminarImagenMedicaHandler(EliminarImagenMedicaBaseHandler):
    def handle(self, comando: EliminarImagenMedica):
        imagen_medica: ImagenMedica = ImagenMedica()
        imagen_medica.eliminar_imagen_medica(comando.id)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesMedicas.__class__)

        repositorio.obtener_por_id(comando.id)
        UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, imagen_medica)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@ejecutar_comando.register(EliminarImagenMedica)
def ejecutar_comando_eliminar_imagen_medica(comando: EliminarImagenMedica):
    handler = EliminarImagenMedicaHandler()
    handler.handle(comando)
