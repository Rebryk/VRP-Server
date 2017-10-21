import logging
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from uuid import UUID

from aiohttp import ClientSession

from .recognizer import SpeechRecognizer


class YSRecognizer(SpeechRecognizer):
    EMPTY_UUID = UUID("00000000000000000000000000000000")
    URL = "https://asr.yandex.net/asr_xml?"

    def __init__(self,
                 api_key: str,
                 topic: str = "notes",
                 disable_antimat: bool = True,
                 capitalize: bool = True,
                 punctuation: bool = True):
        self.api_key = api_key
        self.topic = topic
        self.disable_antimat = disable_antimat
        self.capitalize = capitalize
        self.punctuation = punctuation
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    async def _download_ogg(session: ClientSession, url: str):
        async with session.get(url=url) as response:
            return await response.read()

    @staticmethod
    def _get_url(params):
        return YSRecognizer.URL + urlencode(params)

    @staticmethod
    def _get_headers(length: int):
        return {
            "Content-Type": "audio/ogg;codecs=opus",
            "Content-Length": str(length)
        }

    async def recognize(self, url: str, uuid: UUID):
        async with ClientSession() as session:
            params = {
                "uuid": uuid.hex if uuid else YSRecognizer.EMPTY_UUID.hex,
                "topic": self.topic,
                "key": self.api_key,
                "disableAntimat": str(self.disable_antimat).lower(),
                "capitalize": str(self.capitalize).lower(),
                "punctuation": str(self.punctuation).lower()
            }

            file = await self._download_ogg(session, url)
            req_url = self._get_url(params)
            req_headers = self._get_headers(len(file))

            async with session.post(url=req_url, headers=req_headers, data=file) as response:
                body = await response.read()
                root = ET.fromstring(body.decode("utf8"))

                text = ""

                for child in root:
                    self.logger.debug("Parse: {}".format(child.text))

                    if text == "":
                        text = child.text

                return text
