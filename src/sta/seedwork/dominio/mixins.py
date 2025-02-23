from src.sta.seedwork.dominio.excepciones import ReglaNegocioExcepcion
from src.sta.seedwork.dominio.reglas import ReglaNegocio


class ValidarReglasMixin:
    def validar_regla(self, regla: ReglaNegocio):
        if not regla.es_valido():
            raise ReglaNegocioExcepcion(regla)