from fastapi import FastAPI
from .routes import video

app = FastAPI(title="EmotionAI API")

app.include_router(video.router, prefix="/api/video", tags=["Video"])
