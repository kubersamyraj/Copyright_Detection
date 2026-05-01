import torch
import clip
from PIL import Image
import os
import numpy as np

device = "cuda" if torch.cuda.is_available() else"cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def extract_frame_embeddings(frame_folder, max_frames=10):
    embeddings = []

    files = sorted(os.listdir(frame_folder))[:max_frames]

    for file in files:
        if file.lower().endswith(".jpg"):
            path = os.path.join(frame_folder, file)

            image = preprocess(Image.open(path)).unsqueeze(0).to(device)

            with torch.no_grad():
                image_features = model.encode_image(image)

            image_features = image_features.cpu().numpy()[0]

            embeddings.append(image_features)

    return np.array(embeddings)