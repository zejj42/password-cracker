from fastapi import FastAPI
from app.routers import api_router

app = FastAPI(title="Agent")
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "pong"}
