import os
import cv2
import hashlib
import pickle
from fingerprinting.embedding_db import load_audio_embeddings, add_audio_embeddings
from preprocessing.audio_extractor import extract_audio
from fingerprinting.fingerprint import generate_fingerprint
from ai_models.clip_model import extract_frame_embeddings
from ai_models.clip_similarity import compare_clip_embeddings
from ai_models.yamnet_model import extract_embedding
from blockchain.register import register_hash
from blockchain.verify import verify_hash
from preprocessing.frame_extractor import extract_frames
from fingerprinting.frame_hash import generate_frame_hashes, compare_hashes
from fingerprinting.video_db import load_db, add_video_hashes
from fingerprinting.clip_db import load_clip_embeddings, add_clip_embedding
from fingerprinting.stats_db import load_stats, update_stats
from preprocessing.video_converter import convert_to_mp4
from fingerprinting.database import (
    load_fingerprints, add_fingerprint
)
from fingerprinting.matcher import match_fingerprints as compare
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

clip_db = load_clip_embeddings()
embedding_db = load_audio_embeddings()

def is_low_information_video(frame_folder):
    files = [f for f in os.listdir(frame_folder) if f.endswith(".jpg")]

    if len(files) == 0:
        return True
    
    low_info = 0

    for f in files:
        path = os.path.join(frame_folder, f)
        img = cv2.imread(path)

        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if np.mean(gray) < 5:
            low_info += 1
            continue

        edge = cv2.Canny(gray, 50, 150)

        if np.sum(edge) < 300:
            low_info += 1

    return (low_info / len(files)) > 0.7
 
