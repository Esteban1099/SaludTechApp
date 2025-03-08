from pydispatch import dispatcher

from src.procesamiento_imagen.modulos.procesamiento_imagen.aplicacion.handlers import HandlerImagenMedicaIntegracion
from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.eventos import ImagenMedicaProcesada, \
    ImagenMedicaEliminada

dispatcher.connect(HandlerImagenMedicaIntegracion.handle_imagen_medica_procesada, signal=f'{ImagenMedicaProcesada.__name__}Integracion')

dispatcher.connect(HandlerImagenMedicaIntegracion.handle_imagen_medica_eliminada, signal=f'{ImagenMedicaEliminada.__name__}Integracion')