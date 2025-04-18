import cv2
import os
from deepface import DeepFace
from .face_utils import crop_face_mtcnn
import numpy as np

def analyze_video_emotions(video_path: str, frame_rate: int = 1):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * frame_rate)

    frame_count = 0
    results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            try:

                #convertir el frame a una imagen temporal para analisis
                temp_frame_path = f"temp_frame_{frame_count}.jpg"
                cv2.imwrite(temp_frame_path, frame)

                cropped_path = crop_face_mtcnn(temp_frame_path)
                if cropped_path:
                    analysis = DeepFace.analyze(
                        img_path=cropped_path, actions=['emotion'], enforce_detection=True
                    )
                    results.append(analysis[0])
                    os.remove(cropped_path)
                os.remove(temp_frame_path)
            except Exception as e:
                results.append({"error": str(e), "frame": frame_count})

        frame_count += 1

    cap.release()
    return results
