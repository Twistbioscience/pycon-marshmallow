from sqlalchemy.ext.mutable import Mutable
from weakref import WeakSet


class MutableBase(Mutable):
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, cls):
            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value


class NestedMutableBase:
    def __init__(self):
        self._listeners = WeakSet()

    def register(self, listener):
        callback = getattr(listener, 'changed', None)
        if callback is None:
            raise ValueError('Listener does not have callback changed')
        if not callable(callback):
            raise ValueError('Listener callback is not callable')
        self._listeners.add(listener)

    def unregister(self, listener):
        self._listeners.remove(listener)

    def changed(self):
        for listener in self._listeners:
            listener.changed()
