import os

from flask import Flask, jsonify
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import src.sta.modulos.ingesta_automatizada.aplicacion


def importar_modelos_alchemy():
    import src.sta.modulos.ingesta_automatizada.infraestructura.dto


def comenzar_consumidor(aplicacion):
    import threading
    import src.sta.modulos.ingesta_automatizada.infraestructura.consumidores as ingesta_automatizada

    threading.Thread(target=ingesta_automatizada.suscribirse_a_eventos).start()

    threading.Thread(target=ingesta_automatizada.suscribirse_a_comandos).start()


def create_app():
    aplicacion = Flask(__name__, instance_relative_config=True)

    aplicacion.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI',
                                                             'sqlite:///' + os.path.join(basedir, 'database.db'))
    aplicacion.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    aplicacion.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    aplicacion.config['SESSION_TYPE'] = 'filesystem'

    from src.sta.config.db import init_db
    init_db(aplicacion)

    from src.sta.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()
    comenzar_consumidor(aplicacion)

    with aplicacion.app_context():
        db.create_all()

    from . import ingesta_automatizada

    aplicacion.register_blueprint(ingesta_automatizada.blueprint)

    @aplicacion.route("/spec")
    def spec():
        swag = swagger(aplicacion)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @aplicacion.route("/health")
    def health():
        return {"status": "up"}

    return aplicacion
