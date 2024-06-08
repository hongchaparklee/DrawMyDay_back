import time
from unittest import result
import uuid
from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, StreamingResponse
import os
import requests
from dotenv import load_dotenv
from hanspell import spell_checker
from hanspell.constants import CheckResult
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess
import base64
from pydantic import BaseModel

load_dotenv()


app = FastAPI(
    title="My API",
    description="API description",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def 시작():
    return 'Hello'

@app.post("/userinfo")
async def user_info(userInfo: str = Form(...)):
    try:
        user_info_file = "user_info.txt"
        with open(user_info_file, "w") as infoFile:
            infoFile.write(userInfo)

        return JSONResponse(content={"user info uploaded"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



UPLOAD_DIRECTORY="./recieve"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        save_path = f"./recieve/{file.filename}"
        with open(save_path, "wb") as image_file:
            content = await file.read()
            image_file.write(content)

        subprocess.run(["python3", "inference.py"], check=True)
        subprocess.run(["python3", "textrank.py"], check=True)
        subprocess.run(["python3", "imgdown.py"], check=True)

        with open("result.txt", 'r') as fileHan:
            unspelled_text = fileHan.read().replace('\n', '')

        print('\nuncorrected text: '+unspelled_text)
        spelled_text=spell_checker.check(unspelled_text)
        print('\ncorrected text: '+spelled_text.checked)
        corrected_text = spelled_text.checked

        corrected_text_file = "corrected_text.txt"
        with open(corrected_text_file, "w") as Cfile:
            Cfile.write(corrected_text)


        file_path3 = "Imgdownload/downloaded_image.png"
        if os.path.exists(file_path3):
            with open(file_path3, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return JSONResponse(content={"image": encoded_image})
        else:
            return JSONResponse(status_code=404, content={"error": "Image not found"})

    except subprocess.CalledProcessError as e:
        print(f"Script failed: {e}")
        return JSONResponse(status_code=500, content={"error": f"Script failed: {e}"})
    except Exception as e:
        print(f"Exception: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/text")
def send_corrected_text():
    try:
        corrected_text_file = "corrected_text.txt"
        with open(corrected_text_file, "r") as Cfile:
            corrected_text = Cfile.read()
        return {corrected_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    expose_headers=["*"]
)
