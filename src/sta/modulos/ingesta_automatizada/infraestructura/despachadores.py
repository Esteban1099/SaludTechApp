import datetime

import pulsar
from pulsar.schema import *

from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.comandos import ComandoAgregarImagenMedica
from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import ImagenMedicaAgregadaPayload, \
    EventoImagenMedicaAgregada
from src.sta.seedwork.infraestructura import utils

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        payload = ImagenMedicaAgregadaPayload(
            id=str(evento.id),
            modalidad=evento.modalidad,
            fecha_creacion=str(evento.fecha_creacion),
            estado=evento.estado
        )
        evento_integracion = EventoImagenMedicaAgregada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoImagenMedicaAgregada))

    def publicar_comando(self, comando, topico):
        mapeador = self._obtener_mapeador()
        self._publicar_mensaje(mapeador.comando_a_comando_integracion(comando), topico,
                               AvroSchema(ComandoAgregarImagenMedica))

    def _obtener_mapeador(self):
        from src.sta.modulos.ingesta_automatizada.dominio.mapeadores import MapeadorComandoAgregarImagenMedica
        return MapeadorComandoAgregarImagenMedica()
