from uuid import UUID


class SpeechRecognizer:
    """Base recognizer class"""

    async def recognize(self, url: str, uuid: UUID):
        pass
