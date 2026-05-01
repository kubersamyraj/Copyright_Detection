from preprocessing.frame_extractor import extract_frames
from fingerprinting.frame_hash import generate_frame_hashes, compare_hashes
from fingerprinting.video_db import load_db, add_video_hashes
from preprocessing.video_converter import convert_to_mp4
import os

BASE_DIR = r"D:\College\Major_Project\Final\copyright_ai"
video = os.path.join(BASE_DIR, "storage", "videos", "CheetahCubsFinal.mp4")

video_path = convert_to_mp4(video)

frames = extract_frames(video_path)

hashes = generate_frame_hashes(frames)

db = load_db()

if not db:
    print("Database empty -> adding first video")
    add_video_hashes(hashes)

else:
    for i, stored in enumerate(db):
        score = compare_hashes(hashes, stored)
        print(f"Match with video {i}: {score:.2f}")
    
    add_video_hashes(hashes)
    print("hashes count:", len(hashes))
    print("Stored count:", len(db))