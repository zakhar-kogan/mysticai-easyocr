# Imports
import requests
import os
import mimetypes

# Absolute path
absolute_path = os.path.dirname(__file__)

# Getting the API key
if os.getenv("API_KEY"):
    api_key = os.getenv("API_KEY")
else:
    api_key = "pipeline_sk_iIGN0tU7Jifjdmycp-gOVoqJyYjLAVQA"

# Headers
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

def upload_img(path: str) -> tuple:
    upload_url = "https://www.mystic.ai/v4/files"
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
def run_inference(img_path: str, lang: str) -> str:
    try:
        m_id, m_path = upload_img(img_path)
    except Exception as e:
        print("An error occurred while uploading the image:")
        print(str(e))

    # Debug print
    # print(f"File ID: {m_id}, File path: {m_path}")

    # URL for the API endpoint
    url = 'https://www.mystic.ai/v4/runs'

    # m_path = "https://storage.mystic.ai/" + m_path
    m_path = "https://storage.mystic.ai/pipeline_files/4c/4d/275dec7b-5f03-4356-91d0-7c5cafb8c4e0.jpg"
    # Data payload for the POST request
    data = {
        "pipeline": "uriel/easyocr-r:v34",
        "inputs": [
            {
                "type": "file",
                "file_path": m_path
            },
            {
                "type": "string",
                "value": lang
            }
        ],
        "async_run": true
    }

    # Sending the POST request
    print("Running inference...")
    print(data)

    response = requests.post(url, json=data, headers=headers)
    # Checking the response

    if response.status_code == 200:
        print("Request successful")
    else:
        print("Request failed")
        print("Status code:", response.status_code)
        print("Response:", response.text)

    return response.json()

path = absolute_path + "/media/test.webp"
print(run_inference(path, "en"))
