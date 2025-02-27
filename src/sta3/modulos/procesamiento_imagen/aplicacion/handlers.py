from src.sta3.modulos.procesamiento_imagen.infraestructura.despachadores import Despachador
from src.sta3.seedwork.aplicacion.handlers import Handler


class HandlerImagenMedicaIntegracion(Handler):
    @staticmethod
    def handle_imagen_medica_procesada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-imagen-medica-procesada')