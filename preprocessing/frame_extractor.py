import cv2
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def is_valid_frame(frame):
    gray = np.mean(frame)

    if gray < 10:
        return False
    
    if np.std(frame) < 5:
        return False
    
    return True

def extract_frames(video_path):
    video_name = os.path.basename(video_path).replace(".mp4","")
    
    output_folder = os.path.join(BASE_DIR, "dataset", "frames", video_name)

    print("Saving frames to:", output_folder)

    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print("Failed to open Video")
        return None
    
    frame_count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 10 == 0:
            if is_valid_frame(frame):
                frame_path = os.path.join(output_folder, f"frame_{saved}.jpg")
                cv2.imwrite(frame_path, frame)
                saved += 1

        frame_count += 1
    
    cap.release()
    
    print("Total frames saved:", saved)

    return output_folder