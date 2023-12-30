from pipeline.cloud.pipelines import run_pipeline
import urllib.request

from pipeline import Pipeline, Variable, entity, pipe
from pipeline.objects import File

@entity
class ReturnAFile:
    @pipe
    def get_file(self, random_string: str) -> File:
        file_path = "/tmp/image.jpg"
        urllib.request.urlretrieve(
            "https://storage.mystic.ai/run_files/31/7e/317e304d-e816-4036-86b2-7ad82b208b70/image-0.jpg",  # noqa
            file_path,
        )

        output_image = File(path=file_path)

        return output_image

output = run_pipeline(
	#pipeline pointer or ID
	"uriel/easyocr:v22",
	#:Image File
	"file://example.jpeg",
	async_run = False,
)

run_pipeline(
	"uriel/easyocr:v22",
	
)
print(output)