def process_file(file_path):
    print("\n--- START PIPELINE ---")

    result = {
        "audio_score": 0,
        "video_score": 0,
        "final_score": 0,
        "audio_checked": False,
        "video_checked": False,
        "detected": False,
        "tx_hash": None,
        "message": "",
        "audio_detected_by": None,
        "video_detected_by": None,
        "audio_matched_file": None,
        "video_matched_file": None,
        "detection_details": {},
        "stats": {}
    }

    def record_stats(original_registered=0, duplicate_detected=0, fingerprint_detected=0, audio_ai_detected=0, video_hash_detected=0, video_clip_detected=0):
        stats = update_stats(
            runs=1,
            originals_registered=original_registered,
            duplicates_detected=duplicate_detected,
            audio_fingerprint_detected=fingerprint_detected,
            audio_ai_detected=audio_ai_detected,
            video_hash_detected=video_hash_detected,
            video_clip_detected=video_clip_detected
        )
        result["stats"] = stats
        return stats

    audio_path = os.path.join("uploads", "temp_audio.wav")
    success = extract_audio(file_path, audio_path)

    if not success:
        result["message"] = "Audio Extraction Failed"
        return result

    file_name = os.path.basename(file_path)
    fp = generate_fingerprint(audio_path)
    print("Generated fingerprint length:", len(fp))
    fp_db = load_fingerprints()
    print("DB size:", len(fp_db))


    audio_match = False
    ai_match = False
    video_match = False
    matched_file = None

    audio_match_name = None
    ai_match_name = None
    best_audio_score = 0
    best_ai_score = 0
    max_audio_score = 0

    fp_db = [record for record in fp_db if len(record["fingerprint"]) > 100]
    
    for record in fp_db:
        stored_fp = record["fingerprint"]
        stored_name = record.get("name")
        score = compare(fp, stored_fp)
        max_audio_score = max(max_audio_score, score)

        if score >= 0.40:
            print("Audio match detected:", score)
            audio_match = True
            if score > best_audio_score:
                best_audio_score = score
                audio_match_name = stored_name
            
        elif 0.30 <= score < 0.40:
            print("Running YAMNet for audio confirmation")
            emb = extract_embedding(audio_path)

            for stored_emb_record in embedding_db:
                stored_emb = stored_emb_record["embedding"]
                stored_emb_name = stored_emb_record.get("name")
                sim = cosine_similarity(
                        emb.reshape(1, -1),
                        stored_emb.reshape(1, -1)
                    )[0][0]

                if sim > 0.70:
                    ai_match = True
                    if sim > best_ai_score:
                        best_ai_score = sim
                        ai_match_name = stored_emb_name
        print("Comparing with stored fingerprint")
        print("Stored length:", len(stored_fp))
        print("Score:", score)
                    

    print("Running Video Analysis...")

    video_path = convert_to_mp4(file_path)
    frames = extract_frames(video_path)

    max_video_score = 0
    video_match = False
    hashes = []

    if frames is None:
        print("No frames extracted")

    elif False:
        print("Low information video detected -> skipping video detection")

    else:
        hashes = generate_frame_hashes(frames)

        video_db = load_db()

        best_video_hash_score = 0
        best_video_hash_name = None
        best_video_clip_score = 0
        best_video_clip_name = None
        hash_scores_by_name = {}

        for stored in video_db:
            stored_hashes = stored["hashes"]
            stored_name = stored.get("name")
            v_score = compare_hashes(hashes, stored_hashes)
            hash_scores_by_name[stored_name] = v_score
            max_video_score = max(max_video_score, v_score)

            if v_score > best_video_hash_score:
                best_video_hash_score = v_score
                best_video_hash_name = stored_name

            print("Hash score:", v_score)

            if v_score >= 0.95:
                video_match = True
                result["video_detected_by"] = "hash"
                result["video_matched_file"] = stored_name
                best_video_hash_name = stored_name
                break
            elif 0.85 <= v_score < 0.95:
                print("Moderate hash similarity detected -> verify with CLIP")

        if not video_match and max_video_score >= 0.80:
            print("Potential copyright candidate -> verify with CLIP")
            clip_emb = None
            if len(os.listdir(frames)) < 5:
                print("Not enough frames for CLIP -> skipping CLIP confirmation")
            else:
                clip_emb = extract_frame_embeddings(frames)

                if clip_emb is not None:
                    for stored_emb_record in clip_db:
                        stored_emb = stored_emb_record["embedding"]
                        stored_name = stored_emb_record.get("name")
                        clip_score = compare_clip_embeddings(clip_emb, stored_emb)
                        print("CLIP Score:", clip_score)
                        hash_score_for_name = hash_scores_by_name.get(stored_name, 0)

                        if clip_score > best_video_clip_score:
                            best_video_clip_score = clip_score
                            best_video_clip_name = stored_name

                        if clip_score >= 0.92 and hash_score_for_name >= 0.80:
                            video_match = True
                            result["video_detected_by"] = "clip"
                            result["video_matched_file"] = stored_name
                            best_video_clip_name = stored_name
                            break
                        if clip_score >= 0.95 and hash_score_for_name >= 0.70:
                            video_match = True
                            result["video_detected_by"] = "clip"
                            result["video_matched_file"] = stored_name
                            best_video_clip_name = stored_name
                            break

        if best_video_hash_score >= 0.95 and not video_match:
            video_match = True
            result["video_detected_by"] = "hash"
            result["video_matched_file"] = best_video_hash_name

        if video_match and result.get("video_detected_by") is None:
            if best_video_clip_score >= 0.92:
                result["video_detected_by"] = "clip"
                result["video_matched_file"] = best_video_clip_name
            elif best_video_hash_score >= 0.95:
                result["video_detected_by"] = "hash"
                result["video_matched_file"] = best_video_hash_name

        if not video_match and len(hashes) >= 5:
            add_video_hashes(hashes, file_name)
            clip_emb = extract_frame_embeddings(frames)
            add_clip_embedding(clip_emb, file_name)
            clip_db.append({"name": file_name, "embedding": clip_emb})

    if audio_match:
        result["audio_score"] = best_audio_score
    elif ai_match:
        result["audio_score"] = best_ai_score
    else:
        result["audio_score"] = max_audio_score * 0.50

    if video_match:
        result["video_score"] = max(best_video_hash_score, best_video_clip_score)
    else:
        result["video_score"] = max_video_score * 0.45

    result["final_score"] = max(result["audio_score"], result["video_score"])
    result["audio_checked"] = True
    result["video_checked"] = True
    result["audio_detected_by"] = "fingerprint" if audio_match else ("audio_ai" if ai_match else None)
    result["audio_matched_file"] = audio_match_name if audio_match else ai_match_name
    result["video_matched_file"] = result.get("video_matched_file")

    if result["audio_matched_file"] and result["video_matched_file"]:
        if result["audio_matched_file"] == result["video_matched_file"]:
            matched_file = result["audio_matched_file"]
        else:
            matched_file = f"Audio: {result['audio_matched_file']} / Video: {result['video_matched_file']}"
    elif result["audio_matched_file"]:
        matched_file = result["audio_matched_file"]
    elif result["video_matched_file"]:
        matched_file = result["video_matched_file"]
    else:
        matched_file = None

    result["matched_file"] = matched_file
    result["detection_details"] = {
        "best_audio_score": best_audio_score,
        "best_ai_score": best_ai_score,
        "best_video_hash_score": best_video_hash_score,
        "best_video_clip_score": best_video_clip_score
    }

    if audio_match and video_match:
        result["detected"] = True
        result["message"] = "Copyright Detected (Fingerprint + Video)"
    elif audio_match:
        result["detected"] = True
        result["message"] = "Copyright Detected (Fingerprint)"
    elif ai_match:
        result["detected"] = True
        result["message"] = "Copyright Detected (By AI Model)"
    elif video_match:
        result["detected"] = True
        result["message"] = "Copyright Detected (Video)"
    else:
        hash_string = hashlib.sha256(pickle.dumps(fp)).hexdigest()

        if verify_hash(hash_string):
            result["message"] = "Already Registered on the Blockchain"
            record_stats(
                original_registered=0,
                duplicate_detected=1,
                fingerprint_detected=int(audio_match),
                audio_ai_detected=int(ai_match and not audio_match),
                video_hash_detected=int(result["video_detected_by"] == "hash"),
                video_clip_detected=int(result["video_detected_by"] == "clip")
            )
            return result
        
        emb = extract_embedding(audio_path)

        add_fingerprint(fp, file_name)
        add_audio_embeddings(emb, file_name)
        embedding_db.append({"name": file_name, "embedding": emb})

        register_hash(hash_string)

        result["tx_hash"] = hash_string
        result["message"] = "Original Registered"
        record_stats(
            original_registered=1,
            duplicate_detected=0,
            fingerprint_detected=int(audio_match),
            audio_ai_detected=int(ai_match and not audio_match),
            video_hash_detected=int(result["video_detected_by"] == "hash"),
            video_clip_detected=int(result["video_detected_by"] == "clip")
        )
        return result

    record_stats(
        original_registered=0,
        duplicate_detected=1,
        fingerprint_detected=int(audio_match),
        audio_ai_detected=int(ai_match and not audio_match),
        video_hash_detected=int(result["video_detected_by"] == "hash"),
        video_clip_detected=int(result["video_detected_by"] == "clip")
    )

    return result