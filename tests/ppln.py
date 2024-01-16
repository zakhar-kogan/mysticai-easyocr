import os
# Login to pipeline-ai
os.system(f"pipeline cluster login catalyst-api pipeline_sk_f6cLHs3LUKObckk7z9bEzM4Jbu0aDIGY -u https://www.mystic.ai -a")

from pipeline.cloud.pipelines import run_pipeline
from pipeline.objects import File

# Language map/values for reference
LANG_MAP = {
    "English": "en",
    "Russian": "ru",
}

output = run_pipeline(
        "uriel/easyocr-r:v31",
        File(
            # URL
            # url="https://api.telegram.org/file/bot6678109627:AAFmbzFijiTcICi_dWSiFjeVuIiWbG9cjP8/photos/file_15.jpg"
            # Local files
            path="tests/media/ex.jpeg",
        ),
        # Language
        "ru",
        async_run=False
    )
# Print output if it's not NoneType
if output.result is not None:
    print(output.result.result_array())
else:
    print("Error:")
    print(output.error)
