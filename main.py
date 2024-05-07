import json
import time
from unittest import result
import uuid
from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
import os
import requests
from dotenv import load_dotenv
from hanspell import spell_checker
from hanspell.constants import CheckResult

load_dotenv()


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
    

api_url = os.getenv("ocr_api_url")
secret_key = os.getenv("ocr_secret_key")
image_file = './images//diary1.jpg'

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
    text += field['inferText']+ "  "
print(text+'\n')


# spelled_text = spell_checker.check(text)
# print(spelled_text.checked)
# spelled_text.as_dict()
# spelled_text

# for key, value in spelled_text.words.items():
#     if value == 0:
#         # print("맞춤법 검사 통과:",key)        
#         pass
#     elif value ==1:
#         print("맞춤법 오류:",key)
#     elif value ==2:
#         print("띄어쓰기 오류:",key)
#     elif value ==3:
#         print("표준어 의심:",key)
#     elif value ==4:
#         print("통계적 오류 의심:",key)
    


