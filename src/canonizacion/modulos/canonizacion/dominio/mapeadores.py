from linecache import clearcache

from src.canonizacion.modulos.canonizacion.aplicacion.comandos.canonizar_imagen_medica import CanonizarImagenMedica
from src.canonizacion.modulos.canonizacion.aplicacion.dto import DemografiaDTO, AtributoDTO, DiagnosticoDTO, RegionAnatomicaDTO, \
    ImagenMedicaDTO
from src.canonizacion.modulos.canonizacion.dominio.entidades import Demografia, Diagnostico, RegionAnatomica, Atributo, \
    ImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.comandos import DemografiaRecord, AtributoRecord, \
    DiagnosticoRecord, RegionAnatomicaRecord, ComandoCanonizarImagenMedica, ComandoCanonizarImagenMedicaPayload
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.eventos import ImagenMedicaAgregadaPayload
from src.canonizacion.seedwork.dominio.mapeadores import Mapeador as InfMap


class MapeadorComandoCanonizarImagenMedica(InfMap):
    def _procesar_demografia(self, demografia: Demografia) -> DemografiaDTO:
        demografia_dto = DemografiaDTO()
        demografia_dto.id = str(demografia.id)
        demografia_dto.edad = str(demografia.edad)
        demografia_dto.grupo_edad = str(demografia.grupo_edad)
        demografia_dto.sexo = str(demografia.sexo)
        demografia_dto.etnicidad = str(demografia.etnicidad)
        return demografia_dto

    def _procesar_diagnostico(self, diagnostico: Diagnostico) -> DiagnosticoDTO:
        diagnostico_dto = DiagnosticoDTO()
        diagnostico_dto.id = str(diagnostico.id)
        diagnostico_dto.nombre = diagnostico.nombre
        diagnostico_dto.descripcion = diagnostico.descripcion
        diagnostico_dto.demografia = self._procesar_demografia(diagnostico.demografia)
        diagnostico_dto.atributos = self._procesar_atributos(diagnostico.atributos)
        return diagnostico_dto

    def _procesar_atributos(self, atributos: list[Atributo]) -> list[AtributoDTO]:
        atributos_dto: list[AtributoDTO] = list()
        for atributo in atributos:
            atributo_dto = AtributoDTO()
            atributo_dto.id = str(atributo.id)
            atributo_dto.nombre = atributo.nombre
            atributo_dto.descripcion = atributo.descripcion
            atributos_dto.append(atributo_dto)
        return atributos_dto

    def _procesar_regiones_anatomicas(self, regiones_anatomicas: list[RegionAnatomica]) -> list[
        RegionAnatomicaDTO]:
        regiones_anatomicas_dto: list[RegionAnatomicaDTO] = list()
        for region_anatomica in regiones_anatomicas:
            region_anatomica_dto = RegionAnatomicaDTO()
            region_anatomica_dto.id = str(region_anatomica.id)
            region_anatomica_dto.categoria = str(region_anatomica.categoria)
            region_anatomica_dto.especificacion = region_anatomica.especificacion
            regiones_anatomicas_dto.append(region_anatomica_dto)
        return regiones_anatomicas_dto

    def _procesar_demografia_dto(self, demografia_dto: DemografiaDTO) -> Demografia:
        demografia = Demografia()
        demografia.edad = demografia_dto.edad
        demografia.grupo_edad = demografia_dto.grupo_edad
        demografia.sexo = demografia_dto.sexo
        demografia.etnicidad = demografia_dto.etnicidad
        return demografia

    def _procesar_diagnostico_dto(self, diagnostico_dto: DiagnosticoDTO) -> Diagnostico:
        diagnostico = Diagnostico()
        diagnostico.nombre = diagnostico_dto.nombre
        diagnostico.descripcion = diagnostico_dto.descripcion
        diagnostico.demografia = self._procesar_demografia_dto(diagnostico_dto.demografia)
        diagnostico.atributos = self._procesar_atributos_dto(diagnostico_dto.atributos)
        return diagnostico

    def _procesar_regiones_anatomicas_dto(self, regiones_anatomicas_dto: list[RegionAnatomicaDTO]) -> list[
        RegionAnatomica]:
        regiones_anatomicas: list[RegionAnatomica] = list()
        for region_anatomica_dto in regiones_anatomicas_dto:
            region_anatomica = RegionAnatomica()
            region_anatomica.categoria = region_anatomica_dto.categoria
            region_anatomica.especificacion = region_anatomica_dto.especificacion
            regiones_anatomicas.append(region_anatomica)
        return regiones_anatomicas

    def _procesar_atributos_dto(self, atributos_dto: list[AtributoDTO]) -> list[Atributo]:
        atributos: list[Atributo] = list()
        for atributo_dto in atributos_dto:
            atributo = Atributo()
            atributo.nombre = atributo_dto.nombre
            atributo.descripcion = atributo_dto.descripcion
            atributos.append(atributo)
        return atributos

    def obtener_tipo(self) -> type:
        return ImagenMedica.__class__

    def entidad_a_dto(self, imagen_medica: ImagenMedica) -> ImagenMedicaDTO:
        imagen_medica_dto = ImagenMedicaDTO()
        imagen_medica_dto.id = str(imagen_medica.id)
        imagen_medica_dto.fecha_creacion = imagen_medica.fecha_creacion
        imagen_medica_dto.modalidad = str(imagen_medica.modalidad)
        imagen_medica_dto.diagnostico = self._procesar_diagnostico(imagen_medica.diagnostico)
        imagen_medica_dto.regiones_anatomicas = self._procesar_regiones_anatomicas(imagen_medica.regiones_anatomicas)
        return imagen_medica_dto

    def dto_a_entidad(self, dto: ImagenMedicaDTO) -> ImagenMedica:
        imagen_medica = ImagenMedica()
        imagen_medica.id = dto.id
        imagen_medica.fecha_creacion = str(dto.fecha_creacion)
        imagen_medica.modalidad = dto.modalidad
        imagen_medica.diagnostico = self._procesar_diagnostico_dto(dto.diagnostico)
        imagen_medica.regiones_anatomicas = self._procesar_regiones_anatomicas_dto(dto.regiones_anatomicas)
        return imagen_medica

    def comando_a_comando_integracion(self, comando: CanonizarImagenMedica) -> ComandoCanonizarImagenMedica:
        return ComandoCanonizarImagenMedica(
            data=ComandoCanonizarImagenMedicaPayload(
                id=comando.data.id,
                modalidad=comando.data.modalidad,
                fecha_creacion=comando.data.fecha_creacion,
                regiones_anatomicas=[
                    RegionAnatomicaRecord(
                        id=str(region.id),
                        categoria=region.categoria,
                        especificacion=region.especificacion
                    ) for region in comando.data.regiones_anatomicas
                ] if comando.data.regiones_anatomicas else [],
                diagnostico=DiagnosticoRecord(
                    id=str(comando.data.diagnostico.id),
                    nombre=comando.data.diagnostico.nombre,
                    descripcion=comando.data.diagnostico.descripcion,
                    demografia=DemografiaRecord(
                        id=str(comando.data.diagnostico.demografia.id),
                        edad=comando.data.diagnostico.demografia.edad,
                        grupo_edad=comando.data.diagnostico.demografia.grupo_edad,
                        sexo=comando.data.diagnostico.demografia.sexo,
                        etnicidad=comando.data.diagnostico.demografia.etnicidad
                    ),
                    atributos=[
                        AtributoRecord(
                            id=str(atributo.id),
                            nombre=atributo.nombre,
                            descripcion=atributo.descripcion
                        ) for atributo in comando.data.diagnostico.atributos
                    ] if comando.data.diagnostico.atributos else []
                )
            )
        )

    def comando_integracion_a_comando(self, comando_integracion: ComandoCanonizarImagenMedica) -> CanonizarImagenMedica:
        return CanonizarImagenMedica(
            id=comando_integracion.data.id,
            modalidad=comando_integracion.data.modalidad,
            fecha_creacion=comando_integracion.data.fecha_creacion,
            regiones_anatomicas=[RegionAnatomicaDTO(
                id=region.id,
                categoria=region.categoria,
                especificacion=region.especificacion
            ) for region in comando_integracion.data.regiones_anatomicas],
            diagnostico=DiagnosticoDTO(
                id=comando_integracion.data.diagnostico.id,
                nombre=comando_integracion.data.diagnostico.nombre,
                descripcion=comando_integracion.data.diagnostico.descripcion,
                demografia=DemografiaDTO(
                    id=comando_integracion.data.diagnostico.demografia.id,
                    edad=comando_integracion.data.diagnostico.demografia.edad,
                    grupo_edad=comando_integracion.data.diagnostico.demografia.grupo_edad,
                    sexo=comando_integracion.data.diagnostico.demografia.sexo,
                    etnicidad=comando_integracion.data.diagnostico.demografia.etnicidad
                ),
                atributos=[AtributoDTO(
                    id=atributo.id,
                    nombre=atributo.nombre,
                    descripcion=atributo.descripcion
                ) for atributo in comando_integracion.data.diagnostico.atributos]
            )
        )

    def evento_a_comando(self, evento: ImagenMedicaAgregadaPayload) -> CanonizarImagenMedica:
        # Crear datos por defecto para el comando
        demografia_dto = DemografiaDTO(
            id="1",
            edad=0,
            grupo_edad="ADULTO",
            sexo="MASCULINO",
            etnicidad="LATINO"
        )

        diagnostico_dto = DiagnosticoDTO(
            id="1",
            nombre="Diagnóstico por defecto",
            descripcion="Descripción por defecto",
            demografia=demografia_dto,
            atributos=[]
        )

        # Inicializar correctamente regiones_anatomicas
        regiones_anatomicas_dto = (
            [RegionAnatomicaDTO(
                id="1",
                categoria="CABEZA_CUELLO",
                especificacion="Especificación por defecto"
            )]
            if evento.regiones_anatomicas is None else
            [RegionAnatomicaDTO(
                id=region.id,
                categoria=region.categoria,
                especificacion=region.especificacion
            ) for region in evento.regiones_anatomicas]
        )

        return CanonizarImagenMedica(
            id=evento.id,
            modalidad=evento.modalidad,
            fecha_creacion=evento.fecha_creacion,
            regiones_anatomicas=regiones_anatomicas_dto,
            diagnostico=diagnostico_dto
        )

