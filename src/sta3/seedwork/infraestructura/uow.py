import threading
from abc import ABC, abstractmethod
from enum import Enum

from pydispatch import dispatcher

from src.sta3.seedwork.dominio.entidades import AgregacionRaiz


class Lock(Enum):
    OPTIMISTA = 1
    PESIMISTA = 2


class Batch:
    def __init__(self, operacion, lock: Lock, *args, **kwargs):
        self.operacion = operacion
        self.args = args
        self.lock = lock
        self.kwargs = kwargs


class UnidadTrabajo(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _obtener_eventos(self, batches=None):
        batches = self.batches if batches is None else batches
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    return arg.eventos
        return list()

    @abstractmethod
    def _limpiar_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError

    def commit(self):
        self._publicar_eventos_post_commit()
        self._limpiar_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._limpiar_batches()

    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch)

    def _publicar_eventos_dominio(self, batch):
        for evento in self._obtener_eventos(batches=[batch]):
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

    def _publicar_eventos_post_commit(self):
        for evento in self._obtener_eventos():
            dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)


class UnidadTrabajoSingleton:
    """Implementación de Singleton para la Unidad de Trabajo."""
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        """Devuelve la instancia única de UnidadTrabajoSQLAlchemy."""
        from src.sta3.config.uow import UnidadTrabajoSQLAlchemy
        if UnidadTrabajoSingleton._instance is None:
            with UnidadTrabajoSingleton._lock:
                if UnidadTrabajoSingleton._instance is None:
                    UnidadTrabajoSingleton._instance = UnidadTrabajoSQLAlchemy()
        return UnidadTrabajoSingleton._instance


def unidad_de_trabajo() -> UnidadTrabajo:
    """Devuelve la instancia única de la unidad de trabajo."""
    return UnidadTrabajoSingleton.get_instance()


class UnidadTrabajoPuerto:

    @staticmethod
    def commit():
        uow = unidad_de_trabajo()
        uow.commit()

    @staticmethod
    def rollback(savepoint=None):
        uow = unidad_de_trabajo()
        uow.rollback(savepoint=savepoint)

    @staticmethod
    def savepoint():
        uow = unidad_de_trabajo()
        uow.savepoint()

    @staticmethod
    def dar_savepoints():
        uow = unidad_de_trabajo()
        return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = unidad_de_trabajo()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)
