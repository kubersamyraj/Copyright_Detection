import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "dataset", "audio_db.pkl")

def normalize_fingerprints(db):
    if not db:
        return []
    if isinstance(db[0], dict):
        return db
    return [{"name": None, "fingerprint": entry} for entry in db]

def load_fingerprints():
    if not os.path.exists(DB_PATH):
        print("Creating new audio DB...")
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        with open(DB_PATH, "wb") as f:
            pickle.dump([], f)
        return []
    
    with open(DB_PATH, "rb") as f:
        db = pickle.load(f)
    
    db = normalize_fingerprints(db)
    print("Loaded DB Size:", len(db))
    return db
    
def save_fingerprints(db):
    with open(DB_PATH, "wb")  as f:
        pickle.dump(db, f) 

def add_fingerprint(fp, name=None):
    db = load_fingerprints()
    db.append({"name": name, "fingerprint": fp})
    save_fingerprints(db)

    print("Audio DB updated. Total:", len(db))
