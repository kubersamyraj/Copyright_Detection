from ai_models.yamnet_model import extract_embedding
from ai_models.similarity import cosine_similarity

file1 = "storage/audio/Cheetah Cubs Final.wav"
file2 = "storage/audio/Cheetah Cubs Final.wav"

emb1 = extract_embedding(file1)
emb2 = extract_embedding(file2)

score = cosine_similarity(emb1, emb2)

print("YAMNet similarity:", score)