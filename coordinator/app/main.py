from fastapi import FastAPI
from .routers import api_router


app = FastAPI(title="Coordinator")
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "pong"}
