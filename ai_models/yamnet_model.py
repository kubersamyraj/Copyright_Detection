import tensorflow as tf
import tensorflow_hub as hub
import librosa
import numpy as np

yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

def extract_embedding(file):
    audio, sr = librosa.load(file, sr=16000)

    scores, embeddings, spectrogram = yamnet_model(audio)

    embeddings = embeddings.numpy()

    return np.mean(embeddings, axis=0)