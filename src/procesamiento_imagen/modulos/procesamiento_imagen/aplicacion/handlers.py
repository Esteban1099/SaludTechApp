from src.procesamiento_imagen.modulos.procesamiento_imagen.infraestructura.despachadores import Despachador
from src.procesamiento_imagen.seedwork.aplicacion.handlers import Handler


class HandlerImagenMedicaIntegracion(Handler):
    @staticmethod
    def handle_imagen_medica_procesada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-imagen-medica-procesada')

    @staticmethod
    def handle_imagen_medica_eliminada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-compensacion-imagen-medica-procesada')