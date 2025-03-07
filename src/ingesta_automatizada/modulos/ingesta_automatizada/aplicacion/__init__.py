from pydispatch import dispatcher

from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.handlers import HandlerImagenMedicaIntegracion
from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.eventos import ImagenMedicaAgregada, \
    ImagenMedicaEliminada

dispatcher.connect(HandlerImagenMedicaIntegracion.handle_imagen_medica_agregada,
                   signal=f'{ImagenMedicaAgregada.__name__}Integracion')
dispatcher.connect(HandlerImagenMedicaIntegracion.handle_imagen_medica_eliminada,
                   signal=f'{ImagenMedicaEliminada.__name__}Integracion')
