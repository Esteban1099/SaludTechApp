from src.sta.seedwork.aplicacion.comandos import Comando
from src.sta.modulos.ingesta_automatizada.aplicacion.dto import RegionAnatomicaDTO, DiagnosticoDTO, ImagenMedicaDTO
from src.sta.modulos.ingesta_automatizada.aplicacion.comandos.base import AgregarImagenMedicaBaseHandler
from dataclasses import dataclass
from src.sta.seedwork.aplicacion.comandos import ejecutar_comando as comando
from src.sta.modulos.ingesta_automatizada.dominio.entidades import ImagenMedica
from src.sta.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from src.sta.modulos.ingesta_automatizada.aplicacion.mapeadores import MapeadorImagenMedicaDTOEntity
from src.sta.modulos.ingesta_automatizada.infraestructura.repositorios import RepositorioImagenesMedicas
from src.sta.modulos.ingesta_automatizada.infraestructura.despachadores import Despachador
from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import (
    EventoImagenMedicaAgregada, 
    ImagenMedicaAgregadaPayload,
    RegionAnatomicaRecord,
    DiagnosticoRecord,
    DemografiaRecord,
    AtributoRecord
)
from pulsar.schema import AvroSchema


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

        # Publicar el evento de imagen médica agregada
        despachador = Despachador()

        # Mapear regiones anatómicas
        regiones_anatomicas = []
        for region in comando.regiones_anatomicas:
            region_record = RegionAnatomicaRecord(
                id=str(region.id),
                categoria=str(region.categoria),
                especificacion=str(region.especificacion)
            )
            regiones_anatomicas.append(region_record)

        # Mapear atributos del diagnóstico
        atributos = []
        for atributo in comando.diagnostico.atributos:
            atributo_record = AtributoRecord(
                id=str(atributo.id),
                nombre=str(atributo.nombre),
                descripcion=str(atributo.descripcion)
            )
            atributos.append(atributo_record)

        # Mapear demografía
        demografia = DemografiaRecord(
            id=str(comando.diagnostico.demografia.id),
            edad=comando.diagnostico.demografia.edad,
            grupo_edad=str(comando.diagnostico.demografia.grupo_edad),
            sexo=str(comando.diagnostico.demografia.sexo),
            etnicidad=str(comando.diagnostico.demografia.etnicidad)
        )

        # Mapear diagnóstico
        diagnostico = DiagnosticoRecord(
            id=str(comando.diagnostico.id),
            nombre=str(comando.diagnostico.nombre),
            descripcion=str(comando.diagnostico.descripcion),
            demografia=demografia,
            atributos=atributos
        )

        payload = ImagenMedicaAgregadaPayload(
            id=str(imagen_medica.id),
            modalidad=str(imagen_medica.modalidad),
            fecha_creacion=str(imagen_medica.fecha_creacion),
            regiones_anatomicas=regiones_anatomicas,
            diagnostico=diagnostico
        )
        evento = EventoImagenMedicaAgregada(data=payload)
        despachador._publicar_mensaje(evento, "eventos-imagen-medica", AvroSchema(EventoImagenMedicaAgregada))


@comando.register(AgregarImagenMedica)
def ejecutar_comando_agregar_imagen_medica(comando: AgregarImagenMedica):
    handler = AgregarImagenMedicaHandler()
    handler.handle(comando)
