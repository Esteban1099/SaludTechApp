import logging
import sys
import traceback
from datetime import datetime

import _pulsar
import pulsar
from pulsar.schema import *

from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.schema.v1.eventos import \
    EventoImagenMedicaAgregada
from src.procesamiento_imagen.modulos.procesamiento_imagen.aplicacion.comandos.eliminar_imagen_medica import \
    EliminarImagenMedica
from src.procesamiento_imagen.modulos.procesamiento_imagen.aplicacion.comandos.procesar_imagen_medica import ProcesarImagenMedica
from src.procesamiento_imagen.modulos.procesamiento_imagen.aplicacion.dto import DemografiaDTO, AtributoDTO, DiagnosticoDTO, \
    RegionAnatomicaDTO
from src.procesamiento_imagen.modulos.procesamiento_imagen.dominio.mapeadores import \
    MapeadorComandoProcesarImagenMedica, MapeadorComandoEliminarImagenMedica
from src.procesamiento_imagen.modulos.procesamiento_imagen.infraestructura.despachadores import Despachador
from src.procesamiento_imagen.modulos.procesamiento_imagen.infraestructura.schema.v1.comandos import \
    ComandoProcesarImagenMedica, ComandoEliminarImagenMedica
from src.procesamiento_imagen.modulos.procesamiento_imagen.infraestructura.schema.v1.eventos import \
    EventoImagenMedicaEliminada
from src.procesamiento_imagen.seedwork.aplicacion.comandos import ejecutar_comando
from src.procesamiento_imagen.seedwork.dominio.excepciones import ExcepcionDominio
from src.procesamiento_imagen.seedwork.infraestructura import utils


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='procesamiento-imagen-sub-eventos-imagen-medica-agregada',
                                       schema=AvroSchema(EventoImagenMedicaAgregada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}', file=sys.stdout)

            json_data = {
                "diagnostico": {
                    "nombre": "Tos",
                    "descripcion": "De perra",
                    "demografia": {
                        "edad": 10,
                        "grupo_edad": "Neonatal",
                        "sexo": "Masculino",
                        "etnicidad": "Latino"
                    },
                    "atributos": [
                        {
                            "nombre": "Tos",
                            "descripcion": "De perra"
                        }
                    ]
                },
                "modalidad": "Rayos X",
                "fecha_creacion": "2022-11-22T13:10:00Z",
                "regiones_anatomicas": [
                    {
                        "categoria": "Cabeza y cuello",
                        "especificacion": "Test"
                    }
                ]
            }

            demografia_dto = DemografiaDTO(
                edad=json_data["diagnostico"]["demografia"]["edad"],
                grupo_edad=json_data["diagnostico"]["demografia"]["grupo_edad"],
                sexo=json_data["diagnostico"]["demografia"]["sexo"],
                etnicidad=json_data["diagnostico"]["demografia"]["etnicidad"]
            )

            atributos_dto = [AtributoDTO(
                nombre=atributo["nombre"],
                descripcion=atributo["descripcion"]
            ) for atributo in json_data["diagnostico"]["atributos"]]

            diagnostico_dto = DiagnosticoDTO(
                nombre=json_data["diagnostico"]["nombre"],
                descripcion=json_data["diagnostico"]["descripcion"],
                demografia=demografia_dto,
                atributos=atributos_dto
            )

            regiones_anatomicas_dto = [RegionAnatomicaDTO(
                categoria=region["categoria"],
                especificacion=region["especificacion"]
            ) for region in json_data["regiones_anatomicas"]]

            FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
            FECHA_POR_DEFECTO = '2022-01-01T00:00:00Z'

            fecha_creacion = datetime.strptime(FECHA_POR_DEFECTO, FORMATO_FECHA).strftime(FORMATO_FECHA)
            evento_data = mensaje.value().data

            comando = ProcesarImagenMedica(
                id=evento_data.id,
                url=evento_data.url,
                flag=int(evento_data.flag),
                modalidad=json_data["modalidad"],
                fecha_creacion=fecha_creacion,
                regiones_anatomicas=regiones_anatomicas_dto,
                diagnostico=diagnostico_dto
            )

            despachador = Despachador()
            despachador.publicar_comando(comando=comando, topico="comandos-imagen-medica-procesar")
            consumidor.acknowledge(mensaje)
            print(f'Evento procesado y se ejecutó el comando: {comando}', file=sys.stdout)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_eventos_compensacion():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-compensacion-imagen-medica-procesada', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='ingesta_automatizada-sub-eventos-compensacion-imagen-medica-procesada',
                                       schema=AvroSchema(EventoImagenMedicaEliminada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}', file=sys.stdout)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-imagen-medica-procesar', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='procesamiento-imagen-sub-comandos-imagen-medica-procesar',
                                       schema=AvroSchema(ComandoProcesarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}', file=sys.stdout)
            mapeador = MapeadorComandoProcesarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(mensaje.value())
            try:
                if comando.flag == 1:
                    print(f'El flag de error para saga esta activo', file=sys.stdout)
                    despachador = Despachador()
                    despachador.publicar_comando_rollback(comando.id)
                    print(f'Se envio el comando para hacer rollback a ingesta automatizada', file=sys.stdout)
                else:
                    ejecutar_comando(comando)
                    print(f'Se ejecutó el comando de procesar imagen: {comando}', file=sys.stdout)
            except ExcepcionDominio as e:
                print(e, file=sys.stdout)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos_compensacion():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-compensacion-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='procesamiento-imagen-sub-comandos-compensancion-imagen-medica',
                                       schema=AvroSchema(ComandoEliminarImagenMedica))

        while True:
            print(f'Esperando comando de compensación...', file=sys.stdout)
            mensaje = consumidor.receive()
            print(f'Comando de compensaciónn recibido: {mensaje.value().data}', file=sys.stdout)
            mapeador = MapeadorComandoEliminarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(mensaje.value())
            try:
                ejecutar_comando(comando)
                print(f'Se ejecutó el comando de compensación exitosamente: {comando}', file=sys.stdout)
            except ExcepcionDominio as e:
                print(e, file=sys.stdout)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()