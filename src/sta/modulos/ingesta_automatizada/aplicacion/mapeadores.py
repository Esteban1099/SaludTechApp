from datetime import datetime

from src.sta.modulos.ingesta_automatizada.aplicacion.dto import ImagenMedicaDTO, DemografiaDTO, RegionAnatomicaDTO, \
    DiagnosticoDTO, AtributoDTO
from src.sta.modulos.ingesta_automatizada.dominio.entidades import ImagenMedica, Demografia, RegionAnatomica, \
    Diagnostico, Atributo
from src.sta.modulos.ingesta_automatizada.dominio.objetos_valor import Modalidad, GrupoEdad, Sexo, Etnia, \
    CategoriaAnatomica
from src.sta.seedwork.aplicacion.mapeadores import Mapeador as AplMap
from src.sta.seedwork.dominio.mapeadores import Mapeador as RepMap


class MapeadorImagenMedicaDTOJson(AplMap):

    def _procesar_demografia(self, demografia_externo: dict) -> DemografiaDTO:
        return DemografiaDTO(
            edad=demografia_externo.get('edad', int),
            grupo_edad=demografia_externo.get('grupo_edad', str),
            sexo=demografia_externo.get('sexo', str),
            etnicidad=demografia_externo.get('etnicidad', str)
        )

    def _procesar_diagnostico(self, diagnostico_externo: dict) -> DiagnosticoDTO:
        return DiagnosticoDTO(
            nombre=diagnostico_externo.get('nombre', str),
            descripcion=diagnostico_externo.get('descripcion', str),
            demografia=self._procesar_demografia(diagnostico_externo.get('demografia', dict)),
            atributos=self._procesar_atributos(diagnostico_externo.get('atributos', list))
        )

    def _procesar_regiones_anatomicas(self, regiones_anatomicas_externo: list) -> list[RegionAnatomicaDTO]:
        regiones_anatomicas_dto: list[RegionAnatomicaDTO] = list()
        for region_anatomica_externo in regiones_anatomicas_externo:
            region_anatomica_dto = RegionAnatomicaDTO(
                categoria=region_anatomica_externo.get('categoria'),
                especificacion=region_anatomica_externo.get('especificacion')
            )
            regiones_anatomicas_dto.append(region_anatomica_dto)
        return regiones_anatomicas_dto

    def _procesar_atributos(self, atributos_externo: list) -> list[AtributoDTO]:
        atributos_dto: list[AtributoDTO] = list()
        for atributo_externo in atributos_externo:
            atributo_dto = AtributoDTO(
                nombre=atributo_externo.get('nombre'),
                descripcion=atributo_externo.get('descripcion')
            )
            atributos_dto.append(atributo_dto)
        return atributos_dto

    def externo_a_dto(self, externo: dict) -> ImagenMedicaDTO:
        return ImagenMedicaDTO(
            diagnostico=self._procesar_diagnostico(externo.get('diagnostico', dict)),
            modalidad=externo.get('modalidad', str),
            fecha_creacion=externo.get('fecha_creacion', str),
            regiones_anatomicas=self._procesar_regiones_anatomicas(externo.get('regiones_anatomicas', list))
        )

    def dto_a_externo(self, dto: ImagenMedicaDTO) -> any:
        return dto.__dict__


class MapeadorImagenMedicaDTOEntity(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_demografia(self, demografia: Demografia) -> DemografiaDTO:
        return DemografiaDTO(
            id=str(demografia.id),
            edad=demografia.edad,
            grupo_edad=str(demografia.grupo_edad),
            sexo=str(demografia.sexo),
            etnicidad=str(demografia.etnicidad))

    def _procesar_diagnostico(self, diagnostico: Diagnostico) -> DiagnosticoDTO:
        return DiagnosticoDTO(
            id=str(diagnostico.id),
            nombre=diagnostico.nombre,
            descripcion=diagnostico.descripcion,
            demografia=self._procesar_demografia(diagnostico.demografia),
            atributos=self._procesar_atributos(diagnostico.atributos))

    def _procesar_regiones_anatomicas(self, regiones_anatomicas: list[RegionAnatomica]) -> list[RegionAnatomicaDTO]:
        regiones_anatomicas_dto: list[RegionAnatomicaDTO] = list()
        for region_anatomica in regiones_anatomicas:
            regiones_anatomicas_dto.append(
                RegionAnatomicaDTO(
                    id=str(region_anatomica.id),
                    categoria=str(region_anatomica.categoria),
                    especificacion=region_anatomica.especificacion
                )
            )
        return regiones_anatomicas_dto

    def _procesar_atributos(self, atributos: list[Atributo]) -> list[AtributoDTO]:
        atributos_dto: list[AtributoDTO] = list()
        for atributo in atributos:
            atributos_dto.append(
                AtributoDTO(
                    id=str(atributo.id),
                    nombre=atributo.nombre,
                    descripcion=atributo.descripcion
                )
            )
        return atributos_dto

    def _procesar_demografia_dto(self, demografia_dto: DemografiaDTO) -> Demografia:
        demografia = Demografia()
        demografia.edad = demografia_dto.edad
        demografia.grupo_edad = GrupoEdad(demografia_dto.grupo_edad)
        demografia.sexo = Sexo(demografia_dto.sexo)
        demografia.etnicidad = Etnia(demografia_dto.etnicidad)
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
            region_anatomica.categoria = CategoriaAnatomica(region_anatomica_dto.categoria)
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

    def entidad_a_dto(self, entidad: ImagenMedica) -> ImagenMedicaDTO:
        imagen_medica_dto = ImagenMedicaDTO(
            id=str(entidad.id),
            modalidad=str(entidad.modalidad),
            fecha_creacion=str(entidad.fecha_creacion),
            regiones_anatomicas=self._procesar_regiones_anatomicas(entidad.regiones_anatomicas),
            diagnostico=self._procesar_diagnostico(entidad.diagnostico)
        )
        return imagen_medica_dto

    def dto_a_entidad(self, dto: ImagenMedicaDTO) -> ImagenMedica:
        imagen_medica = ImagenMedica()
        imagen_medica.id = dto.id
        imagen_medica.diagnostico = self._procesar_diagnostico_dto(dto.diagnostico)
        imagen_medica.modalidad = Modalidad(dto.modalidad)
        imagen_medica.fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        imagen_medica.regiones_anatomicas = self._procesar_regiones_anatomicas_dto(dto.regiones_anatomicas)
        return imagen_medica



