from preprocess import audio_to_tensor
import torch

def load_pair(path1, path2, label):
    a1 = audio_to_tensor(path1)
    a2 = audio_to_tensor(path2)

    # Add batch dimension
    a1 = a1.unsqueeze(0)
    a2 = a2.unsqueeze(0)

    label = torch.tensor(label).float()

    return a1, a2, label