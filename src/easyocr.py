from pipeline import File, Pipeline, Variable, entity, pipe, current_configuration
from pipeline.cloud import compute_requirements, pipelines
from pipeline.cloud.environments import create_environment

import easyocr

# Getting environment variables
import os

# Initializing environment variables
# login   = os.environ["USERNAME"]
# pl      = os.environ["PIPELINE"]
# env     = os.environ["ENVIRONMENT"]

current_configuration.set_debug_mode(True)

login = 'uriel'
pl = 'easyocr'
env = 'easyocr-env'


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

        self.model_ru_en = easyocr.Reader(['ru', 'en'])
        self.model_en = easyocr.Reader(['en'])

    @pipe
    def image2ru_en(self, image: File) -> str:
        out = self.model_ru_en.readtext(image, detail=0, paragraph=True)
        # out = self.model_ru_en.readtext(image) # in production
        return out

    @pipe
    def image2en(self, image: File) -> str:
        out = self.model_en.readtext(image, detail=0, paragraph=True)
        # out = self.model_ru_en.readtext(image) # in production
        return out


with Pipeline() as builder:
    image = Variable(
        File,
        choices=['ru_en', 'en'],
        title="Image File",
        description="Upload a .png, .jpg or other image file to be captioned. You can also provide URL",
    )

    model = EasyOCRModel()
    my_file = File.from_object(model)  # Create a file object
    model.load(my_file)

    if choices == 'ru_en':
        output = model.image2ru_en(image)
    elif choices == 'en':
        output = model.image2en(image)

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

# try:
#     env_id = create_environment(
#         name=my_env_name,
#         python_requirements=[
#             "easyocr==1.7.1",
#             "opencv-python-headless==4.8.1.78",
#             "torch==2.1.2",
#             "torchvision==0.16.2",
#         ],
#     )
# except Exception:
#     pass

# pipelines.upload_pipeline(
#     my_pl,
#     my_pl_name,
#     environment_id_or_name=my_env_name,
#     required_gpu_vram_mb=5_000,
#     accelerators=[
#         compute_requirements.Accelerator.nvidia_t4,
#     ],
# )
