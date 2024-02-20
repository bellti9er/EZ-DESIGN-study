import logging
from typing import Dict, Any


class SingletonMeta(type):
    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            logging.info(f"Creating a new instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            logging.info(f"Using existing instance of {cls.__name__}")
        return cls._instances[cls]
