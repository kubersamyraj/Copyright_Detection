import os
from PIL import Image
import imagehash

def generate_frame_hashes(frame_folder, max_frames=10):
    hashes = []

    files = sorted(os.listdir(frame_folder))[:max_frames]

    for file in files:
        if file.lower().endswith(".jpg"):
            path = os.path.join(frame_folder, file)

            img = Image.open(path)

            h = imagehash.phash(img)

            hashes.append(str(h))

    return hashes

def _directional_hash_similarity(src_hashes, tgt_hashes, good_threshold, max_distance):
    distances = []
    good_matches = 0

    for h1 in src_hashes:
        h1_hash = imagehash.hex_to_hash(h1)
        best_distance = max_distance

        for h2 in tgt_hashes:
            h2_hash = imagehash.hex_to_hash(h2)
            dist = h1_hash - h2_hash

            if dist < best_distance:
                best_distance = dist

        distances.append(best_distance)
        if best_distance <= good_threshold:
            good_matches += 1

    matched_ratio = good_matches / len(src_hashes)
    average_similarity = sum(max(0.0, 1.0 - (d / max_distance)) for d in distances) / len(distances)
    median_distance = sorted(distances)[len(distances) // 2]
    median_similarity = max(0.0, 1.0 - (median_distance / max_distance))

    return matched_ratio, average_similarity, median_similarity


def compare_hashes(hashes1, hashes2):
    if not hashes1 or not hashes2:
        return 0.0

    max_distance = 64.0
    good_threshold = 7

    ratio12, avg12, med12 = _directional_hash_similarity(hashes1, hashes2, good_threshold, max_distance)
    ratio21, avg21, med21 = _directional_hash_similarity(hashes2, hashes1, good_threshold, max_distance)

    ratio = (ratio12 + ratio21) / 2
    average_similarity = (avg12 + avg21) / 2
    median_similarity = (med12 + med21) / 2

    score = ratio * 0.7 + median_similarity * 0.2 + average_similarity * 0.1

    if ratio < 0.35:
        score *= 0.4
    elif ratio < 0.45:
        score *= 0.55

    if median_similarity < 0.80 and ratio < 0.60:
        score *= 0.7

    return score