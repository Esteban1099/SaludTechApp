from src.canonizacion.modulos.canonizacion.infraestructura.despachadores import Despachador
from src.canonizacion.seedwork.aplicacion.handlers import Handler


class HandlerImagenMedicaIntegracion(Handler):
    @staticmethod
    def handle_imagen_medica_agregada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-imagen-medica')
        
    @staticmethod
    def handle_imagen_medica_canonizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-imagen-canonizada')