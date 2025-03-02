import json

from flask import Response, request

from src.sta.modulos.ingesta_automatizada.aplicacion.comandos.agregar_imagen_medica import AgregarImagenMedica
from src.sta.modulos.ingesta_automatizada.aplicacion.mapeadores import MapeadorImagenMedicaDTOJson
from src.sta.modulos.ingesta_automatizada.aplicacion.queries.obtener_imagen_medica import ObtenerImagenMedica
from src.sta.modulos.ingesta_automatizada.infraestructura.despachadores import Despachador
from src.sta.seedwork.aplicacion.queries import ejecutar_query
from src.sta.seedwork.dominio.excepciones import ExcepcionDominio
from src.sta.seedwork.presentacion import api

blueprint = api.crear_blueprint('ingesta_automatizada', '/ingesta_automatizada')


@blueprint.route('/imagen_medica-comando', methods=['POST'])
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


@blueprint.route('/imagen_medica-query/<id>', methods=['GET'])
def dar_imagen_medica(id=None):
    query = ejecutar_query(ObtenerImagenMedica(id))
    mapeador_imagen_medica = MapeadorImagenMedicaDTOJson()
    return mapeador_imagen_medica.dto_a_externo(query.resultado)
