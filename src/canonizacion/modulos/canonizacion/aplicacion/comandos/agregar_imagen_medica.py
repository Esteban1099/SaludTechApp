from dataclasses import dataclass

from src.canonizacion.modulos.canonizacion.aplicacion.comandos.base import AgregarImagenMedicaBaseHandler
from src.canonizacion.modulos.canonizacion.aplicacion.dto import RegionAnatomicaDTO, DiagnosticoDTO, ImagenMedicaDTO
from src.canonizacion.modulos.canonizacion.aplicacion.mapeadores import MapeadorImagenMedicaDTOEntity
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.repositorios import RepositorioImagenesMedicas
from src.canonizacion.seedwork.aplicacion.comandos import Comando
from src.canonizacion.seedwork.aplicacion.comandos import ejecutar_comando
from src.canonizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto


@dataclass
class AgregarImagenMedica(Comando):
    id: str
    modalidad: str
    fecha_creacion: str
    regiones_anatomicas: list[RegionAnatomicaDTO]
    diagnostico: DiagnosticoDTO


class AgregarImagenMedicaHandler(AgregarImagenMedicaBaseHandler):
    def handle(self, comando: AgregarImagenMedica):
        imagen_medica_dto = ImagenMedicaDTO(
            modalidad=comando.modalidad,
            fecha_creacion=comando.fecha_creacion,
            regiones_anatomicas=comando.regiones_anatomicas,
            diagnostico=comando.diagnostico)

        imagen_medica: ImagenMedica = self.fabrica_ingestion_automatizada.crear_objeto(imagen_medica_dto,
                                                                                       MapeadorImagenMedicaDTOEntity())
        imagen_medica.agregar_imagen_medica(imagen_medica)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesMedicas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen_medica)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@ejecutar_comando.register(AgregarImagenMedica)
def ejecutar_comando_agregar_imagen_medica(comando: AgregarImagenMedica):
    handler = AgregarImagenMedicaHandler()
    handler.handle(comando)
