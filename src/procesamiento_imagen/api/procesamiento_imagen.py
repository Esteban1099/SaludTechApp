import json

from flask import Response, request

from src.procesamiento_imagen.modulos.procesamiento_imagen.aplicacion.comandos.procesar_imagen_medica import ProcesarImagenMedica
from src.procesamiento_imagen.modulos.procesamiento_imagen.aplicacion.mapeadores import MapeadorImagenMedicaDTOJson
from src.procesamiento_imagen.modulos.procesamiento_imagen.infraestructura.despachadores import Despachador
from src.procesamiento_imagen.seedwork.dominio.excepciones import ExcepcionDominio
from src.procesamiento_imagen.seedwork.presentacion import api

blueprint = api.crear_blueprint('procesamiento_imagen', '/procesamiento_imagen')


@blueprint.route('/procesar_imagen_medica-comando', methods=['POST'])
def procesar_imagen_medica_asincrona():
    try:
        imagen_medica_dict = request.json

        imagen_medica_mapeador = MapeadorImagenMedicaDTOJson()
        imagen_medica_dto = imagen_medica_mapeador.externo_a_dto(imagen_medica_dict)

        comando = ProcesarImagenMedica(
            id=imagen_medica_dto.id,
            url=imagen_medica_dto.url,
            modalidad=imagen_medica_dto.modalidad,
            fecha_creacion=imagen_medica_dto.fecha_creacion,
            regiones_anatomicas=imagen_medica_dto.regiones_anatomicas,
            diagnostico=imagen_medica_dto.diagnostico
        )

        despachador = Despachador()
        despachador.publicar_comando(comando=comando, topico="comandos-imagen-medica-procesar")
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
