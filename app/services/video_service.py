import cv2
from app.services.face_service import analyze_emotion_on_frame
from collections import Counter

def extract_frames(video_path, fps=1):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    success, frame_id = True, 0

    while success:
        success, frame = cap.read()
        if not success:
            break
        if frame_id % (frame_rate * fps) == 0:
            frames.append((frame_id // frame_rate, frame.copy()))
        frame_id += 1
    cap.release()
    return frames

def process_video(video_path):
    frames = extract_frames(video_path, fps=1)
    emotion_timeline = {}

    for second, frame in frames:
        emotion = analyze_emotion_on_frame(frame)
        if emotion:
            emotion_timeline[second] = emotion

    emotion_summary = dict(Counter(emotion_timeline.values()))
    return {
        "timeline": emotion_timeline,
        "emotion_summary": emotion_summary
    }
