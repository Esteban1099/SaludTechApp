from dataclasses import dataclass

from src.canonizacion.modulos.canonizacion.dominio.fabricas import FabricaCanonizacion
from src.canonizacion.modulos.canonizacion.dominio.repositorios import RepositorioImagenesMedicas
from src.canonizacion.modulos.canonizacion.infraestructura.fabricas import FabricaRepositorio
from src.canonizacion.seedwork.aplicacion.comandos import Comando, ComandoHandler
from src.canonizacion.seedwork.aplicacion.comandos import ejecutar_comando as comando
from src.canonizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
import logging

logger = logging.getLogger(__name__)

@dataclass
class EliminarImagenMedica(Comando):
    id: str


class EliminarImagenMedicaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_canonizacion: FabricaCanonizacion = FabricaCanonizacion()


class EliminarImagenMedicaHandler(EliminarImagenMedicaBaseHandler):
    def handle(self, comando: EliminarImagenMedica):
        logger.info(f'Eliminando imagen médica con ID: {comando.id}')
        
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesMedicas.__class__)
        
        try:
            # Intentar obtener la imagen para verificar si existe
            imagen = repositorio.obtener_por_id(comando.id)
            
            # Si existe, eliminarla
            UnidadTrabajoPuerto.registrar_batch(repositorio.eliminar, comando.id)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()
            
            logger.info(f'Imagen médica con ID {comando.id} eliminada correctamente')
        except Exception as e:
            logger.warning(f'No se pudo eliminar la imagen con ID {comando.id}: {str(e)}')
            # No lanzamos excepción, ya que es posible que la imagen no exista
            # y eso es un comportamiento esperado en algunos casos


@comando.register(EliminarImagenMedica)
def ejecutar_comando_eliminar_imagen_medica(comando: EliminarImagenMedica):
    handler = EliminarImagenMedicaHandler()
    handler.handle(comando) 