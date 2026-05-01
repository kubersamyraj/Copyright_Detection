import librosa
import hashlib
import numpy as np
from scipy.ndimage import maximum_filter

def stable_hash(f1, f2, dt):
    return hashlib.sha1(f"{f1}-{f2}-{dt}".encode()).hexdigest()

def get_spectrogram(file):
    y, sr = librosa.load(file, sr=22050, mono=True)
    y = np.nan_to_num(y)

    max_val = np.max(np.abs(y))

    if max_val > 0:
        y = y / max_val

    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    return S

def find_peaks(S, amp_min=0.3):
    local_max = maximum_filter(S, size=20)
    peaks = (S == local_max) & (S > amp_min)
    freq_idx, time_idx = np.where(peaks)

    peaks = list(zip(freq_idx, time_idx))
    peaks.sort(key=lambda x: x[1])
    return peaks[:2000]

def generate_hashes(peaks, fan_value=20):
    hashes = []

    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if i + j < len(peaks):
                f1, t1 = peaks[i]
                f2, t2 = peaks[i + j]

                dt = t2 - t1

                if 0 < dt <= 300:
                    f1_q = f1 // 5
                    f2_q = f2 // 5
                    dt_q = dt // 5

                    hash_val = stable_hash(f1_q, f2_q, dt_q)
                    hashes. append((hash_val, t1))

    return hashes

def generate_fingerprint(file):
    S = get_spectrogram(file)
    peaks = find_peaks(S)
    hashes = generate_hashes(peaks)

    return hashes