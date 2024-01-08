import os  # For operating system related functionalities
import dotenv  # For loading environment variables

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
from pipeline.cloud import (  # For working with cloud resources
    compute_requirements,
    pipelines
)
from pipeline.cloud.environments import create_environment  # For creating cloud environments

dotenv.load_dotenv()

# Initializing environment variables
login   = os.environ["USERNAME"]
pl      = os.environ["PIPELINE"]
env     = os.environ["ENVIRONMENT"]

current_configuration.set_debug_mode(True)

LANG_MAP = {
    'Russian': 'ru',
    'English': 'en',
}

@entity
class EasyOCRModel:
    def __init__(self):
        ...

    @pipe(on_startup=True, run_once=True)
    def load(self, model_file: File) -> None:
        # this needs to run only once to load the model into memory
        import dill
        with model_file.path.open("rb") as file:
            self.pipe = dill.load(file)

        self.model_ru_en = easyocr.Reader([LANG_MAP['English'], LANG_MAP['Russian']], recognizer='Transformer')
        self.model_en = easyocr.Reader([LANG_MAP['English']], recognizer='Transformer')

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
    my_file = File.from_object(model)  # Create a file object
    model.load(my_file)

    output = model.predict(image, lang_choice)

    builder.output(output)

# # Local testing
# model = EasyOCRModel()
# print("Loading model...")
# model.load()
# print("Model loaded")
# output = model.predict("example.jpeg")
# print("Prediction:")
# print(output)

my_pl = builder.get_pipeline()

my_pl_name = f"{login}/{pl}"
my_env_name = f"{login}/{env}"

try:
    env_id = create_environment(
        name=my_env_name,
        python_requirements=[
            "easyocr==1.7.1",
            "opencv-python-headless==4.9.0.80",
            "torch==2.1.2",
            "torchvision==0.16.2",
        ],
    )
except Exception:
    pass

pipelines.upload_pipeline(
    my_pl,
    my_pl_name,
    environment_id_or_name=my_env_name,
    required_gpu_vram_mb=5_000,
    accelerators=[
        compute_requirements.Accelerator.nvidia_t4,
    ],
)
