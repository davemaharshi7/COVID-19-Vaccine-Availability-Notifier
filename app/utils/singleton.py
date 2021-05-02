"""Singletone Class Implementation."""


class Singleton(type):
    """Singleton Class implemetation."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """To redirect single instance object for given class."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
