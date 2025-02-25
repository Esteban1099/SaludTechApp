from src.canonizacion.modulos.canonizacion.dominio.repositorios import RepositorioImagenesCanonizadas
from src.canonizacion.modulos.canonizacion.infraestructura.despachadores import Despachador
from src.sta.seedwork.aplicacion.handlers import Handler
from uuid import UUID
import datetime

class HandlerImagenMedicaIntegracion(Handler):
    def __init__(self, repositorio: RepositorioImagenesCanonizadas):
        self.repositorio = repositorio
        self.despachador = Despachador()

    def handle_imagen_medica_agregada(self, evento):
        # Convertimos el evento recibido en una imagen canonizada
        # En un caso real, aquí iría la lógica de canonización
        imagen_canonizada = {
            'id': str(UUID(evento.data.id)),
            'id_imagen_original': evento.data.id,
            'formato_canonizado': 'DICOM_CANONICO_V1',
            'fecha_canonizacion': datetime.datetime.now().isoformat(),
            'metadatos': 'Metadata estandarizada según protocolo XYZ',
            'modalidad': evento.data.modalidad,
            'fecha_creacion': evento.data.fecha_creacion,
            'diagnostico': evento.data.diagnostico,
            'regiones_anatomicas': evento.data.regiones_anatomicas
        }

        # Guardamos la imagen canonizada
        self.repositorio.agregar(imagen_canonizada)
        
        # Publicamos el evento de canonización completada
        self.despachador.publicar_evento_canonizacion(imagen_canonizada) 