#!/usr/bin/python3
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

API_VERSION = "v1"


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("favicon.png")


@app.get("/")
async def home():
    return {"message": "API for fish recognition! Check documentation on /docs ."}


@app.post(f"/{API_VERSION}/object-detection/with-image/")
async def postObjectDetectionWithImage(file: UploadFile = File(...)):
    return {f"{UploadFile.file.name}"}


@app.post(f"/{API_VERSION}/object-detection/")
async def postObjectDetection(file: UploadFile = File(...)):
    return {f"{UploadFile.file.name}"}


if __name__ == "__main__":
    config = uvicorn.Config("main:app", host="0.0.0.0", port=5000, log_level="debug", reload=True)
    server = uvicorn.Server(config)
    server.run()
