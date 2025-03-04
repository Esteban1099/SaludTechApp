from datetime import datetime
from dataclasses import field, dataclass

from src.canonizacion.modulos.canonizacion.aplicacion.dto import ImagenMedicaDTO, DemografiaDTO, RegionAnatomicaDTO, \
    DiagnosticoDTO, AtributoDTO
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica, Demografia, RegionAnatomica, \
    Diagnostico, Atributo
from src.canonizacion.modulos.canonizacion.dominio.objetos_valor import Modalidad, GrupoEdad, Sexo, Etnia, \
    CategoriaAnatomica
from src.canonizacion.seedwork.aplicacion.mapeadores import Mapeador as AplMap
from src.canonizacion.seedwork.dominio.mapeadores import Mapeador as RepMap


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
            grupo_edad=demografia.grupo_edad.value,
            sexo=demografia.sexo.value,
            etnicidad=demografia.etnicidad.value)

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
                    categoria=region_anatomica.categoria.value,
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
        print(f"DEBUG: Procesando demografia_dto: {demografia_dto.__dict__}")
        demografia = Demografia()
        demografia.edad = demografia_dto.edad
        
        # Extraer el valor real de la enumeración si viene con prefijo (ej: "GrupoEdad.NEONATAL" -> "NEONATAL")
        grupo_edad = demografia_dto.grupo_edad
        print(f"DEBUG: Grupo edad original: {grupo_edad}")
        if '.' in grupo_edad:
            grupo_edad = grupo_edad.split('.')[-1]
            print(f"DEBUG: Grupo edad después de split: {grupo_edad}")
        
        # Manejar casos específicos
        if grupo_edad == 'NEONATAL':
            grupo_edad = 'Neonatal'
        elif grupo_edad == 'PEDIATRICO':
            grupo_edad = 'Pediatrico'
        elif grupo_edad == 'INFANTIL':
            grupo_edad = 'Infantil'
        elif grupo_edad == 'ADULTO':
            grupo_edad = 'Adulto'
        elif grupo_edad == 'GERIATRICO':
            grupo_edad = 'Geriatrico'
        else:
            # Convertir a formato correcto (primera letra mayúscula, resto minúsculas)
            grupo_edad = grupo_edad.capitalize()
        
        print(f"DEBUG: Grupo edad final: {grupo_edad}")
        demografia.grupo_edad = GrupoEdad(grupo_edad)
        
        # Extraer el valor real de la enumeración si viene con prefijo (ej: "Sexo.MASCULINO" -> "MASCULINO")
        sexo = demografia_dto.sexo
        print(f"DEBUG: Sexo original: {sexo}")
        if '.' in sexo:
            sexo = sexo.split('.')[-1]
            print(f"DEBUG: Sexo después de split: {sexo}")
        
        # Manejar casos específicos
        if sexo == 'MASCULINO':
            sexo = 'Masculino'
        elif sexo == 'FEMENINO':
            sexo = 'Femenino'
        else:
            # Convertir a formato correcto (primera letra mayúscula, resto minúsculas)
            sexo = sexo.capitalize()
        
        print(f"DEBUG: Sexo final: {sexo}")
        demografia.sexo = Sexo(sexo)
        
        # Extraer el valor real de la enumeración si viene con prefijo (ej: "Etnicidad.CAUCASICO" -> "CAUCASICO")
        etnicidad = demografia_dto.etnicidad
        print(f"DEBUG: Etnicidad original: {etnicidad}")
        if '.' in etnicidad:
            etnicidad = etnicidad.split('.')[-1]
            print(f"DEBUG: Etnicidad después de split: {etnicidad}")
        
        # Manejar casos específicos para etnicidad
        if etnicidad == 'CAUCASICO':
            etnicidad = 'Caucasico'
        elif etnicidad == 'AFROAMERICANO':
            etnicidad = 'Afroamericano'
        elif etnicidad == 'LATINO':
            etnicidad = 'Latino'
        elif etnicidad == 'ASIATICO':
            etnicidad = 'Asiatico'
        elif etnicidad == 'OTRO':
            etnicidad = 'Otro'
        else:
            # Convertir a formato correcto (primera letra mayúscula, resto minúsculas)
            etnicidad = etnicidad.capitalize()
        
        print(f"DEBUG: Etnicidad final: {etnicidad}")
        demografia.etnicidad = Etnia(etnicidad)
        
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
            
            # Extraer el valor real de la enumeración si viene con prefijo (ej: "CategoriaAnatomica.CABEZA_CUELLO" -> "CABEZA_CUELLO")
            categoria_str = region_anatomica_dto.categoria
            if '.' in categoria_str:
                categoria_str = categoria_str.split('.')[-1]
            
            # Manejar casos específicos para categoría anatómica
            if categoria_str == 'CABEZA_CUELLO':
                region_anatomica.categoria = CategoriaAnatomica.CABEZA_CUELLO
            elif categoria_str == 'TORAX':
                region_anatomica.categoria = CategoriaAnatomica.TORAX
            elif categoria_str == 'ABDOMEN':
                region_anatomica.categoria = CategoriaAnatomica.ABDOMEN
            elif categoria_str == 'MUSCULOESQUELETICO':
                region_anatomica.categoria = CategoriaAnatomica.MUSCULOESQUELETICO
            elif categoria_str == 'PELVIS':
                region_anatomica.categoria = CategoriaAnatomica.PELVIS
            elif categoria_str == 'CUERPO_COMPLETO':
                region_anatomica.categoria = CategoriaAnatomica.CUERPO_COMPLETO
            else:
                # Si no coincide con ninguno, usar un valor por defecto
                print(f"ADVERTENCIA: Categoría anatómica desconocida: {categoria_str}. Usando CABEZA_CUELLO como valor por defecto.")
                region_anatomica.categoria = CategoriaAnatomica.CABEZA_CUELLO
            
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
            modalidad=entidad.modalidad.value,
            fecha_creacion=str(entidad.fecha_creacion),
            regiones_anatomicas=self._procesar_regiones_anatomicas(entidad.regiones_anatomicas),
            diagnostico=self._procesar_diagnostico(entidad.diagnostico)
        )
        return imagen_medica_dto

    def dto_a_entidad(self, dto: ImagenMedicaDTO) -> ImagenMedica:
        imagen_medica = ImagenMedica()
        imagen_medica.id = dto.id
        
        # Estos campos no existen en el DTO, así que los dejamos con valores por defecto
        # o los obtenemos de otra manera si es necesario
        imagen_medica.id_paciente = ""  # Valor por defecto
        imagen_medica.id_estudio = ""   # Valor por defecto
        
        # Convertir el string de modalidad a un objeto Modalidad
        modalidad_str = dto.modalidad
        # Extraer el valor real de la enumeración si viene con prefijo (ej: "Modalidad.RAYOS_X" -> "RAYOS_X")
        if '.' in modalidad_str:
            modalidad_str = modalidad_str.split('.')[-1]
        
        # Manejar casos específicos para modalidad
        if modalidad_str == 'RAYOS_X':
            imagen_medica.modalidad = Modalidad.RAYOS_X
        elif modalidad_str == 'TOMOGRAFIA':
            imagen_medica.modalidad = Modalidad.TOMOGRAFIA
        elif modalidad_str == 'RESONANCIA_MAGNETICA':
            imagen_medica.modalidad = Modalidad.RESONANCIA_MAGNETICA
        elif modalidad_str == 'ULTRA_SONIDO':
            imagen_medica.modalidad = Modalidad.ULTRA_SONIDO
        elif modalidad_str == 'MAMOGRAFIA':
            imagen_medica.modalidad = Modalidad.MAMOGRAFIA
        elif modalidad_str == 'ESCANEO_TEP':
            imagen_medica.modalidad = Modalidad.ESCANEO_TEP
        elif modalidad_str == 'HISTOPATOLOGIA':
            imagen_medica.modalidad = Modalidad.HISTOPATOLOGIA
        else:
            # Si no coincide con ninguno, usar un valor por defecto
            print(f"ADVERTENCIA: Modalidad desconocida: {modalidad_str}. Usando RAYOS_X como valor por defecto.")
            imagen_medica.modalidad = Modalidad.RAYOS_X
        
        imagen_medica.numero_instancia = 0  # Valor por defecto
        imagen_medica.ruta_archivo = ""  # Valor por defecto
        
        imagen_medica.diagnostico = self._procesar_diagnostico_dto(dto.diagnostico)
        imagen_medica.regiones_anatomicas = self._procesar_regiones_anatomicas_dto(dto.regiones_anatomicas)
        
        # El DTO no tiene atributos, así que dejamos una lista vacía
        imagen_medica.atributos = []
        
        # Manejar diferentes formatos de fecha
        try:
            # Intentar con el formato estándar
            imagen_medica.fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        except ValueError:
            try:
                # Intentar con formato alternativo (YYYY-MM-DD HH:MM:SS)
                imagen_medica.fecha_creacion = datetime.strptime(dto.fecha_creacion, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # Si falla, usar la fecha actual
                print(f"ERROR: No se pudo parsear la fecha: {dto.fecha_creacion}. Usando fecha actual.")
                imagen_medica.fecha_creacion = datetime.now()
        
        return imagen_medica



