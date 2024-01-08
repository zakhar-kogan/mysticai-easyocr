# EasyOCR for Mystic.ai

# Installation
1. `git clone` & `cd` into the repo
2. `pdm install` or `python -m pip install .`
3. Create the `.env` file using `env.example` as a template
4. `pdm start` to upload the pipeline, OR `/tests` for code snippets

## Usage

### Calling the API using POST requests
Refer to `/tests/test.py` for an example of how to call the API using POST requests.

Mystic.ai can't handle the files directly, they require uploading to the storage first. It can be managed by [pipeline-ai](https://pypi.org/project/pipeline-ai/) or by using [POST requests](https://docs.mystic.ai/reference/file_post_v3_pipeline_files_post).

POST request snippet is @ `upload_img` function in `/tests/test.py`.

#### Parameters
- **image (File)**: This should be a .png, .jpg, or other image file; or a URL when calling by API.
  
  Important: the file should be uploaded to the storage first, see [here](https://docs.mystic.ai/reference/file_post_v3_pipeline_files_post) for details, or `upload_img` function in `/tests/test.py` for a snippet.
  
  **`upload_img` function takes file path as an argument!**

- **lang (str)** *[Optional]*: The language to use for OCR. Can be either `'ru'`/`'Russian'` or `'en'`/`'English'`. Defaults to English.

#### Returns
- **str**: The OCR output as a JSON with bounding box coordinates, e.g. `[[[[[0, 0], [572, 0], [572, 54], [0, 54]], 'когда забыл 0 том,что закрыл квартиру ,вернулся,а она закрыта:']]]`

If the language is Russian, the function uses a model trained on both English and Russian (see [here](https://www.jaided.ai/easyocr/tutorial/)). If the language is English or any other value/skipped, the function uses a model trained only on English.

### Calling the API using pipeline-ai
Self-explanatory: [documentation @ mystic.ai](https://docs.mystic.ai/docs/learning-the-library) + a snippet @ `tests/ppln.py`.

Requires `pipeline-ai` to be installed.



