import logging
from io import BytesIO
from uuid import UUID

import pydub
import speech_recognition as sr
from aiohttp import ClientSession

from .recognizer import SpeechRecognizer


class GRecognizer(SpeechRecognizer):
    def __init__(self):
        self.asr = sr.Recognizer()
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    async def _download_ogg(session: ClientSession, url: str):
        async with session.get(url=url) as response:
            return await response.read()

    @staticmethod
    def _transcribe_content(content):
        """Transcribe the given audio file"""

        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types
        client = speech.SpeechClient()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=48000,
            language_code="ru-RU")

        return client.recognize(config, audio)

    async def recognize(self, url: str, uuid: UUID):
        async with ClientSession() as session:
            raw_mp3 = BytesIO(await self._download_ogg(session, url))
            raw_flac = BytesIO()

            # convert audio file from mp3 to flac
            pydub.AudioSegment.from_mp3(raw_mp3).export(raw_flac, format="flac")

            # read content
            content = raw_flac.read()

            response = self._transcribe_content(content)
            text = response.results[0].alternatives[0].transcript if len(response.results) else ""
            self.logger.debug("Parse: {}".format(text))
            return text
