#!/usr/bin/python3
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    config = uvicorn.Config("main:app", host="0.0.0.0", port=5000, log_level="debug", reload=True)
    server = uvicorn.Server(config)
    server.run()
