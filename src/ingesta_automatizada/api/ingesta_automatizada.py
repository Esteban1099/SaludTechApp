import json

from flask import Response, request

from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.comandos.agregar_imagen_medica import \
    AgregarImagenMedica
from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.comandos.eliminar_imagen_medica import \
    EliminarImagenMedica
from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.mapeadores import MapeadorImagenMedicaDTOJson
from src.ingesta_automatizada.modulos.ingesta_automatizada.aplicacion.queries.obtener_imagen_medica import \
    ObtenerImagenMedica
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.despachadores import Despachador
from src.ingesta_automatizada.seedwork.aplicacion.queries import ejecutar_query
from src.ingesta_automatizada.seedwork.dominio.excepciones import ExcepcionDominio
from src.ingesta_automatizada.seedwork.presentacion import api
from src.ingesta_automatizada.modulos.ingesta_automatizada.infraestructura.schema.v1.comandos import \
    ComandoAgregarImagenMedica, \
    ComandoEliminarImagenMedica

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
            url=imagen_medica_dto.url,
            flag=imagen_medica_dto.flag,
            fecha_creacion=imagen_medica_dto.fecha_creacion,
            regiones_anatomicas=imagen_medica_dto.regiones_anatomicas,
            diagnostico=imagen_medica_dto.diagnostico
        )

        despachador = Despachador()
        despachador.publicar_comando(comando=comando, topico="comandos-imagen-medica",
                                     esquema=ComandoAgregarImagenMedica)
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@blueprint.route('/imagen_medica-query/<id>', methods=['GET'])
def dar_imagen_medica(id=None):
    try:
        query = ejecutar_query(ObtenerImagenMedica(id))
        mapeador_imagen_medica = MapeadorImagenMedicaDTOJson()
        return mapeador_imagen_medica.dto_a_externo(query.resultado)
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=404, mimetype='application/json')


@blueprint.route('/imagen_medica-comando/<id>', methods=['DELETE'])
def eliminar_imagen_medica(id=None):
    comando = EliminarImagenMedica(
        id=id
    )
    despachador = Despachador()
    despachador.publicar_comando(comando=comando, topico="comandos-compensacion-imagen-medica",
                                 esquema=ComandoEliminarImagenMedica)
    return Response('{}', status=202, mimetype='application/json')
