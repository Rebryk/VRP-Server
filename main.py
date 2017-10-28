import logging
import ujson as json

from vrp import Server, YSRecognizer
from vrp.google import GRecognizer

logger = logging.getLogger(__name__)

#if __name__ == "__main__":
with open("config/config.json") as f:
    config = json.load(f)

logger.debug("Starting server...")

goolge_asr = GRecognizer()

server = Server(asr=goolge_asr, use_cache=False)
server.start(host=config["host"],
             port=config["port"])

app = server.app
