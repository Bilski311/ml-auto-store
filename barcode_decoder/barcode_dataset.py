import os
import pandas as pd
from torch.utils.data import Dataset
from PIL import Image


class BarcodeDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file, dtype={'label': str})
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, item):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[item, 0])
        image = Image.open(img_path)
        label = self.img_labels.iloc[item, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)

        return image, label
