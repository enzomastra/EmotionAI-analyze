import cv2
from deepface import DeepFace
import numpy as np

def detect_and_crop_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    cropped_face = frame[y:y+h, x:x+w]
    return cropped_face

def analyze_video_emotions(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_index = 0
    results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if int(frame_index % fps) == 0:  # 1 frame por segundo
            face = detect_and_crop_face(frame)
            if face is not None:
                try:
                    result = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False)
                    emotions = result[0]["emotion"]
                    converted = {k: float(v) for k, v in emotions.items()}
                    results.append({
                        "second": int(frame_index // fps),
                        "emotions": converted
                    })
                except Exception:
                    pass  # Ignora errores de análisis

        frame_index += 1

    cap.release()
    return results
