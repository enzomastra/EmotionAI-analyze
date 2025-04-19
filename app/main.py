from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import uuid

from .video_utils import extract_frames, analyze_emotions

app = FastAPI()

@app.post("/analyze-video/")
async def analyze_video(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".mp4"):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos .mp4")

        os.makedirs("temp", exist_ok=True)
        video_id = str(uuid.uuid4())
        video_path = f"temp/{video_id}.mp4"

        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        frames = extract_frames(video_path)

        if not frames:
            raise HTTPException(status_code=400, detail="No se pudieron extraer frames del video.")

        result = analyze_emotions(frames)

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
