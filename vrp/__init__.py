import logging

from .server import Server
from .yandex import YSRecognizer
from .google import GRecognizer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

__all__ = ("Server", "YSRecognizer", "GRecognizer")
