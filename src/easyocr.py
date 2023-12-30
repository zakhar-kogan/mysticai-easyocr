
from io import BytesIO
from PIL import Image
from numpy import asarray

from pipeline import File, Pipeline, Variable, entity, pipe
from pipeline.cloud import compute_requirements, pipelines
from pipeline.cloud.environments import create_environment
from pipeline import current_configuration

import easyocr
import torch
# import opencv_python_headless

# Getting environment variables
import os

# Initializing environment variables
# login   = os.environ["USERNAME"]
# pl      = os.environ["PIPELINE"]
# env     = os.environ["ENVIRONMENT"]

current_configuration.set_debug_mode(True)

login   = 'uriel'
pl      = 'easyocr'
env     = 'easyocr-env'

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
        self.model = easyocr.Reader(['ru', 'en']) 

    @pipe
    def predict(self, image: File) -> str:
        raw_image = asarray(Image.open(BytesIO(image.path.read_bytes())))
        out = self.model.readtext(raw_image, detail=0, paragraph=True)
        return out


with Pipeline() as builder:
    image = Variable(
        File,
        title="Image File",
        description="Upload a .png, .jpg or other image file to be captioned. You can also provide URL",
    )
    
    model = EasyOCRModel()
    my_file = File.from_object(model) # Create a file object
    model.load(my_file)

    output = model.predict(image)
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