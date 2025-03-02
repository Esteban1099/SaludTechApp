from enum import Enum


class Modalidad(Enum):
    RAYOS_X = "Rayos X"
    TOMOGRAFIA = "Tomografía"
    RESONANCIA_MAGNETICA = "Resonancia magnética"
    ULTRA_SONIDO = "Ultra sonido"
    MAMOGRAFIA = "Mamografía"
    ESCANEO_TEP = "Escaneo TEP"
    HISTOPATOLOGIA = "Histopatología"


class CategoriaAnatomica(Enum):
    CABEZA_CUELLO = "Cabeza y cuello"
    TORAX = "Tórax"
    ABDOMEN = "Abdomen"
    MUSCULOESQUELETICO = "Musculoesquelético"
    PELVIS = "Pélvis"
    CUERPO_COMPLETO = "Cuerpo completo"


class GrupoEdad(Enum):
    NEONATAL = "Neonatal"
    PEDIATRICO = "Pediatrico"
    ADULTO = "Adulto"
    GERIATRICO = "Geriatrico"


class Sexo(Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"
    INTERSEXUAL = "Intersexual"


class Etnia(Enum):
    LATINO = "Latino"
    CAUCASICO = "Caucásico"
    AFRO = "Afro"
    ASIATICO = "Asiatico"


class EstadoImagenMedica(str, Enum):
    EN_INGESTA = "En ingesta"
    CREADA = "Creada"
    CANONIZADA = "Canonizada"
    PROCESADA = "Procesada"
