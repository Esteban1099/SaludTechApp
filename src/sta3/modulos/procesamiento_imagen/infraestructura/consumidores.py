import logging
import sys
import traceback
import uuid
from datetime import datetime

import _pulsar
import pulsar
from pulsar.schema import *

from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.eventos import EventoImagenMedicaCanonizada
from src.sta3.modulos.procesamiento_imagen.aplicacion.comandos.procesar_imagen_medica import ProcesarImagenMedica
from src.sta3.modulos.procesamiento_imagen.dominio.mapeadores import MapeadorComandoProcesarImagenMedica
from src.sta3.modulos.procesamiento_imagen.infraestructura.despachadores import Despachador
from src.sta3.modulos.procesamiento_imagen.infraestructura.schema.v1.comandos import ComandoProcesarImagenMedica
from src.sta3.modulos.procesamiento_imagen.infraestructura.schema.v1.eventos import EventoImagenMedicaProcesada
from src.sta3.seedwork.aplicacion.comandos import ejecutar_comando
from src.sta3.seedwork.infraestructura import utils
from src.sta3.modulos.procesamiento_imagen.aplicacion.dto import DemografiaDTO, AtributoDTO, DiagnosticoDTO, RegionAnatomicaDTO
from src.sta3.modulos.procesamiento_imagen.aplicacion.comandos.procesar_imagen_medica import ProcesarImagenMedica



def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-imagen-canonizada', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='sta-sub-eventos-imagen-canonizada', schema=AvroSchema(EventoImagenMedicaCanonizada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}', sys.stdout)

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
                    id=evento_data.id,  # Replace with actual id if available
                    url=f"http://example.com/{uuid.uuid4()}",  # Replace with actual url if available
                    modalidad=json_data["modalidad"],
                    fecha_creacion=fecha_creacion,
                    regiones_anatomicas=regiones_anatomicas_dto,
                    diagnostico=diagnostico_dto
                )

            despachador = Despachador()
            despachador.publicar_comando(comando=comando, topico="comandos-imagen-medica-procesar")
            consumidor.acknowledge(mensaje)
            print(f'Evento procesado y se ejecutó el comando: {comando}', sys.stdout)

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
                                       subscription_name='sta-sub-comandos-imagen-medica-procesar',
                                       schema=AvroSchema(ComandoProcesarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}', sys.stdout)
            mapeador = MapeadorComandoProcesarImagenMedica()
            comando = mapeador.comando_integracion_a_comando(mensaje.value())
            ejecutar_comando(comando)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
