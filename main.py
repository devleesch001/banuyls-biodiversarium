#!/usr/bin/python3
import uvicorn
import json
from fastapi import FastAPI, File, UploadFile, WebSocket, APIRouter
from fastapi.responses import FileResponse
from yolov6.core.inferer import Inferer
import time
import threading
import requests
import asyncio
import argparse

app = FastAPI(docs_url="/ia/docs", redoc_url=None)
# app = FastAPI()

API_VERSION = "v1"


inferer_glob = Inferer(None, "weights/best_ckpt.pt", 0, "fishDataset/data.yaml", [416,416], False)
inferer_lock = threading.Lock()

@app.get(f"/ia")
async def root():
    return {"data":{"status":"running"}}

@app.post(f"/ia/{API_VERSION}/image-detection/")
# @app.post(f"/{API_VERSION}/image-detection/")
async def postObjectDetection(file: UploadFile = File(...)):
    print(file)
    contents = await file.read()
    #print(contents)
    # Inference2
    #path = "5e295a5_1666084008932-simonbercy.jpg"
    # inferer = Inferer(contents, "weights/yolov6s.pt", 0, "data/coco.yaml", 640, False)
    if inferer_lock.acquire(False):
        inferer_glob.set_content(contents)
        res = inferer_glob.infer(0.4, 0.45, None, False, 1000, "runs/inference/exp", True, True, False, False, False,use_only_result=True)
        inferer_lock.release()
    else:
        inferer = Inferer(contents, "weights/best_ckpt.pt", 0, "fishDataset/data.yaml", [416,416], False)
        res = inferer.infer(0.4, 0.45, None, False, 1000, "runs/inference/exp", True, True, False, False, False,use_only_result=True)
    print("res",res)
    return {"detection":res}

async def truc(websocket, data):
    await websocket.send_json(data)

async def some_callback(websocket, data):
    await truc(websocket, data)

def between_callback(websocket, data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(some_callback(websocket, data))
    loop.close()


# @app.websocket(f"/{API_VERSION}/live-detection/")
@app.websocket(f"/ia/{API_VERSION}/live-detection/")
async def live_detection(websocket: WebSocket):
    await websocket.accept()
    url = websocket.query_params['target']
    ldt = None
    try:
        # for i in range(100000):
        #     await websocket.send_json(json.dumps({"i":i}))
        # i=0
        
        #g = range(1000)
        #g = inferer.infer_generator(0.4, 0.45, None, False, 1000, "runs/inference/exp", True, True, False, False, False,use_only_result=True)
        # g = truc(100000)
        ldt = LiveDetectionThread(url)
        ldt.start()
        while True:
            # t = Thread(target=truc, args=[websocket,json.dumps({"detection":det})])
            # t.run()
            
            await websocket.send_json(json.dumps({"detection":ldt.getDet()}))
            # await websocket.send_json(json.dumps({"detection":det}))
            # i+=1
            # if i >1000:
            #     g.close()
            #     break
    finally:
        if ldt is not None:
            ldt.stop = True

class LiveDetectionThread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        # self.inferer = Inferer(url, "weights/yolov6s.pt", 0, "data/coco.yaml", 640, False)
        self.inferer = Inferer(url, "weights/best_ckpt.pt", 0, "fishDataset/data.yaml", [416,416], False)
        # Start thread
        self.daemon = True
        self.det = []
        self.lock = threading.Lock()
        self.stop=False

    def getDet(self):
        self.lock.acquire()
        res = self.det.copy()
        self.lock.release()
        return res

    def setDet(self,l):
        self.lock.acquire()
        self.det = l
        self.lock.release()

    def run(self):
        g = self.inferer.infer_generator(0.4, 0.45, None, False, 1000, "runs/inference/exp", True, True, False, False, False,use_only_result=True)
        # g = truc(100000)
        for det in g:
            self.setDet(det)
            if self.stop:
                g.close()
                break
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fast API")
    parser.add_argument("-p", "--port", default=80, type=int, help="port number")
    parser.add_argument("--log_level", default="info", type=str, help="Log level info : 'critical', 'error', 'warning', 'info', 'debug', 'trace'")
    parser.add_argument("--reload", default=False, type=bool, help="auto reload")
    args = parser.parse_args()
    
    config = uvicorn.Config("main:app", host="0.0.0.0", port=args.port, log_level=args.log_level, reload=args.reload)
    server = uvicorn.Server(config)
    server.run()

