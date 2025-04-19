import cv2
from deepface import DeepFace
from collections import defaultdict
import numpy as np

def extract_frames(video_path, interval=1):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)
    
    frame_interval = int(fps * interval)

    frames = []
    frame_count = 0
    second = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                frames.append((second, frame))
                print(f"✅ Rostro detectado en segundo {second}")
            else:
                print(f"🚫 Sin rostro en segundo {second}, se omite.")

            second += interval

        frame_count += 1

    cap.release()
    return frames

def analyze_emotions(frames):
    emotion_summary = defaultdict(int)
    timeline = {}

    for second, frame in frames:
        try:
            result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=True)
            dominant = result[0]["dominant_emotion"]
            timeline[second] = dominant
            emotion_summary[dominant] += 1
        except Exception as e:
            continue

    return {
        "timeline": timeline,
        "emotion_summary": dict(emotion_summary)
    }
