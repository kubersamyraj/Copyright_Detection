import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "dataset", "clip_embeddings.pkl")

def load_clip_embeddings():
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, "wb") as f:
            pickle.dump([], f)
        return []

    with open(DB_PATH, "rb") as f:
        db = pickle.load(f)

    if not db:
        return []

    if isinstance(db[0], dict) and "embedding" in db[0]:
        return db

    return [{"name": None, "embedding": entry} for entry in db]
    
def add_clip_embedding(emb, name=None):
    db = load_clip_embeddings()
    db.append({"name": name, "embedding": emb})
    with open(DB_PATH, "wb") as f:
        pickle.dump(db, f)