"""Module which provides the FlashCard generator class."""
import tempfile
import random
import uuid
import os
import shutil
import genanki
from laoshi.converter import Converter
from laoshi.translator import Translator
from laoshi.speaker import Speaker, Speech

FIELDS_LIST = [
    {"name": "Original"},
    {"name": "Traditional"},
    {"name": "Pinyin"},
    {"name": "Translation"},
    {"name": "Sound"},
]

MODEL_CSS = """
.card {
    font-family: arial;
    font-size: 48px;
    text-align: center;
    color: black;
    background-color: white;
    line-height: 2em;
}
"""

ANSWER = '{{FrontSide}}<hr id="answer">{{Original}}<br>{{Traditional}} \
<br>{{Pinyin}}<br>{{Translation}}</div>'

CHINESE_TO_ENGLISH = genanki.Model(
    1450786248,
    "Chinese to English",
    fields=FIELDS_LIST,
    css=MODEL_CSS,
    templates=[
        {
            "name": "Card {{Original}} English to Chinese",
            "qfmt": '<div class="card">{{Original}}<br>{{Traditional}}',
            "afmt": ANSWER,
        },
    ],
)

ENGLISH_TO_CHINESE = genanki.Model(
    1480566997,
    "English to Chinese",
    fields=FIELDS_LIST,
    css=MODEL_CSS,
    templates=[
        {
            "name": "Card {{Original}} English to Chinese",
            "qfmt": '<div class="card">{{Translation}}',
            "afmt": ANSWER,
        },
    ],
)

AUDIO_ONLY = genanki.Model(
    1899733999,
    "Audio Only",
    fields=FIELDS_LIST,
    css=MODEL_CSS,
    templates=[
        {
            "name": "Card {{Original}} Audio",
            "qfmt": '<div class="card">{{Sound}}',
            "afmt": ANSWER,
        },
    ],
)


def get_unique_id() -> int:
    """Creates a unique ID"""
    return random.randrange(1 << 30, 1 << 31)


class FlashCard:
    """Class which holds all the information needed for
    flashcards
    """

    def __init__(
        self,  # pylint: disable=too-many-arguments
        simplified: str,
        traditional: str,
        pinyin: str,
        translation: str,
        sound_file: str,
        sound_path: str,
    ):
        self.simplified = simplified
        self.traditional = traditional
        self.pinyin = pinyin
        self.translation = translation
        self.sound_file = sound_file
        self.sound_path = sound_path

    def get_fields(self) -> list[str]:
        """Get fields from Flashcard except from sound files."""
        return [self.simplified, self.traditional, self.pinyin, self.translation]

    def get_media_path(self) -> str:
        """Get media path"""
        return self.sound_path


class FlashCardGenerator:
    """Generates flashcards"""

    def __init__(self, tempfolder: str = ""):
        """
        Parameters:
            self: The instantiated object
            tempfolder: Folder to use to save the audio files.
        """
        self.tempfolder = tempfolder

    def __enter__(self):
        """
        It creates the temporary folder when using it when the with statement
        """
        self.tempfolder = tempfile.mkdtemp()
        return self

    def create_sound(self, hanzitext: str) -> Speech:
        """
        Creates a sound in a temporal folder.
        Parameters:
            self (FlashCardGenerator): the instantiated object.
            hanzitext (str): Chinese text
        Returns:
            Speech: The saved speech object
        """
        speech: Speech = Speaker.text_to_speech(hanzitext)
        name = f"{str(uuid.uuid4())}.mp3"
        path = f"{self.tempfolder}/{name}"
        speech.save(f"[sound:{name}]", path)
        return speech

    def from_traditional(self, hanzi: str) -> FlashCard:
        """
        Creates a FlashCard from a traditional text
        Parameters:
            self: The object
            hanzi: Traditional chinese text
        Returns:
            FlashCard: Returns an instantiated FlashCard
        """
        speech: Speech = self.create_sound(hanzi)
        return FlashCard(
            simplified=Converter.to_simplified(hanzi),
            traditional=hanzi,
            pinyin=Converter.to_pinyin(hanzi),
            translation=Translator().translate(hanzi),
            sound_path=speech.path,
            sound_file=speech.name,
        )

    def from_simplified(self, hanzi: str) -> FlashCard:
        """
        Creates a FlashCard from a traditional text
        Parameters:
            self: The object
            hanzi: Simplified chinese text
        Returns:
            FlashCard: Returns an instantiated FlashCard
        """
        speech: Speech = self.create_sound(hanzi)
        return FlashCard(
            simplified=hanzi,
            traditional=Converter.to_traditional(hanzi),
            pinyin=Converter.to_pinyin(hanzi),
            translation=Translator().translate(hanzi),
            sound_path=speech.path,
            sound_file=speech.name,
        )

    def __exit__(self, *_args):
        """
        Needed to delete the temporary folder when exiting a with statement.
        """
        if os.path.exists(self.tempfolder):
            shutil.rmtree(self.tempfolder)


class DeckManager:  # pylint: disable=too-few-public-methods
    """Manages and creates Anki Decks"""

    def __init__(self, deck_name: str):
        """Init method"""
        self.deck_name = deck_name

    def create_deck(self, flashcard: FlashCard):
        """Creates a deck from one FlashCard"""
        deck = genanki.Deck(get_unique_id(), self.deck_name)
        package = genanki.Package(deck)
        output = f"{deck.name}.apkg"
        deck.add_note(
            genanki.Note(
                guid=get_unique_id(),
                model=CHINESE_TO_ENGLISH,
                fields=flashcard.get_fields(),
            )
        )
        deck.add_note(
            genanki.Note(
                guid=get_unique_id(),
                model=ENGLISH_TO_CHINESE,
                fields=flashcard.get_fields(),
            )
        )
        deck.add_note(
            genanki.Note(
                guid=get_unique_id(), model=AUDIO_ONLY, fields=flashcard.get_fields()
            )
        )
        package.media_files = [flashcard.get_media_path()]
        package.write_to_file(output)
