import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_PATH = os.path.join(BASE_DIR, "fingerprinting", "detection_stats.json")

DEFAULT_STATS = {
    "runs": 0,
    "audio_fingerprint_detected": 0,
    "audio_ai_detected": 0,
    "video_hash_detected": 0,
    "video_clip_detected": 0,
    "duplicates_detected": 0,
    "originals_registered": 0
}


def load_stats():
    if not os.path.exists(STATS_PATH):
        os.makedirs(os.path.dirname(STATS_PATH), exist_ok=True)
        with open(STATS_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_STATS, f, indent=2)
        return DEFAULT_STATS.copy()

    with open(STATS_PATH, "r", encoding="utf-8") as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            stats = DEFAULT_STATS.copy()

    for key, value in DEFAULT_STATS.items():
        stats.setdefault(key, value)

    return stats


def save_stats(stats):
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def update_stats(**kwargs):
    stats = load_stats()
    for key, value in kwargs.items():
        if key not in stats:
            stats[key] = 0
        stats[key] += value
    save_stats(stats)
    return stats
