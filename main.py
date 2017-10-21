import logging
import ujson as json

from vrp import Server, YSRecognizer

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    with open("config/config.json") as f:
        config = json.load(f)

    with open("config/yandex.json") as f:
        yandex_config = json.load(f)

    yandex_asr = YSRecognizer(yandex_config["api_key"])

    server = Server(asr=yandex_asr)

    logger.debug("Starting server...")
    server.start(host=config["host"],
                 port=config["port"])
