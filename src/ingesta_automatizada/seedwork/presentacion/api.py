from flask import Blueprint


def crear_blueprint(nombre: str, prefijo_url):
    return Blueprint(nombre, __name__, url_prefix=prefijo_url)
