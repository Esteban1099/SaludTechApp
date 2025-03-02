import datetime
import pulsar
from pulsar.schema import *

from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.comandos import ComandoAgregarImagenMedica
from src.sta.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import ImagenMedicaAgregadaPayload, EventoImagenMedicaAgregada
from src.sta.seedwork.infraestructura import utils

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def __init__(self):
        """Inicializa el cliente Pulsar y el diccionario de productores."""
        self.cliente = pulsar.Client(
            f'pulsar://{utils.broker_host()}:6650',
            operation_timeout_seconds=30,  # Evita timeouts rápidos
        )
        self.productores = {}  # Almacenar productores por topic

    def _obtener_productor(self, topico, schema):
        """Si el productor no existe, lo crea y lo almacena."""
        if topico not in self.productores:
            self.productores[topico] = self.cliente.create_producer(topico, schema=schema)
        return self.productores[topico]

    def _publicar_mensaje(self, mensaje, topico, schema):
        """Envía un mensaje usando un productor reutilizable."""
        try:
            publicador = self._obtener_productor(topico, schema)
            publicador.send(mensaje)
        except Exception as e:
            print(f"⚠️ Error al publicar mensaje en {topico}: {e}")

    def publicar_evento(self, evento, topico):
        """Publica un evento en el topic de Pulsar."""
        payload = ImagenMedicaAgregadaPayload(
            id=str(evento.id),
            modalidad=evento.modalidad,
            fecha_creacion=str(evento.fecha_creacion),
            estado=evento.estado
        )
        evento_integracion = EventoImagenMedicaAgregada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoImagenMedicaAgregada))

    def publicar_comando(self, comando, topico):
        """Publica un comando en el topic de Pulsar."""
        mapeador = self._obtener_mapeador()
        self._publicar_mensaje(mapeador.comando_a_comando_integracion(comando), topico, AvroSchema(ComandoAgregarImagenMedica))

    def _obtener_mapeador(self):
        """Carga el mapeador solo cuando se necesita."""
        from src.sta.modulos.ingesta_automatizada.dominio.mapeadores import MapeadorComandoAgregarImagenMedica
        return MapeadorComandoAgregarImagenMedica()

    def close(self):
        """Cierra los productores y el cliente Pulsar correctamente."""
        for productor in self.productores.values():
            productor.close()
        self.cliente.close()
