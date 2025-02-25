from pydispatch import dispatcher

from src.sta.modulos.ingesta_automatizada.aplicacion.handlers import HandlerImagenMedicaIntegracion
from src.sta.modulos.ingesta_automatizada.dominio.eventos import ImagenMedicaAgregada

dispatcher.connect(HandlerImagenMedicaIntegracion.handle_imagen_medica_agregada, signal=f'{ImagenMedicaAgregada.__name__}Integracion')