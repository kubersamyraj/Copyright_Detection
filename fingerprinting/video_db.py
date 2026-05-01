import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'fingerprinting', 'video_hash_db.pkl')

def normalize_video_db(db):
    if not db:
        return []
    if isinstance(db[0], dict):
        return db
    return [{"name": None, "hashes": entry} for entry in db]

def load_db():
    if not os.path.exists(DB_PATH):
        print('Creating new video DB...')
        with open(DB_PATH, 'wb') as f:
            pickle.dump([], f)
        return []
    with open(DB_PATH, 'rb') as f:
        db = pickle.load(f)
    return normalize_video_db(db)

def save_db(db):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'wb') as f:
        pickle.dump(db, f)

def add_video_hashes(hashes, name=None):
    db = load_db()
    db.append({"name": name, "hashes": hashes})
    save_db(db)

    print('Video DB updated. Total:', len(db))
