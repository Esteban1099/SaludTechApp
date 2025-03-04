from dataclasses import dataclass

from src.canonizacion.modulos.canonizacion.aplicacion.comandos.base import CanonizarImagenMedicaBaseHandler
from src.canonizacion.modulos.canonizacion.aplicacion.dto import RegionAnatomicaDTO, DiagnosticoDTO, ImagenMedicaDTO
from src.canonizacion.modulos.canonizacion.aplicacion.mapeadores import MapeadorImagenMedicaDTOEntity
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.despachadores import Despachador
from src.canonizacion.modulos.canonizacion.infraestructura.repositorios import RepositorioImagenesMedicas
from src.canonizacion.seedwork.aplicacion.comandos import Comando
from src.canonizacion.seedwork.aplicacion.comandos import ejecutar_comando
from src.canonizacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto


@dataclass
class CanonizarImagenMedica(Comando):
    id: str
    modalidad: str
    fecha_creacion: str
    regiones_anatomicas: list[RegionAnatomicaDTO]
    diagnostico: DiagnosticoDTO


class CanonizarImagenMedicaHandler(CanonizarImagenMedicaBaseHandler):
    def handle(self, comando: CanonizarImagenMedica):
        imagen_medica_dto = ImagenMedicaDTO(
            modalidad=comando.modalidad,
            fecha_creacion=comando.fecha_creacion,
            regiones_anatomicas=comando.regiones_anatomicas,
            diagnostico=comando.diagnostico)

        imagen_medica: ImagenMedica = self.fabrica_ingestion_automatizada.crear_objeto(imagen_medica_dto,
                                                                                       MapeadorImagenMedicaDTOEntity())
        imagen_medica.agregar_imagen_medica(imagen_medica)
        imagen_medica.canonizar_imagen_medica()

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesMedicas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen_medica)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        despachador = Despachador()
        despachador.publicar_evento(evento=imagen_medica.eventos[-1], topico='eventos-imagen-canonizada')

        print(f'Imagen médica canonizada y evento publicado: {imagen_medica.id}')


@ejecutar_comando.register(CanonizarImagenMedica)
def ejecutar_comando_canonizar_imagen_medica(comando: CanonizarImagenMedica):
    handler = CanonizarImagenMedicaHandler()
    handler.handle(comando) 