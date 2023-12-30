import requests
import base64

# URL for the API endpoint
url = 'https://www.mystic.ai/v3/runs'

# Headers to be sent with the request
headers = {
    'Authorization': 'Bearer pipeline_sk_iIGN0tU7Jifjdmycp-gOVoqJyYjLAVQA',
    # 'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

path = "tests/ex.jpeg"
file_name = path.split("/")[-1]
print(file_name)
with open(path, "rb") as imageFile:
    data = base64.b64encode(imageFile.read()).decode('')
    
# Data payload for the POST request
data = {
    "pipeline_id_or_pointer": "uriel/easyocr:v22",
    "async_run": False,
    "input_data": [
        {
            "type": "file",
            "value": data,
            # "file_path": "https://api.telegram.org/file/bot6678109627:AAFmbzFijiTcICi_dWSiFjeVuIiWbG9cjP8/photos/file_15.jpg"
            "file_path": ""
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
