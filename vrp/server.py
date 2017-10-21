import logging
import uuid
from http import HTTPStatus
from json.decoder import JSONDecodeError

from aiohttp import web
from pony import orm

from data import Audio, User
from .recognizer import SpeechRecognizer


class Server:
    def __init__(self, asr: SpeechRecognizer, use_cache=True):
        self.app = web.Application()
        self.app.router.add_post('/recognize', self.recognize_request)
        self.asr = asr
        self.use_cache = use_cache
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

        if url and not self._is_ogg(url):
            return web.Response(text="invalid url to ogg file", status=HTTPStatus.BAD_REQUEST)

        try:
            with orm.db_session:
                text = await self.recognize_audio(url, user_id)
        except Exception as e:
            self.logger.error("Failed to recognize audio: {}".format(str(e)))
            return web.Response(text="failed to recognize audio", status=HTTPStatus.SERVICE_UNAVAILABLE)

        return web.Response(text=text, status=HTTPStatus.OK)

    async def recognize_audio(self, url, user_id):
        user = None

        if user_id:
            user = User.get(id=user_id) or User(id=user_id, uuid=uuid.uuid4())

        # return text if audio was recognized before
        if self.use_cache:
            audio = Audio.get(url=url)

            if audio and audio.text is not None:
                return audio.text

        text = await self.asr.recognize(url, user.uuid if user else None)

        try:
            if self.use_cache:
                Audio(url=url, text=text, user=user)
        except Exception as e:
            self.logger.error("Failed to insert audio: {}".format(str(e)))

        return text

    @staticmethod
    def _is_mp3(url):
        return url.endswith(".mp3")

    @staticmethod
    def _is_ogg(url):
        return url.endswith(".ogg")
