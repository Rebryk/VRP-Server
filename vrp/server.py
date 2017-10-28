import logging
import uuid
from http import HTTPStatus
from json.decoder import JSONDecodeError

from aiohttp import web

from .recognizer import SpeechRecognizer


class Server:
    def __init__(self, asr: SpeechRecognizer, use_cache=True):
        self.app = web.Application()
        self.app.router.add_post('/recognize', self.recognize_request)
        self.asr = asr
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self, host: int, port: int):
        web.run_app(self.app, host=host, port=port)

    async def recognize_request(self, request):
        try:
            params = await request.json()
        except JSONDecodeError as e:
            return web.Response(text="failed to parse request: {}".format(str(e)), status=HTTPStatus.BAD_REQUEST)

        url = params.get("url", None)
        user_id = params.get("user_id", None)

        if url is None and url is None:
            return web.Response(text="url is not specified", status=HTTPStatus.BAD_REQUEST)

        if url and not self._is_mp3(url):
            return web.Response(text="invalid url to mp3 file", status=HTTPStatus.BAD_REQUEST)

        try:
            text = await self.recognize_audio(url, user_id)
        except Exception as e:
            self.logger.error("Failed to recognize audio: {}".format(str(e)))
            return web.Response(text="failed to recognize audio", status=HTTPStatus.SERVICE_UNAVAILABLE)

        return web.Response(text=text, status=HTTPStatus.OK)

    async def recognize_audio(self, url, user_id):
        text = await self.asr.recognize(url, None)

        return text

    @staticmethod
    def _is_mp3(url):
        return url.endswith(".mp3")

    @staticmethod
    def _is_ogg(url):
        return url.endswith(".ogg")
