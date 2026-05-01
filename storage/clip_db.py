import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "storage", "clip_db.pkl")

def load_clip_db():
    if not os.path.exists(DB_PATH):
        return[]
    
    with open(DB_PATH, "rb") as f:
        return pickle.load(f)
    
def save_clip_db(db):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with open(DB_PATH, "wb") as f:
        pickle.dump(db, f)

def add_clip_embedding(emb):
    db = load_clip_db()
    db.append(emb)
    save_clip_db(db)