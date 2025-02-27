from src.canonizacion.modulos.canonizacion.dominio.entidades import Demografia, Diagnostico, RegionAnatomica, Atributo, \
    ImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.dto import DemografiaDTO, DiagnosticoDTO, RegionAnatomicaDTO, \
    AtributoDTO, ImagenMedicaDTO
from src.canonizacion.seedwork.dominio.mapeadores import Mapeador


class MapeadorImagenMedicaDTOEntity(Mapeador):
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
