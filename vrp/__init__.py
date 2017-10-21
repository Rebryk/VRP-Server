import logging

from .server import Server
from .yandex import YSRecognizer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

__all__ = ("Server", "YSRecognizer")
