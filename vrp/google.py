import logging
from io import BytesIO
from uuid import UUID

import pydub
from aiohttp import ClientSession

from .recognizer import SpeechRecognizer


class GRecognizer(SpeechRecognizer):
    EMPTY_UUID = UUID("00000000000000000000000000000000")

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    async def _download_mp3(session: ClientSession, url: str):
        async with session.get(url=url) as response:
            return await response.read()

    @staticmethod
    def _upload_audio(filename, data):
        from google.cloud import storage

        client = storage.Client("voice-recognition-plugin")
        bucket = client.get_bucket("vrp-audio")
        blob = storage.Blob(filename, bucket)

        blob.upload_from_file(data)

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

    @staticmethod
    def _transcribe_content_async(gcs_uri: str):
        """Transcribe the given audio file"""

        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types
        client = speech.SpeechClient()

        audio = types.RecognitionAudio(uri=gcs_uri)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=48000,
            language_code="ru-RU")

        operation = client.long_running_recognize(config, audio)
        return operation.result(timeout=90)

    async def recognize(self, url: str, uuid: UUID):
        async with ClientSession() as session:
            raw_mp3 = BytesIO(await self._download_mp3(session, url))
            raw_flac = BytesIO()

            # convert audio file from mp3 to flac
            pydub.AudioSegment.from_mp3(raw_mp3).export(raw_flac, format="flac")

            length = raw_flac.__sizeof__() / 25000

            if length < 59:
                # read content
                content = raw_flac.read()
                response = self._transcribe_content(content)
            else:
                self.logger.debug("Loading file to google storage")
                file_name = uuid.hex if uuid else GRecognizer.EMPTY_UUID.hex
                self._upload_audio(file_name, raw_flac)
                response = self._transcribe_content_async("gs://vrp-audio/{}".format(file_name))

            text = response.results[0].alternatives[0].transcript if len(response.results) else ""
            self.logger.debug("Parse: {}".format(text))
            return text
