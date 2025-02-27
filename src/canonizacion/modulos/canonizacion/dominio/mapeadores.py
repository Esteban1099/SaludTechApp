from src.canonizacion.modulos.canonizacion.aplicacion.comandos.agregar_imagen_medica import AgregarImagenMedica
from src.canonizacion.modulos.canonizacion.aplicacion.dto import DemografiaDTO, AtributoDTO, DiagnosticoDTO, \
    RegionAnatomicaDTO
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.comandos import DemografiaRecord, AtributoRecord, \
    DiagnosticoRecord, RegionAnatomicaRecord, ComandoAgregarImagenMedica, ComandoAgregarImagenMedicaPayload
from src.canonizacion.seedwork.infraestructura.mapeadores import Mapeador as InfMap


class MapeadorComandoAgregarImagenMedica(InfMap):
    def _procesar_demografia_dto(self, demografia_dto: DemografiaDTO):
        return DemografiaRecord(
            id=demografia_dto.id,
            edad=demografia_dto.edad,
            grupo_edad=demografia_dto.grupo_edad,
            sexo=demografia_dto.sexo,
            etnicidad=demografia_dto.etnicidad
        )

    def _procesar_atributos_dto(self, atributos_dto: list[AtributoDTO]):
        atributos_records = []
        for atributo_dto in atributos_dto:
            atributos_records.append(
                AtributoRecord(
                    id=str(atributo_dto.id),
                    nombre=atributo_dto.nombre,
                    descripcion=atributo_dto.descripcion
                )
            )
        return atributos_records

    def _procesar_diagnostico_dto(self, diagnostico_dto: DiagnosticoDTO):
        return DiagnosticoRecord(
            id=diagnostico_dto.id,
            nombre=diagnostico_dto.nombre,
            descripcion=diagnostico_dto.descripcion,
            demografia=self._procesar_demografia_dto(diagnostico_dto.demografia),
            atributos=self._procesar_atributos_dto(diagnostico_dto.atributos)
        )

    def _procesar_regiones_anatomicas_dto(self, regiones_anatomicas_dto: list[RegionAnatomicaDTO]):
        regiones_anatomicas_records = []
        for region_anatomica_dto in regiones_anatomicas_dto:
            regiones_anatomicas_records.append(
                RegionAnatomicaRecord(
                    categoria=region_anatomica_dto.categoria,
                    especificacion=region_anatomica_dto.especificacion
                )
            )
        return regiones_anatomicas_records

    def comando_a_comando_integracion(self, comando: AgregarImagenMedica) -> ComandoAgregarImagenMedica:
        return ComandoAgregarImagenMedica(
            data=ComandoAgregarImagenMedicaPayload(
                id=comando.id,
                modalidad=comando.modalidad,
                fecha_creacion=comando.fecha_creacion,
                diagnostico=self._procesar_diagnostico_dto(comando.diagnostico),
                regiones_anatomicas=self._procesar_regiones_anatomicas_dto(comando.regiones_anatomicas)
            )
        )

    def _procesar_demografia_record(self, demografia_record: DemografiaRecord):
        return DemografiaDTO(
            id=demografia_record.id,
            edad=demografia_record.edad,
            grupo_edad=demografia_record.grupo_edad,
            sexo=demografia_record.sexo,
            etnicidad=demografia_record.etnicidad
        )

    def _procesar_atributos_record(self, atributos_record: list[AtributoRecord]):
        atributos_dtos = []
        for atributo_record in atributos_record:
            atributos_dtos.append(
                AtributoDTO(
                    id=str(atributo_record.id),
                    nombre=atributo_record.nombre,
                    descripcion=atributo_record.descripcion
                )
            )
        return atributos_dtos

    def _procesar_diagnostico_record(self, diagnostico_record: DiagnosticoRecord):
        return DiagnosticoDTO(
            id=diagnostico_record.id,
            nombre=diagnostico_record.nombre,
            descripcion=diagnostico_record.descripcion,
            demografia=self._procesar_demografia_record(diagnostico_record.demografia),
            atributos=self._procesar_atributos_record(diagnostico_record.atributos)
        )

    def _procesar_regiones_anatomicas_record(self, regiones_anatomicas_record: list[RegionAnatomicaRecord]):
        regiones_anatomicas_dtos = []
        for region_anatomica_record in regiones_anatomicas_record:
            regiones_anatomicas_dtos.append(
                RegionAnatomicaDTO(
                    categoria=region_anatomica_record.categoria,
                    especificacion=region_anatomica_record.especificacion
                )
            )
        return regiones_anatomicas_dtos

    def comando_integracion_a_comando(self, comando_integracion: ComandoAgregarImagenMedica) -> AgregarImagenMedica:
        return AgregarImagenMedica(
            id=comando_integracion.data.id,
            modalidad=comando_integracion.data.modalidad,
            fecha_creacion=comando_integracion.data.fecha_creacion,
            regiones_anatomicas=self._procesar_regiones_anatomicas_record(comando_integracion.data.regiones_anatomicas),
            diagnostico=self._procesar_diagnostico_record(comando_integracion.data.diagnostico)
        )
