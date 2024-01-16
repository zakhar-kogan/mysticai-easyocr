import os  # For operating system related functionalities

from PIL import Image  # For working with images
import io
from numpy import asarray  # For numerical operations
import easyocr  # For performing optical character recognition

from pipeline import (  # For working with pipelines
    File,
    Pipeline,
    Variable,
    entity,
    pipe,
    current_configuration
)

current_configuration.set_debug_mode(True)

LANG_MAP = {
    'Russian': 'ru',
    'English': 'en',
    'Spanish': 'es',
    'Portuguese': 'pt',
    'Uzbek': 'uz',
    'French': 'fr',
    'Farsi': 'fa',
    'Indonesian': 'id',
}

@entity
class EasyOCRModel:
    def __init__(self):
        ...

    @pipe(on_startup=True, run_once=True)
    def load(self) -> None:
        # this needs to run only once to load the model into memory

        self.model_ru_en = easyocr.Reader([LANG_MAP['English'], LANG_MAP['Russian']], recognizer='Transformer')
        self.model_es_en = easyocr.Reader([LANG_MAP['English'], LANG_MAP['Spanish']], recognizer='Transformer')
        self.model_pt_en = easyocr.Reader([LANG_MAP['English'], LANG_MAP['Portuguese']], recognizer='Transformer')
        self.model_uz_en = easyocr.Reader([LANG_MAP['English'], LANG_MAP['Uzbek']], recognizer='Transformer')
        self.model_fr_en = easyocr.Reader([LANG_MAP['English'], LANG_MAP['French']], recognizer='Transformer')
        self.model_fa_en = easyocr.Reader([LANG_MAP['English'], LANG_MAP['Farsi']], recognizer='Transformer')
        self.model_id_en = easyocr.Reader([LANG_MAP['English'], LANG_MAP['Indonesian']], recognizer='Transformer')
        self.model_en = easyocr.Reader([LANG_MAP['English']], recognizer='Transformer')

        self.model_map = {
            'ru': self.model_ru_en,
            'es': self.model_es_en,
            'pt_br': self.model_pt_en,
            'uz': self.model_uz_en,
            'fr': self.model_fr_en,
            'fa': self.model_fa_en,
            'id': self.model_id_en,
            'en': self.model_en,
        }

    @pipe
    def predict(self, image: File, lang: str) -> str:
        """
        Performs optical character recognition (OCR) on the provided image file.

        Parameters:
        image (File): This should be a .png, .jpg, or other image file; or a URL when calling by API.
        lang (str): The language to use for OCR. Can be either 'ru'/Russian or 'en'/English. Defaults to English.

        Returns:
        str: The OCR output as a string. If the language is Russian, the function uses a model trained on both English and Russian. If the language is English or any other value, the function uses a model trained only on English.

        Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the language is not supported.
        """
        # Open the file in binary mode and read it into a BytesIO object
        img = asarray(Image.open(io.BytesIO(image.path.read_bytes())).convert("L"))
        out = ''

        match lang:
            case 'ru' | 'Russian':
                out = self.model_ru_en.readtext(img, paragraph=True)
            case 'en' | 'English':
                out = self.model_en.readtext(img, paragraph=True)
            case 'es' | 'Spanish':
                out = self.model_es_en.readtext(img, paragraph=True)
            case 'pt' | 'pt_br' | 'Portuguese':
                out = self.model_pt_en.readtext(img, paragraph=True)
            case 'uz' | 'Uzbek':
                out = self.model_uz_en.readtext(img, paragraph=True)
            case 'fr' | 'French':
                out = self.model_fr_en.readtext(img, paragraph=True)
            case 'fa' | 'Farsi':
                out = self.model_fa_en.readtext(img, paragraph=True)
            case 'id' | 'Indonesian':
                out = self.model_id_en.readtext(img, paragraph=True)
            case _:
                out = self.model_en.readtext(img, paragraph=True)
        return out


with Pipeline() as builder:
    image = Variable(
        File,
        title="Image File",
        description="Upload a .png, .jpg or other image file to be captioned, or a URL with API",
    )

    lang_choice = Variable(
        str,
        choices=list(LANG_MAP.keys()),
        title="Language",
        default="Russian",
        description="OCR language to use. English if not specified.",
    )

    model = EasyOCRModel()
    model.load()

    output = model.predict(image, lang_choice)

    builder.output(output)

my_pl = builder.get_pipeline()
