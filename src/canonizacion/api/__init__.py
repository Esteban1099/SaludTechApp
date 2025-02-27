import os
import threading

from flask import Flask, jsonify
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import src.canonizacion.modulos.canonizacion.aplicacion


def importar_modelos_alchemy():
    import src.canonizacion.modulos.canonizacion.infraestructura.dto


def iniciar_hilos(app):
    """Función para iniciar los hilos de suscripción dentro del contexto de Flask."""
    import src.canonizacion.modulos.canonizacion.infraestructura.consumidores as ingesta_automatizada

    def run_suscribirse_a_eventos():
        with app.app_context():  # Asegura que Flask tenga contexto en este hilo
            ingesta_automatizada.suscribirse_a_eventos()

    def run_suscribirse_a_comandos():
        with app.app_context():  # Asegura que Flask tenga contexto en este hilo
            ingesta_automatizada.suscribirse_a_comandos()

    # Iniciar los hilos en modo daemon (para que terminen cuando la app se cierre)
    threading.Thread(target=run_suscribirse_a_eventos, daemon=True).start()
    threading.Thread(target=run_suscribirse_a_comandos, daemon=True).start()


def create_app():
    aplicacion = Flask(__name__)

    aplicacion.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI',
                                                             'sqlite:///' + os.path.join(basedir, 'database.db'))
    aplicacion.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    aplicacion.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    aplicacion.config['SESSION_TYPE'] = 'filesystem'

    from src.canonizacion.config.db import init_db
    init_db(aplicacion)

    from src.canonizacion.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with aplicacion.app_context():
        db.create_all()
        iniciar_hilos(aplicacion)

    from . import canonizacion

    aplicacion.register_blueprint(canonizacion.blueprint)

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
