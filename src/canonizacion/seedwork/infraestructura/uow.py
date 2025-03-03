import threading
import uuid
from abc import ABC, abstractmethod
from enum import Enum

from pydispatch import dispatcher

from src.canonizacion.seedwork.dominio.entidades import AgregacionRaiz


class Lock(Enum):
    OPTIMISTA = 1
    PESIMISTA = 2


class Batch:
    def __init__(self, operacion, *args, **kwargs):
        self.operacion = operacion
        self.args = args
        self.kwargs = kwargs
        self.lock = threading.RLock()


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

    def registrar_batch(self, operacion, *args, **kwargs):
        batch = Batch(operacion, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch)
        return batch

    def _publicar_eventos_dominio(self, batch):
        for evento in self._obtener_eventos(batches=[batch]):
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

    def _publicar_eventos_post_commit(self):
        for evento in self._obtener_eventos():
            dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)


class UnidadTrabajoSingleton(type):
    _instance = None
    _lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(UnidadTrabajoSingleton, cls).__call__(*args, **kwargs)
        return cls._instance


class UnidadTrabajoPuerto(metaclass=UnidadTrabajoSingleton):

    @classmethod
    def commit(cls):
        uow = cls.get_instance()
        uow.commit()

    @classmethod
    def rollback(cls, savepoint=None):
        uow = cls.get_instance()
        uow.rollback(savepoint=savepoint)

    @classmethod
    def savepoint(cls):
        uow = cls.get_instance()
        return uow.savepoint()

    @classmethod
    def dar_savepoints(cls):
        uow = cls.get_instance()
        return uow.savepoints()

    @classmethod
    def registrar_batch(cls, operacion, *args, **kwargs):
        uow = cls.get_instance()
        return uow.registrar_batch(operacion, *args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Devuelve la instancia única de UnidadTrabajoSQLAlchemy."""
        from src.canonizacion.config.uow import UnidadTrabajoSQLAlchemy
        if UnidadTrabajoSingleton._instance is None:
            with UnidadTrabajoSingleton._lock:
                if UnidadTrabajoSingleton._instance is None:
                    UnidadTrabajoSingleton._instance = UnidadTrabajoSQLAlchemy()
        return UnidadTrabajoSingleton._instance
