# Imports
import requests
import os
import mimetypes

# Getting the API key
if os.getenv("API_KEY"):
    api_key = os.getenv("API_KEY")
else:
    api_key = "pipeline_sk_iIGN0tU7Jifjdmycp-gOVoqJyYjLAVQA"

# Headers
headers = {
    'Authorization': f"Bearer {api_key}",
    'Content-Type': 'application/json'
}

def upload_img(path: str) -> tuple:
    upload_url = "https://www.mystic.ai/v3/pipeline_files"
    img_name = os.path.basename(path)
    mime = mimetypes.guess_type(path)[0]
    if img_name[-4:] == "webp":
        mime = "image/webp"

    if not os.path.exists(path):
        raise FileNotFoundError(f"No file found at {path}")

    if not mime:
        raise ValueError(f"Could not determine MIME type for file {path}")

    with open(path, "rb") as img_file:
        files = { "pfile": (img_name, img_file, mime) }
        headers = {
            "accept": "application/json",
            "authorization": "Bearer pipeline_sk_iIGN0tU7Jifjdmycp-gOVoqJyYjLAVQA"
        }
        response = requests.post(upload_url, files=files, headers=headers)
        return response.json()["id"], response.json()["path"]

# define with lang as optional argument
def run_inference(img_path: str, lang: str = "en") -> str:
    try:
        m_id, m_path = upload_img(img_path)
    except Exception as e:
        print("An error occurred while uploading the image:")
        print(str(e))

    # Debug print
    # print(f"File ID: {m_id}, File path: {m_path}")

    # URL for the API endpoint
    url = 'https://www.mystic.ai/v3/runs'

    # Data payload for the POST request
    data = {
        "pipeline_id_or_pointer": "uriel/easyocr-r:v31",
        "async_run": False,
        "input_data": [
            {
                "type": "file",
                "value": "",
                "file_path": m_path
            },
            {
                "type": "string",
                "value": lang
            }
        ]
    }

    # Sending the POST request
    response = requests.post(url, json=data, headers=headers)

    # Checking the response
    if response.status_code == 200:
        print("Request successful")
        # print(response.json())
    else:
        print("Request failed")
        print("Status code:", response.status_code)
        print("Response:", response.text)

    return response.json()

print(run_inference("/home/ubuntu/mysticai-easyocr/tests/media/sun.webp", "en"))
