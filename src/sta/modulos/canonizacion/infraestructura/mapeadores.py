from src.sta.modulos.canonizacion.dominio.entidades import ImagenCanonizada, Demografia, Diagnostico, RegionAnatomica, Atributo
from src.sta.modulos.canonizacion.infraestructura.dto import ImagenCanonizadaDTO, DemografiaDTO, DiagnosticoDTO, RegionAnatomicaDTO, AtributoDTO
from src.sta.seedwork.dominio.repositorios import Mapeador
from uuid import UUID

class MapeadorImagenCanonizadaDTOEntity(Mapeador):
    def entidad_a_dto(self, entidad: ImagenCanonizada) -> ImagenCanonizadaDTO:
        imagen_dto = ImagenCanonizadaDTO()
        imagen_dto.id = str(entidad.id)
        imagen_dto.fecha_creacion = entidad.fecha_creacion
        imagen_dto.fecha_canonizacion = entidad.fecha_canonizacion
        imagen_dto.modalidad = entidad.modalidad
        imagen_dto.formato_canonizado = entidad.formato_canonizado

        # Mapear diagnóstico
        diagnostico_dto = DiagnosticoDTO()
        diagnostico_dto.id = str(entidad.diagnostico.id)
        diagnostico_dto.nombre = entidad.diagnostico.nombre
        diagnostico_dto.descripcion = entidad.diagnostico.descripcion

        # Mapear demografía
        demografia_dto = DemografiaDTO()
        demografia_dto.id = str(entidad.diagnostico.demografia.id)
        demografia_dto.edad = entidad.diagnostico.demografia.edad
        demografia_dto.grupo_edad = entidad.diagnostico.demografia.grupo_edad
        demografia_dto.sexo = entidad.diagnostico.demografia.sexo
        demografia_dto.etnicidad = entidad.diagnostico.demografia.etnicidad
        diagnostico_dto.demografia = demografia_dto

        # Mapear atributos
        for atributo in entidad.diagnostico.atributos:
            atributo_dto = AtributoDTO()
            atributo_dto.id = str(atributo.id)
            atributo_dto.nombre = atributo.nombre
            atributo_dto.descripcion = atributo.descripcion
            diagnostico_dto.atributos.append(atributo_dto)

        imagen_dto.diagnostico = diagnostico_dto

        # Mapear regiones anatómicas
        for region in entidad.regiones_anatomicas:
            region_dto = RegionAnatomicaDTO()
            region_dto.id = str(region.id)
            region_dto.categoria = region.categoria
            region_dto.especificacion = region.especificacion
            imagen_dto.regiones_anatomicas.append(region_dto)

        return imagen_dto

    def dto_a_entidad(self, dto: ImagenCanonizadaDTO) -> ImagenCanonizada:
        # Mapear demografía
        demografia = Demografia(
            id=UUID(dto.diagnostico.demografia.id),
            edad=dto.diagnostico.demografia.edad,
            grupo_edad=dto.diagnostico.demografia.grupo_edad,
            sexo=dto.diagnostico.demografia.sexo,
            etnicidad=dto.diagnostico.demografia.etnicidad
        )

        # Mapear atributos
        atributos = []
        for atributo_dto in dto.diagnostico.atributos:
            atributo = Atributo(
                id=UUID(atributo_dto.id),
                nombre=atributo_dto.nombre,
                descripcion=atributo_dto.descripcion
            )
            atributos.append(atributo)

        # Mapear diagnóstico
        diagnostico = Diagnostico(
            id=UUID(dto.diagnostico.id),
            nombre=dto.diagnostico.nombre,
            descripcion=dto.diagnostico.descripcion,
            demografia=demografia,
            atributos=atributos
        )

        # Mapear regiones anatómicas
        regiones = []
        for region_dto in dto.regiones_anatomicas:
            region = RegionAnatomica(
                id=UUID(region_dto.id),
                categoria=region_dto.categoria,
                especificacion=region_dto.especificacion
            )
            regiones.append(region)

        return ImagenCanonizada(
            id=UUID(dto.id),
            fecha_creacion=dto.fecha_creacion,
            fecha_canonizacion=dto.fecha_canonizacion,
            modalidad=dto.modalidad,
            formato_canonizado=dto.formato_canonizado,
            diagnostico=diagnostico,
            regiones_anatomicas=regiones
        ) 