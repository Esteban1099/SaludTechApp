from dataclasses import dataclass

from src.sta3.modulos.procesamiento_imagen.aplicacion.comandos.base import ProcesarImagenMedicaBaseHandler
from src.sta3.modulos.procesamiento_imagen.aplicacion.dto import RegionAnatomicaDTO, DiagnosticoDTO, ImagenMedicaDTO
from src.sta3.modulos.procesamiento_imagen.aplicacion.mapeadores import MapeadorImagenMedicaDTOEntity
from src.sta3.modulos.procesamiento_imagen.dominio.entidades import ImagenMedica
from src.sta3.modulos.procesamiento_imagen.infraestructura.repositorios import RepositorioImagenesMedicas
from src.sta3.seedwork.aplicacion.comandos import Comando
from src.sta3.seedwork.aplicacion.comandos import ejecutar_comando
from src.sta3.seedwork.infraestructura.uow import UnidadTrabajoPuerto


@dataclass
class ProcesarImagenMedica(Comando):
    id: str
    url: str
    modalidad: str
    fecha_creacion: str
    regiones_anatomicas: list[RegionAnatomicaDTO]
    diagnostico: DiagnosticoDTO


class ProcesarImagenMedicaHandler(ProcesarImagenMedicaBaseHandler):
    def handle(self, comando: ProcesarImagenMedica):
        imagen_medica_dto = ImagenMedicaDTO(
            id=comando.id,
            url=comando.url,
            modalidad=comando.modalidad,
            fecha_creacion=comando.fecha_creacion,
            regiones_anatomicas=comando.regiones_anatomicas,
            diagnostico=comando.diagnostico)

        imagen_medica: ImagenMedica = self.fabrica_procesamiento_imagen.crear_objeto(imagen_medica_dto,
                                                                                       MapeadorImagenMedicaDTOEntity())
        imagen_medica.procesar_imagen_medica(imagen_medica)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesMedicas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen_medica)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@ejecutar_comando.register(ProcesarImagenMedica)
def ejecutar_comando_procesar_imagen_medica(comando: ProcesarImagenMedica):
    handler = ProcesarImagenMedicaHandler()
    handler.handle(comando)
