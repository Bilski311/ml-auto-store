import os

import torch
from torch.utils.data import DataLoader, random_split
from barcode_dataset import BarcodeDataset

from transforms import transform_image, transform_barcode_to_one_hot
from utils import display_transformed_image

if __name__ == '__main__':
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f'Using device: {device}')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    annotations_file = os.path.join(script_dir, 'dataset/labels/annotations.csv')
    img_dir = os.path.join(script_dir, 'dataset/images')
    dataset = BarcodeDataset(
        annotations_file=annotations_file,
        img_dir=img_dir,
        transform=transform_image,
        target_transform=transform_barcode_to_one_hot
    )

    torch.manual_seed(42)
    dataset_size = len(dataset)
    train_dataset_size = int(dataset_size * 0.8)
    test_dataset_size = dataset_size - train_dataset_size
    train_data, test_data = random_split(dataset, [train_dataset_size, test_dataset_size])
    display_transformed_image(train_data[0][0])
    print(train_data[0][1])
