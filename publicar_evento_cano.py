import pulsar
from pulsar.schema import *
import uuid
import sys
import json
from datetime import datetime
import argparse

# Parsear argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Publicar eventos para probar Canonización')
parser.add_argument('--tipo', type=str, choices=['canonizar', 'rollback'], required=True,
                    help='Tipo de evento a publicar: "canonizar" para imagen agregada, "rollback" para compensación')
parser.add_argument('--flag', type=int, default=1,
                    help='Solo para tipo "canonizar": Flag para aceptar (1) o rechazar (0) la transacción')
parser.add_argument('--id', type=str, default=str(uuid.uuid4()),
                    help='ID de la imagen médica')
parser.add_argument('--host', type=str, default="pulsar",
                    help='Host de Pulsar (usa "localhost" si ejecutas fuera de Docker)')
parser.add_argument('--port', type=int, default=6650,
                    help='Puerto de Pulsar')
args = parser.parse_args()


# Definir los esquemas necesarios
class RegionAnatomicaRecord(Record):
    id = String()
    categoria = String()
    especificacion = String()


class ImagenMedicaAgregadaPayload(Record):
    id = String()
    modalidad = String()
    fecha_creacion = String()
    estado = String()
    flag = Integer()
    url = String(default="http://example.com/imagen.jpg")
    regiones_anatomicas = Array(RegionAnatomicaRecord())


class EventoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long(default=int(datetime.now().timestamp() * 1000))
    ingestion = Long(default=int(datetime.now().timestamp() * 1000))
    specversion = String(default="v1")
    type = String()
    datacontenttype = String(default="application/json")
    service_name = String(default="prueba")


class EventoImagenMedicaAgregada(EventoIntegracion):
    type = String(default="ImagenMedicaAgregada")
    data = ImagenMedicaAgregadaPayload()


# Esquema para eventos de compensación
class CompensacionImagenMedicaPayload(Record):
    id = String()
    motivo = String()
    fecha_compensacion = String()


class EventoCompensacionImagenMedica(EventoIntegracion):
    type = String(default="CompensacionImagenMedica")
    data = CompensacionImagenMedicaPayload()


# Publicar evento de imagen médica agregada
def publicar_evento_canonizar():
    pulsar_url = f"pulsar://{args.host}:{args.port}"
    print(f"Conectando a Pulsar en {pulsar_url}...")
    client = pulsar.Client(pulsar_url)

    producer = client.create_producer(
        "eventos-imagen-medica",
        schema=AvroSchema(EventoImagenMedicaAgregada)
    )

    payload = ImagenMedicaAgregadaPayload(
        id=args.id,
        modalidad="RAYOS_X",  # usa un valor exacto esperado por tu dominio
        fecha_creacion="2022-11-22T13:10:00Z",
        estado="CREADA",
        flag=args.flag,
        url="http://example.com/imagen.jpg",
        regiones_anatomicas=[
            RegionAnatomicaRecord(
                id=str(uuid.uuid4()),
                categoria="CABEZA_CUELLO",
                especificacion="Test"
            )
        ]
    )

    evento = EventoImagenMedicaAgregada(data=payload)

    producer.send(evento)
    print(f"Evento enviado con ID: {args.id}, Flag: {args.flag}")

    producer.close()
    client.close()


# Publicar evento de compensación (rollback)
def publicar_evento_rollback():
    pulsar_url = f"pulsar://{args.host}:{args.port}"
    print(f"Conectando a Pulsar en {pulsar_url}...")
    client = pulsar.Client(pulsar_url)

    producer = client.create_producer(
        "eventos-compensacion-imagen-medica",
        schema=AvroSchema(EventoCompensacionImagenMedica)
    )

    payload = CompensacionImagenMedicaPayload(
        id=args.id,
        motivo="Prueba de compensación manual",
        fecha_compensacion=datetime.now().isoformat()
    )

    evento = EventoCompensacionImagenMedica(data=payload)

    producer.send(evento)
    print(f"Evento de compensación enviado con ID: {args.id}")

    producer.close()
    client.close()


# Función principal
def main():
    try:
        if args.tipo == 'canonizar':
            publicar_evento_canonizar()
        elif args.tipo == 'rollback':
            publicar_evento_rollback()

        print("Evento publicado exitosamente.")

    except Exception as e:
        print(f"Error al publicar evento: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
