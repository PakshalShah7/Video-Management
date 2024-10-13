from fastapi import FastAPI

from app.db import init_db
from app.routes.video_routes import router as video_router

app = FastAPI()

app.include_router(video_router)


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def root():
    return {"message": "Video Management API is running"}
