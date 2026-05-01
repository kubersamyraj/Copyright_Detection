from preprocessing.frame_extractor import extract_frames
from ai_models.clip_model import extract_frame_embeddings
from ai_models.clip_similarity import compare_clip_embeddings
from storage.clip_db import load_clip_db, add_clip_embedding

video = "storage/videos/Cheetah Cubs Final.mp4"

frames = extract_frames(video)

emb = extract_frame_embeddings(frames)

db = load_clip_db()

if not db:
    print("DB empty -> adding first video")
    add_clip_embedding(emb)

else:
    for i, stored in enumerate(db):
        score = compare_clip_embeddings(emb, stored)
        print(f"CLIP match with video {i}: {score:.2f}")

    add_clip_embedding(emb)