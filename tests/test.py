# Imports
import requests
import os
from dotenv import load_dotenv

# import base64

# Getting the API key
load_dotenv()
api_key = os.getenv("API_KEY")

# URL for the API endpoint
url = 'https://www.mystic.ai/v3/runs'

# Headers
headers = {
    'Authorization': f"Bearer {api_key}",
    'Content-Type': 'application/json'
}

# Data payload for the POST request
data = {
    "pipeline_id_or_pointer": "uriel/easyocr-r:v30",
    "async_run": False,
    "input_data": [
        {
            "type": "file",
            "value": "",
            "file_path": "https://res.cloudinary.com/practicaldev/image/fetch/s--JHfhlxxt--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_350/https://i.imgur.com/fYloAem.jpg"
            # "file_path": "tests/media/ex.jpeg" # Not working yet
        },
        {
            "type": "string",
            "value": "Russian"
        }
    ]
}

# Sending the POST request
response = requests.post(url, json=data, headers=headers)

# Checking the response
if response.status_code == 200:
    print("Request successful")
    print(response.json())
else:
    print("Request failed")
    print("Status code:", response.status_code)
    print("Response:", response.text)

# ------------------ #
# File path for local testing (not working)
path = "tests/media/test.webp"
# file_name = path.split("/")[-1]
# print(file_name)

# # Base64 encoding for the image (not working)
# def base_img(path: str) -> str:
#     with open(path, "rb") as imageFile:
#         img_base64 = base64.b64encode(imageFile.read()).decode()
#     return img_base64

# img = base_img(path)