from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.despachadores import Despachador
from src.ingesta_automatizada.seedwork.aplicacion.handlers import Handler


class HandlerImagenMedicaIntegracion(Handler):
    @staticmethod
    def handle_imagen_medica_agregada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-imagen-medica')

    @staticmethod
    def handle_imagen_medica_eliminada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-compensacion-imagen-medica')
