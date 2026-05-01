import librosa
import numpy as np

def generate_spectogram (audio_path):

    audio_path = "D:/College/Major Project/Final/copyright_ai/storage/audio/"

    y , sr = librosa.load(audio_path, sr=44100, duration = 5)

    stft = librosa.stft(y, n_fft=4096, hop_length=512)

    spectogram = np.abs(stft)

    spectogram_db = librosa.amplitude_to_db(spectogram)

    spectogram_db = (spectogram_db - np.mean(spectogram_db)) / np.std(spectogram_db)

    spectogram_db = spectogram_db[:128, :128]

    return spectogram_db