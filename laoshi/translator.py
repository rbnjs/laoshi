"""Module for the Translator classes"""
from googletrans import Translator as GTranslator


class Translator:
    """Translator class"""

    def __init__(self):
        """Initiliazer for Translator"""
        self.translator = GTranslator()

    def translate(self, text: str, dest: str = "en") -> str:
        """Translate a text into english (by default)"""
        return self.translator.translate(text, dest=dest).text
