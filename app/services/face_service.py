import cv2
from deepface import DeepFace

def extract_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face_img = image[y:y+h, x:x+w]
        return face_img
    return None

def analyze_emotion_on_frame(frame):
    face = extract_face(frame)
    if face is None:
        return None
    try:
        analysis = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False)
        if isinstance(analysis, list):
            analysis = analysis[0]
        return analysis["dominant_emotion"]
    except Exception:
        return None
