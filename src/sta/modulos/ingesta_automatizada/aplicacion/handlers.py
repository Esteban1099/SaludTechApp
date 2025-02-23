from src.sta.modulos.ingesta_automatizada.infraestructura.despachadores import Despachador
from src.sta.seedwork.aplicacion.handlers import Handler


class HandlerImagenMedicaIntegracion(Handler):
    @staticmethod
    def handle_imagen_medica_agregada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')