import shutil
from fastapi import UploadFile, File, APIRouter, Form, Request
from typing import List

from fastapi.responses import JSONResponse

from schemas import *

video_router = APIRouter()


@video_router.post("/")
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(file.filename, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        file.file.close()
    return {'file': file.filename, 'info': info}


@video_router.post("/img", status_code=200)
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(img.filename, 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)
            img.file.close()
    return {'file': 'good'}


@video_router.get("/video", response_model=GetVideo, responses={404: {'model': Message}})
async def get_video():
    user = {'id': 25, 'name': 'Pipec'}
    video = {'title': 'Test', 'description': 'Description'}
    info = GetVideo(user=user, video=video)

    return JSONResponse(status_code=200, content=info.dict())


@video_router.get("/test")
async def get_test(req: Request):
    print(req.headers)
    return {}
