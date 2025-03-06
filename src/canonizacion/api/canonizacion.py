import json

from flask import Response, request

from src.canonizacion.modulos.canonizacion.aplicacion.comandos.agregar_imagen_medica import CanonizarImagenMedica
from src.canonizacion.modulos.canonizacion.aplicacion.mapeadores import MapeadorImagenMedicaDTOJson
from src.canonizacion.modulos.canonizacion.infraestructura.despachadores import Despachador
from src.canonizacion.seedwork.dominio.excepciones import ExcepcionDominio
from src.canonizacion.seedwork.presentacion import api
from src.canonizacion.modulos.canonizacion.aplicacion.comandos.canonizar_imagen_medica import CanonizarImagenMedica
from src.canonizacion.modulos.canonizacion.aplicacion.comandos.canonizar_imagen_medica import CanonizarImagenMedicaHandler
from src.canonizacion.seedwork.aplicacion.comandos import ejecutar_comando

blueprint = api.crear_blueprint('canonizacion', '/canonizacion')


@blueprint.route('/agregar_imagen_medica-comando', methods=['POST'])
def agregar_imagen_medica_asincrona():
    try:
        imagen_medica_dict = request.json

        imagen_medica_mapeador = MapeadorImagenMedicaDTOJson()
        imagen_medica_dto = imagen_medica_mapeador.externo_a_dto(imagen_medica_dict)

        comando = AgregarImagenMedica(
            id=imagen_medica_dto.id,
            modalidad=imagen_medica_dto.modalidad,
            fecha_creacion=imagen_medica_dto.fecha_creacion,
            regiones_anatomicas=imagen_medica_dto.regiones_anatomicas,
            diagnostico=imagen_medica_dto.diagnostico
        )

        despachador = Despachador()
        despachador.publicar_comando(comando=comando, topico="comandos-imagen-medica")
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

def iniciar_aplicacion():
    # Registrar comandos
    ejecutar_comando.register(CanonizarImagenMedica, CanonizarImagenMedicaHandler())
