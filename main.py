#!/usr/bin/python3
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from yolov6.core.inferer import Inferer

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
    print(file)
    contents = await file.read()
    #print(contents)
    # Inference2
    #path = "5e295a5_1666084008932-simonbercy.jpg"
    inferer = Inferer(contents, "weights/yolov6s.pt", 0, "data/coco.yaml", 640, False)
    res = inferer.infer(0.4, 0.45, None, False, 1000, "runs/inference/exp", True, True, False, False, False,use_only_result=True)
    print("res",res)
    return {"detection":res}


if __name__ == "__main__":
    config = uvicorn.Config("main:app", host="0.0.0.0", port=5000, log_level="debug", reload=True)
    server = uvicorn.Server(config)
    server.run()
