from dataset import AudioDataset
dataset = AudioDataset("dataset/original", "dataset/modified")

a1, a2, label = dataset[0]

print(a1.shape, a2.shape, label)