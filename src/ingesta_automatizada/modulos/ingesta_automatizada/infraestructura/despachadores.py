import datetime

import pulsar
from pulsar.schema import *

from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.comandos.agregar_imagen_medica import \
    AgregarImagenMedica
from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.eventos import ImagenMedicaEliminada
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import \
    ImagenMedicaAgregadaPayload, \
    EventoImagenMedicaAgregada, ImagenMedicaEliminadaPayload, EventoImagenMedicaEliminada, DiagnosticoRecord, \
    DemografiaRecord, AtributoRecord, RegionAnatomicaRecord
from src.ingesta_automatizada.seedwork.infraestructura import utils

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
        if isinstance(evento, ImagenMedicaEliminada):
            payload = ImagenMedicaEliminadaPayload(
                id=str(evento.id),
                estado=evento.estado
            )
            evento_integracion = EventoImagenMedicaEliminada(data=payload)
            self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoImagenMedicaEliminada))
        else:
            payload = ImagenMedicaAgregadaPayload(
                id=str(evento.id),
                modalidad=evento.modalidad,
                url=evento.url,
                flag=evento.flag,
                fecha_creacion=str(evento.fecha_creacion),
                regiones_anatomicas=[
                    RegionAnatomicaRecord(
                        id=str(region_anatomica.id),
                        categoria=region_anatomica.categoria,
                        especificacion=region_anatomica.especificacion
                    ) for region_anatomica in evento.regiones_anatomicas
                ],
                diagnostico=DiagnosticoRecord(
                    id=str(evento.diagnostico.id),
                    nombre=evento.diagnostico.nombre,
                    descripcion=evento.diagnostico.descripcion,
                    demografia=DemografiaRecord(
                        id=str(evento.diagnostico.demografia.id),
                        edad=evento.diagnostico.demografia.edad,
                        grupo_edad=evento.diagnostico.demografia.grupo_edad,
                        sexo=evento.diagnostico.demografia.sexo,
                        etnicidad=evento.diagnostico.demografia.etnicidad
                    ),
                    atributos=[
                        AtributoRecord(
                            id=str(atributo.id),
                            nombre=atributo.nombre,
                            descripcion=atributo.descripcion,
                        ) for atributo in evento.diagnostico.atributos
                    ]
                ),
                estado=evento.estado

            )
            evento_integracion = EventoImagenMedicaAgregada(data=payload)
            self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoImagenMedicaAgregada))

    def publicar_comando(self, comando, topico, esquema):
        mapeador = self._obtener_mapeador(comando)
        self._publicar_mensaje(mapeador.comando_a_comando_integracion(comando), topico, AvroSchema(esquema))

    def _obtener_mapeador(self, comando):
        if isinstance(comando, AgregarImagenMedica):
            from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.mapeadores import \
                MapeadorComandoAgregarImagenMedica
            return MapeadorComandoAgregarImagenMedica()
        else:
            from src.ingesta_automatizada.modulos.ingesta_automatizada.dominio.mapeadores import \
                MapeadorComandoEliminarImagenMedica
            return MapeadorComandoEliminarImagenMedica()
