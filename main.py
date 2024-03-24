import json
import time
from unittest import result
import uuid
from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
import os

import requests

app = FastAPI()

@app.get("/")
def 시작():
    return 'Hello'

@app.post("/upload_image")
async def upload_image(img_file:UploadFile =File(...)):

    if '.jpg' in img_file.filename or '.jpeg' in img_file.filename or '.png' in img_file.filename:
        file_save_path="./images/"+img_file.filename
        if os.path.exists("./images") == False:
            os.makedirs("./images")

        with open(file_save_path, "wb") as f:
            f.write(img_file.file.read())

        if os.path.exists(file_save_path):
            return {"image_path":file_save_path,"message": "Image saved successfully"}
        else:
            return {"error":"Image Not saved !!!"}
    else:
        return {"error": "File Type is not valid please upload only jpg,jpeg and png"}
    

api_url = 'https://zi0uv1fzvz.apigw.ntruss.com/custom/v1/28276/d3e2835462d47248f2cb0ae0e59b207575163a11137316a56754d3d3e66e6bd1/general'
secret_key = 'dmhSWmZoQkJDbE5ic1VhbVFEeGxqR2xsZUJqdnpvSms='
image_file = './images//sample1.jpg'

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))

result = response.json()
with open('result.json', 'w', encoding='utf-8') as make_file:
    json.dump(result, make_file, indent="\t", ensure_ascii=False)

text = " "
for field in result['images'][0]['fields']:
    text += field['inferText']
print(text)
