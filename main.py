import logging
import ujson as json

from vrp import Server, YSRecognizer
from vrp.google import GRecognizer

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    with open("config/config.json") as f:
        config = json.load(f)

    with open("config/yandex.json") as f:
        yandex_config = json.load(f)

    logger.debug("Starting server...")

    yandex_asr = YSRecognizer(yandex_config["api_key"],
                              topic="maptalks")

    server = Server(asr=yandex_asr)
    server.start(host=config["host"],
                 port=config["port"])
