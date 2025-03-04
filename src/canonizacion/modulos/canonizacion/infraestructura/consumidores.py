import logging
import traceback
import uuid
from datetime import datetime

import _pulsar
import pulsar
from pulsar.schema import *

from src.canonizacion.modulos.canonizacion.aplicacion.comandos.agregar_imagen_medica import AgregarImagenMedica
from src.canonizacion.modulos.canonizacion.aplicacion.dto import DemografiaDTO, AtributoDTO, DiagnosticoDTO, RegionAnatomicaDTO
from src.canonizacion.modulos.canonizacion.dominio.mapeadores import MapeadorComandoAgregarImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.comandos import ComandoAgregarImagenMedica
from src.canonizacion.modulos.canonizacion.infraestructura.schema.v1.eventos import EventoImagenMedicaAgregada, EventoImagenMedicaCanonizada
from src.canonizacion.seedwork.aplicacion.comandos import ejecutar_comando
from src.canonizacion.seedwork.infraestructura import utils
from src.canonizacion.modulos.canonizacion.infraestructura.despachadores import Despachador
from src.canonizacion.modulos.canonizacion.dominio.entidades import ImagenMedica
from src.canonizacion.modulos.canonizacion.dominio.objetos_valor import Modalidad, EstadoImagenMedica


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='canonizacion-sub-eventos-imagen-medica',
                                       schema=AvroSchema(EventoImagenMedicaAgregada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido en canonización: {mensaje.value().data}')
            
            # Procesar el evento recibido
            datos = mensaje.value().data
            
            # Extraer el valor real de la enumeración si viene con prefijo (ej: "Modalidad.RAYOS_X" -> "RAYOS_X")
            modalidad = datos.modalidad
            if '.' in modalidad:
                modalidad = modalidad.split('.')[-1]
            
            # Crear DTOs para el comando
            # Datos de ejemplo para pruebas
            demografia_dto = DemografiaDTO(
                edad=1,
                grupo_edad="NEONATAL",
                sexo="MASCULINO",
                etnicidad="LATINO"
            )
            
            atributos_dto = [
                AtributoDTO(
                    nombre="Tos",
                    descripcion="Seca, sin producción de flema"
                ),
                AtributoDTO(
                    nombre="Frecuencia",
                    descripcion="Persistente durante el día y la noche"
                ),
                AtributoDTO(
                    nombre="Duración",
                    descripcion="Más de 3 semanas (crónica)"
                ),
                AtributoDTO(
                    nombre="Sonido",
                    descripcion="Ronca y áspera"
                ),
                AtributoDTO(
                    nombre="Síntomas Asociados",
                    descripcion="Dolor de garganta, fiebre, fatiga"
                ),
                AtributoDTO(
                    nombre="Desencadenantes",
                    descripcion="Alérgenos, aire frío, ejercicio"
                )
            ]
            
            diagnostico_dto = DiagnosticoDTO(
                nombre="Tos seca persistente",
                descripcion="Diagnóstico generado automáticamente",
                demografia=demografia_dto,
                atributos=atributos_dto
            )
            
            regiones_anatomicas_dto = [
                RegionAnatomicaDTO(
                    categoria="CABEZA_CUELLO",
                    especificacion="Test"
                )
            ]
            
            # Crear el comando
            comando = AgregarImagenMedica(
                id=datos.id,
                modalidad=modalidad,
                fecha_creacion=datos.fecha_creacion,
                regiones_anatomicas=regiones_anatomicas_dto,
                diagnostico=diagnostico_dto
            )
            
            # Publicar el comando
            despachador = Despachador()
            despachador.publicar_comando(comando=comando, topico="comandos-imagen-medica")
            
            print(f'Comando publicado en el tópico comandos-imagen-medica: {comando}')
            
            consumidor.acknowledge(mensaje)

        cliente.close()
    except Exception as e:
        logging.error(f'ERROR: Suscribiendose al tópico de eventos! {str(e)}')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-imagen-medica', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='canonizacion-sub-comandos-imagen-medica',
                                       schema=AvroSchema(ComandoAgregarImagenMedica))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')
            
            try:
                # Mapear el comando de integración a un comando de dominio
                mapeador = MapeadorComandoAgregarImagenMedica()
                comando = mapeador.comando_integracion_a_comando(mensaje.value())
                
                # Ejecutar el comando
                ejecutar_comando(comando)
                
                print(f'Comando ejecutado exitosamente: {comando}')
                
                # Reconocer el mensaje
                consumidor.acknowledge(mensaje)
            except Exception as e:
                print(f'Error al procesar el comando: {str(e)}')
                traceback.print_exc()
                # En caso de error, podríamos implementar un mecanismo de reintento
                # o simplemente reconocer el mensaje para no procesarlo nuevamente
                consumidor.acknowledge(mensaje)

        cliente.close()
    except Exception as e:
        logging.error(f'ERROR: Suscribiendose al tópico de comandos! {str(e)}')
        traceback.print_exc()
        if cliente:
            cliente.close()
