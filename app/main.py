from fastapi import FastAPI, UploadFile, File
import shutil
import os
from .face_utils import analyze_video_emotions

app = FastAPI()

@app.post("/analyze-video/")
async def analyze_video(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = analyze_video_emotions(temp_path)
        os.remove(temp_path)
        return {"results": result}
    except Exception as e:
        os.remove(temp_path)
        return {"error": str(e)}
