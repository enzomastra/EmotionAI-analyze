from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.video_service import process_video
from ..utils.file_utils import is_allowed_file
import os

router = APIRouter()

@router.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Formato de archivo no compatible. Solo .mp4 es permitido.")

    try:
        temp_file_path = f"./uploads/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        result = process_video(temp_file_path)
        
        os.remove(temp_file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el video: {str(e)}")