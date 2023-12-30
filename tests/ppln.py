# Should have pipeline-ai installed to use this snippet

from pipeline.cloud.pipelines import run_pipeline
from pipeline.objects import File
    
output = run_pipeline(
        "uriel/easyocr:v22",
        File(
            # Telegram URL working
            # url="https://api.telegram.org/file/bot6678109627:AAFmbzFijiTcICi_dWSiFjeVuIiWbG9cjP8/photos/file_15.jpg"
            # Local files
            path="tests/media/test.webp",
        )
    )
# Print output if it's not NoneType
if output.result is not None:
    print(output.result.result_array())
else:
    print("Error:")
    print(output.error)