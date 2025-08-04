from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List




app = FastAPI()

#  跨域中间件配置，允许所有来源跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可根据需要指定允许的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 上传文件存储目录
UPLOAD_FOLDER = "./software_uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post("/software/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    单文件上传
    """
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return JSONResponse(status_code=200, content={
        "message": "File uploaded successfully",
        "filename": file.filename,
        "filepath": file_location
    })

@app.post("/software/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """
    多文件上传
    """
    uploaded_files = []
    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())
        uploaded_files.append({
            "filename": file.filename,
            "filepath": file_location
        })
    return JSONResponse(status_code=200, content={
        "message": "Files uploaded successfully",
        "files": uploaded_files
    })

@app.get("/software/download/{filename}")
async def download_file(filename: str):
    """
    文件下载
    """
    file_location = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_location):
        return JSONResponse(status_code=404, content={"message": "File not found"})
    return FileResponse(file_location, media_type="application/octet-stream", filename=filename)


#增加到处文件列表
@app.get("/software/list/")
async def list_files():
    """
    列出上传的文件
    """
    files = os.listdir(UPLOAD_FOLDER)
    return JSONResponse(status_code=200, content={
        "message": "Files retrieved successfully",
        "files": files
    })